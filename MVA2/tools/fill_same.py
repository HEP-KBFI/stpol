#!/usr/bin/env python
"""Script that fills the MVA values to the same ROOT file."""

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import array
import pprint
import os, os.path, shutil
import mvalib.fill
import mvalib.utils

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('mva', help = 'output .root of mva trainer')
	parser.add_argument('trees', nargs = '*', help = 'list of input root files')
	parser.add_argument('-n', '--tree-name', default='MVA', type=str, help='name of the TTree')
	args = parser.parse_args()

	mvas = mvalib.fill.read_mvas(args.mva)
	reader = mvalib.fill.MVAReader(mvas.items()[0][1]['varlist'])

	for name,mvameta in mvas.items():
		reader.book_method(name, mvameta)

	for tree_ifname in args.trees:
		mvalib.fill.fill_tree(reader, tree_ifname, None, mvatree_name=args.tree_name)
