#!/usr/bin/env python
"""Script that fills calculates the MVA values for TTrees."""

import array
import pprint
import os, os.path, shutil
import ROOT; ROOT.PyConfig.IgnoreCommandLineOptions = True
import mvalib.fill
import mvalib.utils

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('mva', help = 'output .root of mva trainer')
	parser.add_argument('trees', nargs = '*', help = 'list of input root files')
	parser.add_argument('-o', '--odir', default=None, help = 'output dir')
	parser.add_argument('-s', '--suf', default='mva', help = 'filename suffix')
	args = parser.parse_args()

	mvas = mvalib.fill.read_mvas(args.mva)
	reader = mvalib.fill.MVAReader(mvas.items()[0][1]['varlist'])

	for name,mvameta in mvas.items():
		reader.book_method(name, mvameta)

	for tree_ifname in args.trees:
		odir = os.path.dirname(tree_ifname) if args.odir is None else args.odir
		if not os.path.isdir(odir):
			os.makedirs(odir)
		
		sample_name = mvalib.utils.get_sample_name(tree_ifname)
		tree_ofname = os.path.join(odir, '{0}_{1}.root'.format(sample_name, args.suf))
		[tree_ifname,tree_ofname] = map(os.path.abspath, [tree_ifname,tree_ofname])
		print tree_ifname,'>',tree_ofname
		mvalib.fill.fill_tree(reader, tree_ifname, tree_ofname)
