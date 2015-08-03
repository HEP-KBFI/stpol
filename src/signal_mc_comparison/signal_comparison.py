# prepare the FWLite autoloading mechanism
from PhysicsTools.PythonAnalysis import *
from DataFormats.FWLite import Events, Handle, Lumis

import ROOT
from ROOT import TH1D, TH2D, TFile
ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

import sys
import os
from array import array
from time import gmtime, strftime
import math
#from mva_variables import *
from cuts import *

print "args", sys.argv
channel = sys.argv[1]
dataset = sys.argv[2]
counter = sys.argv[3]
base_filename = sys.argv[4]
added_filename = sys.argv[5]

ROOT.TH1.AddDirectory(False)


variables = ["bdt_sig_bg", "cos_theta_lj"]


qcd_mva_cut = -0.15
#qcd_mva_cut = 0.10
if channel == "ele":
    qcd_mva_cut = 0.15
    #qcd_mva_cut = 0.25

#range_cuts = ["nocut", "reversecut", "qcdcut", "qcdcut_new", "bdtcut_old", "bdtcut"]
cuts = ["preqcd", "preselection", "bdt"]

ranges = {}
ranges["qcd_mva"] = (40, -1, 1)
ranges["bdt_sig_bg"] = (40, -1, 1)
ranges["cos_theta_lj"] = (40,-1,1) 

jettag = ["2j1t", "2j0t", "3j1t", "3j2t"]

infile =  TFile.Open(base_filename, "read")
infile2 =  TFile.Open(added_filename, "read")

events = infile.Get('dataframe')
events2 = infile2.Get('dataframe')

histograms = dict()
c = channel

luminosity = 19670
if channel == "ele":
    luminosity = 19637

for var in variables:
    #if var not in variables and "qcd_mva" not in var and "bdt" not in var: continue
        for cut in cuts:
            #histograms[c][var][jt] = dict()
            dataset_name = dataset
            if dataset == "Tbar_t_ToLeptons" or dataset == "T_t_ToLeptons":
                dataset_name = "Powheg"
            elif dataset == "TToBENu_t-channel" or dataset == "TToBMuNu_t-channel" or dataset == "TToBTauNu_t-channel":
                dataset_name = "Comphep"
            elif dataset == "TToLeptons_tchannel_aMCatNLO":
                dataset_name = "aMC@NLO"
            name = "histo__%s__%s__%s__%s" % (dataset_name, channel, var, cut)
            histograms[c+var+cut] = TH1D(name, name, ranges[var][0], ranges[var][1], ranges[var][2])
            #histograms[c+var][jt].SetDirectory(0)
            histograms[c+var+cut].Sumw2()        

extra_data = {}
i=-1
for event in events2:
    i+=1
    #extra_data[i] = [event.bdt_qcd, event.bdt_sig_bg, event.xsweight, event.wjets_ct_shape_weight, event.wjets_fl_yield_weight]
    try:
        extra_data[i] = [event.xsweight, event.wjets_ct_shape_weight, event.wjets_fl_yield_weight, event.bdt_sig_bg, event.bdt_qcd, event.wjets_pt_weight]
    except AttributeError:
        if i>0:
            print "Error"
            sys.exit(1)

i=-1
missing = 0
nan_events = 0
total_events = 0
for event in events:
    total_events += 1
    i+=1
    #if i not in extra_data: continue
    if not passes_cuts(event, channel): continue
    
    xsweight = extra_data[i][0]
    #wjets_shape_weight = extra_data[i][1]
    #wjets_yield_weight = extra_data[i][2]
    #wjets_pt_weight = extra_data[i][5]

    jt = "%sj%st" % (event.njets, event.ntags)
    

    total_weight = event.pu_weight * event.lepton_weight__id * event.lepton_weight__iso * event.lepton_weight__trigger * xsweight
    #         * wjets_shape_weight
    #if not math.isnan(event.b_weight):
    total_weight *= event.b_weight
    #total_weight *= wjets_pt_weight
    total_weight *= luminosity

    if math.isnan(total_weight): continue
    
    event_vars = {}
    qcd_mva = extra_data[i][4]
    event_vars["bdt_sig_bg"] = extra_data[i][3]
    event_vars["cos_theta_lj"] = event.cos_theta_lj
    
    #preqcd
    for var in event_vars:
        histograms[c+var+"preqcd"].Fill(event_vars[var], total_weight)

    if qcd_mva < qcd_mva_cut: continue

    #preselection
    for var in event_vars:
        histograms[c+var+"preselection"].Fill(event_vars[var], total_weight)
    
    if event_vars["bdt_sig_bg"] < 0.45: continue

    #bdt
    for var in event_vars:
        histograms[c+var+"bdt"].Fill(event_vars[var], total_weight)
    

print "writing"
#print "total events:", total_events, " nans:", nan_events
outfilename = os.path.join(os.environ["STPOL_DIR"], "src/qcd_ntuples/signal_histos/",  channel , "histos_%s_%s_%s.root" % (dataset, channel, counter))

print outfilename
outfile = TFile(outfilename, "RECREATE")
outfile.cd() 

for h in histograms.values():
    h.Write()
    
outfile.Write()
outfile.Close()
print "finished"             

        
