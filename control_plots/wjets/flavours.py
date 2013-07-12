import ROOT
from plots.common.sample import Sample
from plots.common.cuts import Cuts
from root_numpy import tree2rec
import numpy
import os
import logging
import glob
import re

from plots.common.hist_plots import plot_hists
from plots.common.sample_style import Styling, ColorStyleGen
from plots.common.legend import legend
from plots.common.tdrstyle import tdrstyle
from plots.common.utils import merge_hists, mkdir_p
import argparse
import pdb
import math

basedir = os.environ["STPOL_DIR"] + "/data"
datadirs = dict()
datadirs["iso"] = "/".join((basedir, "out_step3_joosep_11_07_19_44", "mu" ,"iso", "nominal"))

def get_hf_frac(name, cut):
	logging.info("Getting fractions for %s" % name)
	samp = Sample.fromFile(datadirs["iso"] + "/" + name)
	logging.info("cut=%s" % str(cut))
	arr = tree2rec(samp.tree, ["gen_flavour_bj", "gen_flavour_lj"], selection=str(cut))
	print len(arr)
	counts = dict()
	counts["WXX"] = len(arr)
	#pdb.set_trace()
	#logging.info("array dimensions = ")
	b1 = numpy.abs(arr[:]["gen_flavour_bj"]) == 5
	b2 = numpy.abs(arr[:]["gen_flavour_lj"]) == 5
	
	c1 = numpy.abs(arr[:]["gen_flavour_bj"]) == 4
	c2 = numpy.abs(arr[:]["gen_flavour_lj"]) == 4

	g1 = numpy.abs(arr[:]["gen_flavour_bj"]) == 21
	g2 = numpy.abs(arr[:]["gen_flavour_lj"]) == 21
	
	l1 = (numpy.abs(arr[:]["gen_flavour_bj"]) == 1) + (numpy.abs(arr[:]["gen_flavour_bj"]) == 2) + (numpy.abs(arr[:]["gen_flavour_bj"]) == 3)
	l2 = (numpy.abs(arr[:]["gen_flavour_lj"]) == 1) + (numpy.abs(arr[:]["gen_flavour_lj"]) == 2) + (numpy.abs(arr[:]["gen_flavour_lj"]) == 3)

	counts["Wbb"] = numpy.sum(b1*b2)
	counts["Wgg"] = numpy.sum(g1*g2)
	counts["WgX"] = numpy.sum(g1 + g2)
	counts["WbX"] = numpy.sum(b1 + b2)
	counts["WcX"] = numpy.sum(c1 + c2)
	counts["WlX"] = numpy.sum(l1 + l2)
	logging.info("counts = %s" % str(counts))
	return counts

def make_histos(cut_name, cut, samples, out_dir):
	samp_out_dir = "/".join((out_dir, cut_name))
	mkdir_p(samp_out_dir)
	count_list = ["Wbb", "Wgg", "WbX", "WgX", "WcX", "WlX", "WXX"]

	for s in samples:
		fi = ROOT.TFile(samp_out_dir + "/WJets_flavour_fracs__%s" % s, "RECREATE")
		fi.cd()
		hi = ROOT.TH1I("flavour_counts", "Flavour counts", len(count_list), 0, len(count_list)-1)
		counts = get_hf_frac(s, cut)
		
		i = 1
		for count in count_list:
			hi.SetBinContent(i, counts[count])
			hi.SetBinError(i, math.sqrt(counts[count]))
			hi.GetXaxis().SetBinLabel(i, count)
			i += 1
		hi.Sumw2()

		#Normalize to according to all events
		hi.Scale(10000.0/hi.GetBinContent(i-1))

		samp = Sample.fromFile(datadirs["iso"] + "/" + s)
		if samp.isMC:
			hi.Scale(samp.lumiScaleFactor(20000))
		fi.Write()
		logging.info("Wrote file %s" % fi.GetPath())
		fi.Close()
	return

if __name__=="__main__":
	logging.basicConfig(level=logging.INFO)
	tdrstyle()
	ROOT.gStyle.SetOptTitle(1)
	#ROOT.gStyle.SetTitle


	out_dir = "/".join((os.environ["STPOL_DIR"], "out", "plots", "wjets", "flavour"))
	doHists = False
	doPlots = True
	if doHists:
		samps = [
			"W1Jets_exclusive.root", "W2Jets_exclusive.root", "W3Jets_exclusive.root", "W4Jets_exclusive.root",
			"WJets_sherpa_nominal.root",
			"WJets_inclusive.root",
			"TTJets_MassiveBinDECAY.root",
			#"T_t_ToLeptons.root",
			#"SingleMu.root"
		]
		make_histos("2J0T", Cuts.final(2, 0), samps, out_dir)
		make_histos("2J1T", Cuts.final(2, 1), samps, out_dir)
	if doPlots:
		cut_name = "2J1T"
		fnames = glob.glob(out_dir + "/%s/WJets_flavour_fracs__*.root" % cut_name)
		files = {}
		hists = {}
		for fn in fnames:
			files[re.match(".*__(.*).root", fn).group(1)] = ROOT.TFile(fn)
		logging.info("files = %s" % str(files))

		for sn, fi in files.items():
			hi = fi.Get("flavour_counts")
			hi.SetName(sn)
			Styling.mc_style(hi, sn)
			hists[sn] = hi

		merges = dict()
		merges["WJets inc. MG"] = ["WJets_inclusive"]
		merges["WJets exc, MG"] =  ["W1Jets_exclusive", "W2Jets_exclusive", "W3Jets_exclusive", "W4Jets_exclusive"]
		merges["WJets inc. SHRP"] =  ["WJets_sherpa_nominal"]
		#merges["TTBar inc. MG"] =  ["TTJets_MassiveBinDECAY"]
		#merges["t-channel"] =  ["T_t_ToLeptons"]
		#merges["data"] =  ["TTJets_MassiveBinDECAY"]
		hists_merged = merge_hists(hists, merges)
		hists = hists_merged.values()

		ColorStyleGen.style_hists(hists)
		for h in hists:
			h.SetFillColor(ROOT.kWhite)
		c = plot_hists(hists, x_label="flavour(j,j)", y_label="", draw_cmd="HIST E1")
		leg = legend(hists, styles=len(hists)*["f"], nudge_x=-0.1)
		hists[0].SetTitle("Jet flavour fraction (a.u.) in %s" % cut_name)
		#hists[0].SetFillColor(ROOT.kGreen+2)
		hists[0].SetMinimum(10.0)
		hists[0].SetMaximum(10**7)
		#hists[0].SetLineColor(ROOT.kGreen+2)
		c.SetLogy()
		c.SaveAs("flavour_%s.png" % cut_name)
			