"""Classes and methods that can be used to fill TTrees with MVA values."""
__all__ = ['read_mvas']

import os
import os.path
import sys
import array
import pprint
import ROOT
import mvalib.utils
from mvalib.train import _vartypes

# ================================
# Public API classes and functions
# ================================

def read_mvas(fName):
	"""Reads all the MVAs from a specified ROOT file and returs as a dict."""
	tfile = ROOT.TFile(fName, 'READ')
	meta = mvalib.utils.read_TObject('meta', tfile)
	print '=== MVA metadata ({0}) ==='.format(fName)
	pprint.pprint(meta)

	methods = {}
	for name in meta['mvas']:
		path = 'MVAs/{0}'.format(name)
		methods[name] = mvalib.utils.read_TObject(path, tfile)
		methods[name]['name'] = name

	tfile.Close()
	return methods


class MVAReader:
	"""Wrapper around the TMVA::Reader in order to support the custom format.
	
	Instead of providing weight files and settings variables manually, these
	are read from dictionaries that handle that meta-information. Also, instead
	of filling and evaluating events separately, you supply the input and
	output tree (via `set_trees()`) and then call `fill()`, which fills all the
	output trees. The trees can the be swapped out for the next batch without
	having to reinitialize the MVAReader.
	
	"""
	def __init__(self, variables, silent=False):
		"""Initialize the reader with a list of variables.
		
		The `variables` is a list of variable names in their proper order.
		If `silent` argument is true, option `Silent` is passed to the
		TMVA::Reader. Otherwise the option is `V:Color`.
		
		"""
		self._mvalist = []
		self._discr = array.array('f', [0])
		self._varvals = [(n,array.array(_vartypes[n].lower(), [0])) for n in variables]

		self._reader = ROOT.TMVA.Reader('Silent' if silent else 'V:Color')
		for n,ptr in self._varvals:
			self._reader.AddVariable(n, ptr)

	def book_method(self, name, mvameta):
		"""Calls the TMVA::Reader.BookMVA for the MVA in mvameta dict."""
		mva = {'name': name}
		self._mvalist.append(name)
		
		import tempfile, random, string
		#tempxml_name = '.temp.xml'
		tempxml_name = '/tmp/mvatmp_'+''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))+'.xml'
		print 'Booking {0} from {1}'.format(name, tempxml_name)
		tempxml = open(tempxml_name, 'w')
		tempxml.write(mvameta['xmlstring'])
		tempxml.close()
		self._reader.BookMVA(name, tempxml_name)
		print 'Deleting `{0}`'.format(tempxml_name)
		os.unlink(tempxml_name)

	def set_trees(self, intree, outtree):
		"""Set the input (events) and output (mva values) trees.
		
		A new branch is created in the output tree (mva_<MVA name>).
		
		"""
		self._branches = {}
		self._eventtree = intree
		for mva in self._mvalist:
			self._branches[mva] = outtree.Branch('mva_'+mva, self._discr, 'mva_'+mva+'/F')
		for n,ptr in self._varvals:
			intree.SetBranchAddress(n,ptr)

	def fill(self):
		"""Evaluate all MVAs for all events and fill the output trees."""
		nentries = self._eventtree.GetEntries()
		print 'Filling MVAs ({0} entries)...'.format(nentries)
		for n in range(nentries):
			if (n+1)%2e3 == 0:
				sys.stdout.write('.')
				sys.stdout.flush()
			if (n+1)%100e3 == 0:
				print ' -- {0:5.2f}% done ({1} of {2})'.format(100*float(n+1)/nentries, n+1, nentries)
			self._eventtree.GetEntry(n)
			for mva in self._mvalist:
				self._discr[0] = self._reader.EvaluateMVA(mva)
				self._branches[mva].Fill()
		if nentries%50e3 != 0: print
		print nentries, 'filled!'


def fill_tree(reader, tree_ifname, tree_ofname=None, mvatree_name='MVA'):
	"""Fill a tree with corresponding MVA values.

	It reads the events from the `tree_ifname` ROOT file (trees/Events TTree).
	The MVA values are written to the file `tree_ofname`. If the output file
	is `None` of the same string as the input file, the MVAs are written to
	the same file. The TTree with MVA values is calles `trees/<mvatree_name>`.

	"""
	if tree_ofname is None or tree_ifname == tree_ofname:
		tfile_in = tfile_out = ROOT.TFile(tree_ifname, 'UPDATE')
	else:
		tfile_in  = ROOT.TFile(tree_ifname)
		tfile_out = ROOT.TFile(tree_ofname, 'UPDATE')
	tree_events = tfile_in.Get('trees/Events')

	if not tfile_out.Get('trees'):
		tfile_out.mkdir('trees')

	if not tfile_out.Get('trees/{0}'.format(mvatree_name)):
		tfile_out.Get('trees').cd()
		tree_mva = ROOT.TTree(mvatree_name, mvatree_name)
	else:
		tree_mva = tfile_out.Get('trees/{0}'.format(mvatree_name))

	reader.set_trees(tree_events, tree_mva)
	reader.fill()

	tfile_out.Get('trees').cd()
	tree_mva.SetEntries()
	tree_mva.Write('', ROOT.TObject.kOverwrite)
	tfile_out.Close()
	tfile_in.Close()