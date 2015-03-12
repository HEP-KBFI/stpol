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
from mva_variables import *
from cuts import *

print "args", sys.argv
channel = sys.argv[1]
dataset = sys.argv[2]
counter = sys.argv[3]
iso = sys.argv[4]
base_filename = sys.argv[5]
added_filename = sys.argv[6]

ROOT.TH1.AddDirectory(False)


variables = ["qcd_mva", "met", "mtw"]


ROOT.TMVA.Tools.Instance()
reader = ROOT.TMVA.Reader( "Color:!Silent" )

bdt_varlist = get_fixed(channel)
bdt_vars={}
for bv in bdt_varlist:
    bdt_vars[bv] = array('f',[0])
    reader.AddVariable(bv,bdt_vars[bv])
dirname = os.environ["STPOL_DIR"]+"/src/qcd_mva/weights/"
prefix = "anti_QCD_MVA_07_04"
#prefix = "anti_QCD_MVA_28Nov"
#prefix2 = "MVA_BDT_AN_BDT_from_AN"
reader.BookMVA( "MVA_BDT", dirname+prefix+"_final2_"+channel+".weights.xml" )
#reader.BookMVA( "MVA_BDT", dirname+prefix+"_qcdBDT_"+channel+".weights.xml" )
#reader.BookMVA( "MVA_BDT", dirname+prefix+"_test_final2_withmtw_"+channel+".weights.xml" )
#reader2.BookMVA( "BDT_from_AN", dirname+prefix2+"_"+channel+".weights.xml" )


qcd_mva_cut = 0.4
if channel == "ele":
    qcd_mva_cut = 0.55

#range_cuts = ["nocut", "reversecut", "qcdcut"]
cut_points = {"qcd_mva": qcd_mva_cut, 
    "mtw": 50, "met": 45}

ranges = {}
ranges["reversecut"] = {}
ranges["reversecut"]["qcd_mva"] = (20, -1, qcd_mva_cut)
ranges["reversecut"]["met"] = (9, 0, 45)
ranges["reversecut"]["mtw"] = (10, 0, 50)
ranges["qcdcut"] = {}
ranges["qcdcut"]["qcd_mva"] = (40, qcd_mva_cut, 1)
ranges["qcdcut"]["met"] = (31, 45, 200)
ranges["qcdcut"]["mtw"] = (30, 50, 200)    
ranges["nocut"] = {}
ranges["nocut"]["qcd_mva"] = (40, -1, 1)
ranges["nocut"]["met"] = (40, 0, 200)
ranges["nocut"]["mtw"] = (40, 0, 200)

jettag = ["2j1t", "2j0t", "3j1t", "3j2t", "2j2t", "3j0t", "3j3t"]

infile =  TFile.Open(base_filename, "read")
infile2 =  TFile.Open(added_filename, "read")

print base_filename, added_filename

events = infile.Get('dataframe')
events2 = infile2.Get('dataframe')

colnames = [ "xsweight", "wjets_ct_shape_weight", "wjets_fl_yield_weight"]

histograms = dict()

c = channel

#luminosity  = 19764
luminosity = 16872
if iso == "antiiso":
    luminosity = 16903
if channel == "ele":
    #luminosity = 19820
    luminosity = 18939

for var in variables:
    for jt in jettag:
        dataset_name = dataset
        if dataset.startswith("Single"):
            dataset_name = "data"
        elif dataset.startswith("QCD"):
            dataset_name = "QCD"
        name = "qcd__%s__%s__%s__%s__%s" % (channel, var, jt, iso, dataset_name)
        histograms[c+var+jt] = TH1D(name, name, ranges["nocut"][var][0], ranges["nocut"][var][1], ranges["nocut"][var][2])
        #histograms[c+var][jt].SetDirectory(0)
        histograms[c+var+jt].Sumw2()
    name = "qcd__%s__%s__%s__%s__%s" % (channel, var, "alljt", iso, dataset_name)
    histograms[c+var+"alljt"] = TH1D(name, name, ranges["nocut"][var][0], ranges["nocut"][var][1], ranges["nocut"][var][2])
    #histograms[c+var][jt].SetDirectory(0)
    histograms[c+var+"alljt"].Sumw2()                

extra_data = {}
i=-1
for event in events2:
    i+=1
    #extra_data[i] = [event.bdt_qcd, event.bdt_sig_bg, event.xsweight, event.wjets_ct_shape_weight, event.wjets_fl_yield_weight]
    try:
        extra_data[i] = [event.xsweight, event.wjets_ct_shape_weight, event.wjets_fl_yield_weight, event.bdt_sig_bg, event.bdt_qcd,  event.bdt_qcd_reproc, event.bdt_qcd_mixed, event.bdt_sig_bg_old]
    except AttributeError:
        if i>0:
            print "Error", added_filename
            sys.exit(1)
    #print extra_data[i]

