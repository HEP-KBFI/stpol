#!/usr/bin/env python
import sys

import ROOT; ROOT.PyConfig.IgnoreCommandLineOptions = True

from mvalib import utils
from plots.common.cuts import Cuts, Cut
from plots.common.plot_defs import cutlist

def main(argv):
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-l', '--lepton_channel', help = 'used to identify default trees and cutstring', choices=['ele', 'mu'], required=True)
	parser.add_argument('-v', '--var', help = 'variable name to find the cut point for', required=True)
	parser.add_argument('-c', '--cutstring', help = 'cutstring (in python format) to apply before cutting on var', default=None)
	parser.add_argument('-e', '--efficiency', help = 'efficiency you want to achive', required=True, type=float)
	parser.add_argument('trees', nargs = '*', help = 'list of input root files to calculate the efficiency in')
	args = parser.parse_args(argv)
	
	lept = args.lepton_channel
	
	filenames = []
	if len(args.trees) > 0:
		filenames = args.trees
	else:
		filenames.append("../step3_latest/{0}/mc/iso/nominal/Jul15/T_t_ToLeptons.root".format(lept))
		filenames.append("../step3_latest/{0}/mc/iso/nominal/Jul15/Tbar_t_ToLeptons.root".format(lept))

	if len(filenames) == 0:
		print "Error: did not find any files"
		return
	
	files = {}
	trees = {}
	samples = {}
	for f in filenames: 
		files[f] = ROOT.TFile(f);
		trees[f] = files[f].Get("trees/Events")
		samples[trees[f]] = 1;
	
	cutstring = str(cutlist['2j1t']*cutlist['presel_{0}'.format(lept)])
	if args.cutstring is not None:
		print "cutstring = str({0})".format(args.cutstring)
		cutstring = str(eval(args.cutstring))
	
	res = utils.find_cut_value(samples, args.var, args.efficiency, cutstring)
	
	print "To achive {0}% efficiecy, you should cut {1} > {2}".format(100*args.efficiency, args.var, res)

if __name__ == "__main__":
	main(sys.argv[1:])
