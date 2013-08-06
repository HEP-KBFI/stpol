"""Utilities that are used to prepare step3 datasets for MVA."""
__all__ = ['MVAPreparer']

import os
import os.path
import shutil
from glob import glob
import array
import random
import zlib
import ROOT
import mvalib.utils

_datatype_paths = {
	('mc','iso'): 'mc/iso/nominal/Jul15',
	('data','iso'): 'data/iso/Jul15',
	('mc','antiiso'): 'mc/antiiso/nominal/Jul15',
	('data','antiiso'): 'data/antiiso/Jul15'
}

# ============================
# Public prepare API functions
# ============================

class MVAPreparer:
	"""Class that is used to prepare samples for MVA.
	
	The class takes the specified step3 files, list of samples and few
	other parameters and creates a MVA training trees based on these.
	If requested, it also copies the step3 structure and adds weigth files
	for fractional trees (with `mva_training_weight`, which is is 0.0 for
	training events, 1/fraction for testing events and 1.0 for events that
	did not pass the cut used to choose training events).
	
	`add_frac`/`add_train`/`add_test` methods are used to specify the samples.
	`category` can be either `signal` or `background`. In `add_frac`, `fraction`
	specifies the amount of events that are used for training.
	
	"""
	def __init__(self, step3_path, datatypes=[('data','iso'), ('mc','iso')], default_cutstring=''):
		"""Initialize the preparer and point it to step3 data files."""
		self._step3_root = step3_path
		self._datatypes = datatypes
		self._samples = []
		self._default_cutstring = str(default_cutstring)

	def add_frac(self, category, sample, iso='iso', cutstring=None, train_fraction=0.5, name=None):
		"""Add test and train trees by splitting the sample up."""
		self._add_sample(category, sample, iso, cutstring, train_fraction, name)

	def add_train(self, category, sample, iso='iso', cutstring=None, name=None):
		"""Add a sample that is used solely for training."""
		self._add_sample(category, sample, iso, cutstring, True, name)

	def add_test(self, category, sample, iso='iso', cutstring=None, name=None):
		"""Add a sample that is used solely for testing."""
		self._add_sample(category, sample, iso, cutstring, False, name)

	def _add_sample(self, category, sample, iso, cutstring, train_fraction, name):
		cutstring = self._default_cutstring if cutstring is None else str(cutstring)
		if name is None:
			name = '{0}_{1}_cut{2}'.format(sample, iso, str(abs(zlib.adler32(cutstring))))
		f = {'category':category, 'fraction':train_fraction, 'name':name, 'sample':sample, 'iso':iso,
		     'cut': cutstring}
		print 'Adding sample `{0}` ({1}, {2}) fraction={3}, cat={4}'.format(f['name'], f['iso'], f['sample'], f['fraction'], f['category'])
		self._samples.append(f)

	def write(self, channel, ofname, step3_ofdir=None):
		"""Prepare the MVA training trees.

		It takes the samples from the specified channel, applies a the cut
		and writes out a ROOT file (`ofname`) with the training and test trees.
		If `step3_ofdir` is specified it also clones the step3 structure,
		symlinks the original sources and adds a weight file for fractional
		samples.

		The `cutstring` can also be a dictionary, where key is the sample name
		and value is the cutstring.

		"""
		self._channel = str(channel)

		print 'Prepping channel `{0}` to `{1}`'.format(self._channel, ofname)
		tfile = ROOT.TFile(ofname, 'RECREATE')

		meta = {
			'lept': self._channel, 'ch': self._channel, 'channel': self._channel,
			'samples': {}
		}

		_dir = tfile.mkdir('train')
		_dir.mkdir('signal'); _dir.mkdir('background')
		_dir = tfile.mkdir('test')
		_dir.mkdir('signal'); _dir.mkdir("background")
		tempdir = tfile.mkdir('temporary')  # FIXME: hack.. more below..

		for s in self._samples:
			print 'Prepping sample `{0}` ({1}, {2})'.format(s['name'], s['iso'], s['sample'])
			sample_ifname_mc = os.path.join(self._step3_root, self._channel, _datatype_paths[('mc',s['iso'])], '{0}.root'.format(s['sample']))
			sample_ifname_data = os.path.join(self._step3_root, self._channel, _datatype_paths[('data',s['iso'])], '{0}.root'.format(s['sample']))
			if os.path.isfile(sample_ifname_mc) and not os.path.isfile(sample_ifname_data):
				is_mc_sample = True
			elif not os.path.isfile(sample_ifname_mc) and os.path.isfile(sample_ifname_data):
				is_mc_sample = False
			elif os.path.isfile(sample_ifname_mc) and os.path.isfile(sample_ifname_data):
				raise Exception('Sample `{0}` ({1}) in both MC and data (mc:{2}, data:{3})'.format(s['sample'], s['iso'], sample_ifname_mc, sample_ifname_data))
			else:
				raise Exception('Sample `{0}` ({1}) missing (mc:{2}, data:{3})'.format(s['sample'], s['iso'], sample_ifname_mc, sample_ifname_data))

			sample_ifname = sample_ifname_mc if is_mc_sample else sample_ifname_data
			sample_tfile = ROOT.TFile(sample_ifname)
			sample_ttree = sample_tfile.Get('trees/Events')

			sample_count_hist = sample_tfile.Get('trees/count_hist')
			s['initial_events'] = sample_count_hist.GetBinContent(1)
			meta['samples'][s['name']] = s

			if isinstance(s['fraction'], float):
				# if the sample is fractional
				tc = _TrainTreeCreator(sample_ttree, s['cut'], s['fraction'])
				tc.write_train_tree(
					tfile.Get('{0}/{1}'.format('train', s['category'])),
					name=s['name']
				)
				tc.write_test_tree(
					tfile.Get('{0}/{1}'.format('test', s['category'])),
					name=s['name']
				)

				if step3_ofdir is not None:
					wfile_datatype_path = _datatype_paths[('mc' if is_mc_sample else 'data',s['iso'])]
					wfile_path = os.path.join(step3_ofdir, self._channel, wfile_datatype_path)
					if not os.path.isdir(wfile_path):
						os.makedirs(wfile_path)
					wfile_ofname = os.path.join(wfile_path, '{0}_mvaweight.root'.format(s['sample']))
					wfile_tfile = ROOT.TFile(wfile_ofname, 'RECREATE')
					wfile_tdir = wfile_tfile.mkdir('trees')
					tc.write_weight_tree(wfile_tdir)
					wfile_tfile.Close()
			else:
				roodir = '{0}/{1}'.format('train' if s['fraction'] else 'test', s['category'])
				s['fraction'] = 1.0 if s['fraction'] else 0.0
				print 'Clone tree `{0}` to `{1}`'.format(s['name'], roodir)
				tempdir.cd() # FIXME: ugly hack because ROOT stores it's temporary trees also..
				otree = sample_ttree.CopyTree(s['cut'])
				tfile.Get(roodir).cd()
				otree.Write(s['name'])
				print 'Events written:', otree.GetEntries()

			sample_tfile.Close()
		mvalib.utils.write_TObject('meta', meta, tfile)
		tfile.Close()

		# Create symlinks to other step3 trees
		if step3_ofdir is not None:
			self._symlink_step3(step3_ofdir)

	def _symlink_step3(self, ofdir):
		"""Create symlinks for step3 output."""
		for datatype in self._datatypes:
			p, ss = _find_files(self._step3_root, self._channel, datatype)
			if not os.path.isdir(os.path.join(ofdir, p)):
				os.makedirs(os.path.join(ofdir, p))
			for s in ss:
				sample_ifname = os.path.abspath(os.path.join(self._step3_root, p, '{0}.root'.format(s)))
				sample_ofname = os.path.join(ofdir, p, '{0}.root'.format(s))
				print 'Symlinking sample: `{0}` ({1})'.format(s, sample_ofname)
				os.symlink(sample_ifname, sample_ofname)


