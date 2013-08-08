"""Utility methods for the MVA library."""

import os.path
import pickle
import ROOT
from plots.common import cross_sections

def write_TObject(name, obj, directory, overwrite=True):
	"""Pickle the object `obj` and write it to a ROOT directory."""
	pString = pickle.dumps(obj)
	directory.WriteTObject(ROOT.TObjString(pString), name, 'Overwrite' if overwrite else '')


def read_TObject(name, directory):
	"""Read a pickled object from a ROOT file."""
	tObj = directory.Get(name)
	pString = tObj.String().Data()
	return pickle.loads(pString)


def scale_factor(channel, sample, eventcount, fraction=1.0):
	"""Calculate the scalefactor to scale MC to luminosity."""
	if sample.startswith('Single'): 
		print 'Warning: using 1 as data scale factor'
		return 1;
	return (cross_sections.xs[sample]*cross_sections.lumi_iso[channel])/(fraction*eventcount)


def iter_entrylist(elist):
	"""Create an iterator that iterates over TEntryList elements."""
	for n in xrange(0, elist.GetN()):
		yield elist.GetEntry(n)


def get_sample_name(fullpath):
	"""Reduce a path of a ROOT file to the sample name"""
	return '.'.join(os.path.basename(fullpath).split('.')[:-1])

def find_efficiency(signals, cs1, cs2):
	"""Find the event yield ratio with cs1+cs2 compared to just cs1"""
	sum_tot = 0.0
	sum_left = 0.0
	for tree, weight in signals.iteritems():
		sum_tot += tree.GetEntries(cs1) * weight
		sum_left += tree.GetEntries("(" + cs1 + ") && (" + cs2 + ")") * weight
	return sum_left, sum_tot

def find_cut_value(signals, var, efficiency, cs):
	"""Find the cut value for var that gives efficiency, given cs"""
	cmax = float('-Inf')
	cmin = float('Inf')
	for tree in signals:
		cmax = max(cmax, tree.GetMaximum(var))
		cmin = min(cmin, tree.GetMinimum(var))
	cval = (cmax+cmin)/2
	ceff = find_efficiency(signals, cs, "{0} > {1}".format(var, cval))
	iters = 0
	
	while abs(ceff - efficiency) > 0.01 and iters < 30:
		if ceff > efficiency:
			cmin = cval
		else:
			cmax = cval
		cval = (cmax+cmin)/2
		good, total = find_efficiency(signals, cs, "{0} > {1}".format(var, cval))
		ceff = float(good)/total
		iters += 1
	if iters == 30:
		print "Warning: binary search of cut value for "+var+" did not converge"
	return cval
