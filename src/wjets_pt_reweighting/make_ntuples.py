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

print "args", sys.argv
channel = sys.argv[1]
dataset = sys.argv[2]
counter = sys.argv[3]
iso = sys.argv[4]
base_filename = sys.argv[5]
added_filename = sys.argv[6]

ROOT.TH1.AddDirectory(False)


var = "w_pt"

#qcd_mva_cut = -0.15
#if channel == "ele":
#    qcd_mva_cut = 0.15

jt = "2j0t"

infile =  TFile.Open(base_filename, "read")
infile2 =  TFile.Open(added_filename, "read")

events = infile.Get('dataframe')
events2 = infile2.Get('dataframe')

colnames = ["xsweight"]

histograms = dict()

c = channel

#luminosity  = 19764
luminosity = 19670
if channel == "ele":
    luminosity = 19637

dataset_name = dataset
if dataset.startswith("Single"):
    dataset_name = "data"
elif dataset.startswith("QCD"):
    dataset_name = "QCD"
name = "%s__%s__%s__%s__%s" % (var, channel, jt, iso, dataset_name)
histogram = TH1D(name, name, 25, 0, 250)
#histograms[c+var][jt].SetDirectory(0)
histogram.Sumw2()        

extra_data = {}
i=-1
for event in events2:
    i+=1
    extra_data[i] = [event.xsweight, event.wjets_ct_shape_weight, event.wjets_fl_yield_weight, event.bdt_qcd, event.bdt_sig_bg]
    
i=-1
missing = 0
for event in events:
    i+=1
    
    if not (event.njets == 2 and event.ntags == 0): continue
    
    if event.n_signal_mu == 1 and abs(event.lepton_type) == 13:
        ch = "mu"
    elif event.n_signal_ele == 1 and abs(event.lepton_type) == 11:
        ch = "ele"
    else: continue
    if not ch == channel: continue

    #if event.n_veto_mu > 0 or event.n_veto_ele > 0: return False
    
    if event.bjet_pt <= 40 or event.ljet_pt <= 40: continue
    if channel == "mu" and event.hlt_mu != 1: continue
    if channel == "ele" and event.hlt_ele != 1: continue
    
    if math.isnan(event.lepton_weight__id): continue
    if math.isnan(event.lepton_weight__iso): continue
    if math.isnan(event.lepton_weight__trigger): continue
    if math.isnan(event.b_weight): continue
    
    xsweight = extra_data[i][0]
    wjets_shape_weight = extra_data[i][1]
    #wjets_yield_weight = extra_data[i][2]
     
    total_weight = event.pu_weight * wjets_shape_weight * xsweight * event.b_weight * event.lepton_weight__id * event.lepton_weight__iso * event.lepton_weight__trigger
    
    total_weight *= luminosity
    
    if "Single" in dataset:
        total_weight = 1
    
    histogram.Fill(event.w_pt, total_weight)

outfilename = os.path.join(os.environ["STPOL_DIR"], "src/wjets_pt_reweighting/histos/", "histos_%s_%s_%s_%s.root" % (dataset, channel, iso, counter))

print outfilename
outfile = TFile(outfilename, "RECREATE")
outfile.cd() 

histogram.Write()
    
#outfile.Write()
outfile.Close()
print "finished"             

        
