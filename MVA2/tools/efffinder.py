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
	parser.add_argument('-p', '--precut', help = 'cutstring (in python format) to apply before finding efficiency', default=None)
	parser.add_argument('-c', '--cutstring', help = 'cutstring (in python format) to find the efficiency for', required=True)
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
		files[f] = ROOT.TFile(f)
		trees[f] = files[f].Get("trees/Events")
		trees[f].AddFriend("trees/MVA")
		samples[trees[f]] = 1;
	
	precut = str(cutlist['2j1t']*cutlist['presel_{0}'.format(lept)])
	if args.precut is not None:
		print "precut = str({0})".format(args.precut)
		precut = str(eval(args.precut))
	
	print "cutstring = str({0})".format(args.cutstring)
	cutstring = str(eval(args.cutstring))
		
	good, total = utils.find_efficiency(samples, precut, cutstring)
	
	print "With cut ({0})&&({1}) you get {2:.1f}% ({4}/{5}) efficiency compared to just {0} in the following trees: {3}".format(precut, cutstring, 100.0*good/total, filenames, int(good), int(total))

if __name__ == "__main__":
	main(sys.argv[1:])
