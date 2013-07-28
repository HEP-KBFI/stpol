"""Utilities that are used to prepare step3 datasets for MVA."""
__all__ = ['prepare']

import os
import os.path
import shutil
import tempfile
from glob import glob
#from itertools import product
import ROOT
from plots.common import cuts
import mvalib.utils

_default_cutstring = str(cuts.Cuts.rms_lj*cuts.Cuts.mt_mu*cuts.Cuts.n_jets(2)*cuts.Cuts.n_tags(1))

# ============================
# Public prepare API functions
# ============================

def prepare(signals, backgrounds, step3_path='step3_latest', odir='prepared',
            default_ratio=0.5, copy_trees=False, cutstring=_default_cutstring,
            channels=['mu', 'ele'], datatypes=['data', 'mc']):
	"""Prepares the output files from step3 for usage in the MVA.

	Takes a list of names for signals and backgrounds. They can be either a
	list or a dictionary and in the case of the latter it is expected that
	the keys are the names of the samples and the values are the fraction
	of the sampled used for training. If it is not specified the default_ratio
	is used.

	The function looks for the step3 samples in the step3_path and creates
	a new directory odir where the output is stored. If copy_trees is True
	then all the trees are copied to the odir (retaining the directory structure
	of the step3). Events used for training are removed from the signal and
	background trees.

	"""
	step3_path = os.path.abspath(step3_path)
	if not os.path.isdir(odir):
		os.makedirs(odir)

	signals = _check_default_ratios(signals, default_ratio)
	backgrounds = _check_default_ratios(backgrounds, default_ratio)
	signal_and_bg = dict(signals.items()+backgrounds.items())

	for channel in channels:
		ofname = os.path.join(odir, 'mvaprep_{0}.root'.format(channel))
		tfile = ROOT.TFile(ofname, 'RECREATE')

		meta = {
			'lept': channel, 'ch': channel, 'channel': channel,
			'cutstring': cutstring,
			'initial_events': {}, 'fractions': {}
		}

		_dir = tfile.mkdir('train')
		_dir.mkdir('signal'); _dir.mkdir('background')
		_dir = tfile.mkdir('test')
		_dir.mkdir('signal'); _dir.mkdir("background")

		for datatype in datatypes:
			path, samples = _find_files(step3_path, channel, datatype)
			if copy_trees and not os.path.isdir(os.path.join(odir, path)):
				os.makedirs(os.path.join(odir, path))

			for s in samples:
				sample_ifname = os.path.join(step3_path, path, '{0}.root'.format(s))
				if s in signal_and_bg:
					sigbg = 'signal' if s in signals else 'background'
					
					tfile_sample = ROOT.TFile(sample_ifname)
					meta['initial_events'][s] = tfile_sample.Get('trees/count_hist').GetBinContent(1)
					tc = _TrainTreeCreator(tfile_sample.Get('trees/Events'),
					                       cutstring, signal_and_bg[s])

					odir = tfile.Get('{0}/{1}'.format('train', sigbg))
					tc.write_train_tree(odir)
					odir = tfile.Get('{0}/{1}'.format('test', sigbg))
					tc.write_test_tree(odir)
					
					if copy_trees:
						sample_ofname = os.path.join(odir, path, '{0}.root'.format(s))
						tfile_sample_of = ROOT.TFile(sample_ofname, 'RECREATE')
						odir = tfile_sample_of.mkdir('trees')
						tc.write_test_tree(odir)
						tfile_sample_of.Close()
						
						sample_ofname = os.path.join(odir, path, '{0}_train.root'.format(s))
						tfile_sample_of = ROOT.TFile(sample_ofname, 'RECREATE')
						odir = tfile_sample_of.mkdir('trees')
						tc.write_train_tree(odir)
						tfile_sample_of.Close()
					
					tfile_sample.Close()
				elif copy_trees:
					sample_ofname = os.path.join(odir, path, '{0}.root'.format(s))
					print 'Direct copy: {0} ({1} -> {2})'.format(s, sample_ifname,
					                                                sample_ofname)
					shutil.copyfile(sample_ifname, sample_ofname)

		tfile.Close()


# =========================
# Internal helper functions
# =========================

def _check_default_ratios(samples, ratio):
	"""Checks if samples are a list, converts to dict and set to ratio."""
	if isinstance(samples, dict):
		return samples
	if isinstance(samples, list):
		return dict(map(lambda s: (s, ratio), samples))
	else:
		raise Exception('Bad type for samples `{0}`'.format(type(samples)))


def _find_files(root, channel, datatype):
	"""Finds the root files for the specified type of data."""
	_datatype_paths = {
		'mc': 'mc/iso/nominal/Jul15',
		'data': 'data/iso/Jul15'
	}

	if not channel in ['mu', 'ele']:
		raise Exception('Bad channel `{0}`'.format(channel))
	if not datatype in _datatype_paths:
		raise Exception('Bad datatype `{0}`'.format(datatype))

	path = os.path.join(root, channel, _datatype_paths[datatype])
	samples = map(_get_sample_name, glob(os.path.join(path, '*')))
	return os.path.join(channel, _datatype_paths[datatype]), samples


def _get_sample_name(fullpath):
	"""Reduce a path to a ROOT file to the sample name"""
	return '.'.join(os.path.basename(fullpath).split('.')[:-1])


class _TrainTreeCreator:
	"""Helper class that is used to create and write the training trees."""
	def __init__(self, intree, cutstring, fraction):
		print intree
		
		self.tmpfile = tempfile.NamedTemporaryFile(mode='r')
		self.temp_tfile = ROOT.TFile(self.tmpfile.name, 'RECREATE')
		self.temp_tfile.cd()
		
		self.tree = intree.CopyTree(cutstring)

	def __del__(self):
		print 'del'
		temp_tfile.Close()
		del(self.tmpfile)

	def write_train_tree(self, tdir):
		self._write_tree(tdir, 'training==1')

	def write_test_tree(self, tdir):
		self._write_tree(tdir, 'training==0')

	def _write_tree(self, tdir, cut):
		pass

# Unit testing...
if __name__ == '__main__':
	print 'Default cutstring:', _default_cutstring

	print _find_files('step3_latest', 'mu', 'mc')
	print _find_files('step3_latest', 'ele', 'data')

	try: _find_files('step3_latest', 'tau', 'mc')
	except Exception as e: print e

	try: _find_files('step3_latest', 'mu', 'fake')
	except Exception as e: print e
	
	_check_default_ratios({'a':2, 'b':3}, 0.3)
	_check_default_ratios(['a','b'], 9000)
	try: _check_default_ratios('Woot?', 1337)
	except Exception as e: print e

	prepare(['T_t_ToLeptons', 'Tbar_t_ToLeptons'], ['WW', 'WZ', 'ZZ'])