i=-1
missing = 0
for event in events:
    i+=1
    #if i not in extra_data: continue
    if not passes_cuts(event, channel, iso, iso_var=""): continue
    #run = event.run
    #lumi = event.lumi
    #eventid = event.event    
    
    #f not run in outdata[channel]: continue
    #f not lumi in outdata[channel][run]: continue
    #f not eventid in outdata[channel][run][lumi]: continue

    xsweight = extra_data[i][0]
    wjets_shape_weight = extra_data[i][1]
    wjets_yield_weight = extra_data[i][2]
    #xsweight = 1.
    #wjets_shape_weight = 1.
    #wjets_yield_weight = 1.
    #print dataset, xsweight

    jt = "%sj%st" % (event.njets, event.ntags)
    
    if math.isnan(event.b_weight): 
        event.b_weight = 1
    #total_weight = event.pu_weight * wjets_shape_weight * wjets_yield_weight * xsweight
    total_weight = event.pu_weight * event.lepton_weight__id * event.lepton_weight__iso * event.lepton_weight__trigger \
             * wjets_shape_weight * wjets_yield_weight * xsweight
    if math.isnan(event.b_weight * event.top_weight * event.pu_weight * event.lepton_weight__id * event.lepton_weight__iso * event.lepton_weight__trigger * wjets_shape_weight * wjets_yield_weight * xsweight):
        print "NAN", dataset, event.b_weight, event.top_weight, event.pu_weight, event.lepton_weight__id, event.lepton_weight__iso, event.lepton_weight__trigger, wjets_shape_weight, wjets_yield_weight, xsweight
    if event.top_weight > 0:
        total_weight *= event.top_weight
    #if not math.isnan(event.b_weight):
    #    total_weight *= event.b_weight
    
    total_weight *= luminosity
    
    if "Single" in dataset:
        total_weight = 1
    #print "weights", dataset, event.b_weight, event.top_weight, event.pu_weight, event.lepton_weight__id, event.lepton_weight__iso, event.lepton_weight__trigger, wjets_shape_weight, wjets_yield_weight, xsweight, luminosity
    
    bdt_vars["met"][0] = event.met
    bdt_vars["isotropy"][0] = event.isotropy
    bdt_vars["top_mass"][0] = event.top_mass
    
    if channel == "mu":
        bdt_vars["mu_mtw"][0] = event.mtw
        bdt_vars["ljet_pt"][0] = event.ljet_pt
        bdt_vars["ljet_mass"][0] = event.ljet_mass
    
    if channel == "ele":
        bdt_vars["bjet_pt"][0] = event.bjet_pt
        #bdt_vars["top_eta"][0] = event.top_eta
        #bdt_vars["ele_mtw"][0] = event.mtw
    
    event_vars = {}
    event_vars["qcd_mva"] = reader.EvaluateMVA("MVA_BDT")
    event_vars["met"] = event.met
    event_vars["mtw"] = event.mtw

    print extra_data[i][4], event_vars["qcd_mva"], extra_data[i] 
    event_vars["qcd_mva"] = extra_data[i][4]
    if event_vars["qcd_mva"] < qcd_mva_cut: continue
    if event.njets != 2: continue
    if event.ntags != 1: continue
    for v in event_vars:
        if event.njets < 4 and event.njets >= 2:
            histograms[c+v+jt].Fill(event_vars[v], total_weight)
        histograms[c+v+"alljt"].Fill(event_vars[v], total_weight)
        


print "writing"

outfilename = os.path.join(os.environ["STPOL_DIR"], "src/qcd_ntuples/yield_histos/",  channel , "histos_%s_%s_%s_%s.root" % (dataset, channel, iso, counter))

#outfilename = os.path.join("/scratch/andres/qcd/histos",  channel , "histos_%s_%s_%s_%s.root" % (dataset, channel, iso, counter))
#outfilename = os.path.join("/hdfs/local/andres/stpol/qcd/histos/", channel , "histos_%s_%s_%s_%s.root" % (dataset, channel, iso, counter))
print outfilename
outfile = TFile(outfilename, "RECREATE")
outfile.cd() 

for h in histograms.values():
    h.Write()
    
outfile.Write()
outfile.Close()

#for f in ROOT.gROOT.GetListOfFiles():
#    f.Close("R")
    
print "finished"             

        