# =========================
# Internal helper functions
# =========================

def _find_files(root, channel, datatype):
	"""Finds the root files for the specified type of data."""
	if not channel in ['mu', 'ele']:
		raise Exception('Bad channel `{0}`'.format(channel))
	if not datatype in _datatype_paths:
		raise Exception('Bad datatype `{0}`'.format(datatype))

	path = os.path.join(root, channel, _datatype_paths[datatype])
	samples = map(mvalib.utils.get_sample_name, glob(os.path.join(path, '*')))
	return os.path.join(channel, _datatype_paths[datatype]), samples


class _TrainTreeCreator:
	"""Helper class that is used to create and write the training trees."""
	def __init__(self, tree, cutstring, fraction):
		self.tree = tree
		self.cutstring = cutstring
		self.fraction = fraction

		self.elist_all = ROOT.TEntryList('elist_all', '')
		self.elist_cut = ROOT.TEntryList('elist_cut', '')
		self.elist_invcut = ROOT.TEntryList('elist_invcut', '')

		self.tree.Draw('>>elist_all', '', 'entrylist')
		self.tree.Draw('>>elist_cut', self.cutstring, 'entrylist')
		self.elist_invcut.Add(self.elist_all)
		self.elist_invcut.Subtract(self.elist_cut)

		evids_cutall = list(mvalib.utils.iter_entrylist(self.elist_cut))
		evids_invcut = list(mvalib.utils.iter_entrylist(self.elist_invcut))
		random.shuffle(evids_cutall)
		N_train = int(self.fraction*len(evids_cutall))
		evids_train = evids_cutall[:N_train]
		evids_test  = evids_cutall[N_train:]

		self.elist_train = ROOT.TEntryList('elist_train', '')
		self.elist_test  = ROOT.TEntryList('elist_test', '')
		map(self.elist_train.Enter, evids_train)
		map(self.elist_test.Enter, evids_test)

		try:
			weight = float(len(evids_cutall))/float((len(evids_cutall)-N_train))
			print 'Weight:', weight
		except ZeroDivisionError as e:
			print 'Warning: ZeroDivisionError', e
			print 'len(evids_cutall):', len(evids_cutall)
			print 'N_train:', N_train
			weight = 0

		weights_test   = list(map(lambda n:(n,0.0), evids_test))
		weights_train  = list(map(lambda n:(n,weight), evids_train))
		weights_invcut = list(map(lambda n:(n,1.0), evids_invcut))
		self.weights = sorted(weights_test+weights_train+weights_invcut)

	def write_weight_tree(self, tdir, treename='mva'):
		print 'Writing weigths to `{0}`'.format(tdir)
		tdir.cd()
		otree = ROOT.TTree(treename, treename)
		var_w = array.array('f', [0])
		br = otree.Branch('mva_training_weight', var_w, 'mva_training_weight/F')

		for n,var_w[0] in self.weights:
			otree.Fill()
		otree.Write()

	def write_train_tree(self, tdir, name='Events'):
		print 'Writing train to `{0}`'.format(tdir)
		self._write_tree(tdir, self.elist_train, name)

	def write_test_tree(self, tdir, name='Events'):
		print 'Writing test to `{0}`'.format(tdir)
		self._write_tree(tdir, self.elist_test, name)

	def _write_tree(self, tdir, elist, name):
		self.tree.SetEntryList(elist)
		tdir.cd()
		otree=self.tree.CopyTree('')
		otree.Write(name)
		print 'Events written:', otree.GetEntries()
