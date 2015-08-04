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
iso = sys.argv[4]
base_filename = sys.argv[5]
added_filename = sys.argv[6]

ROOT.TH1.AddDirectory(False)


variables = ["met", "mtw", 
    "lepton_pt", "lepton_eta", "lepton_iso", "lepton_phi", "bjet_pt", "bjet_eta", "bjet_mass", "bjet_bd_b",
    "bjet_phi", "bjet_dr", "bjet_pumva", "ljet_pt", "ljet_eta", "ljet_mass", "ljet_bd_b", "ljet_phi", "ljet_dr", "ljet_pumva",
    "sjet1_pt", "sjet1_eta", "sjet1_bd", "sjet2_pt", "sjet2_eta", "sjet2_bd", "cos_theta_lj", "cos_theta_bl", "cos_theta_whel_lj", 
    "met_phi", "C", "D", "circularity", "sphericity", "isotropy", "aplanarity", "thrust", "C_with_nu", "top_mass", "top_pt",
    "top_eta", "top_phi", "w_mass", "w_pt", "w_eta", "w_phi", "jet_cls", "hadronic_pt", "hadronic_eta", "hadronic_phi", "hadronic_mass",
    "shat_pt", "shat_eta", "shat_phi", "shat_mass", "shat", "ht", "lepton_met_dr", "ljet_met_dr", "bjet_met_dr", "sjet1_met_dr", "sjet2_met_dr", "lepton_met_dphi", "ljet_dphi", "bjet_dphi", "jet1_met_dphi", "jet2_met_dphi", "ljet_met_dphi", "bjet_met_dphi"
]

#variables = ["mtw", "cos_theta_lj"] 


"""ROOT.TMVA.Tools.Instance()
reader = ROOT.TMVA.Reader( "Color:!Silent" )
reader_old = ROOT.TMVA.Reader( "Color:!Silent" )

bdt_varlist = get_fixed(channel)
bdt_vars={}
for bv in bdt_varlist:
    bdt_vars[bv] = array('f',[0])
    reader.AddVariable(bv,bdt_vars[bv])

bdt_varlist_old = get_fixed(channel, old = True)
bdt_vars_old={}
for bv in bdt_varlist_old:
    bdt_vars_old[bv] = array('f',[0])
    reader_old.AddVariable(bv,bdt_vars_old[bv])


dirname = os.environ["STPOL_DIR"]+"/src/qcd_mva/weights/"
prefix_old = "anti_QCD_MVA_07_04"
#prefix = "anti_QCD_MVA_24_09"
#prefix2 = "MVA_BDT_AN_BDT_from_AN"
#prefix = "anti_QCD_MVA_28Nov"
#prefix2 = "MVA_BDT_AN_BDT_from_AN"
#reader.BookMVA( "MVA_BDT", dirname+prefix+"_qcdBDT_"+channel+".weights.xml" )
reader.BookMVA( "MVA_BDT", dirname+prefix_old+"_final2_"+channel+".weights.xml" )
#reader.BookMVA( "MVA_BDT", dirname+prefix+"_test_final2_withmtw_"+channel+".weights.xml" )
#reader.BookMVA( "MVA_BDT", dirname+prefix+"_test_final2_"+channel+".weights.xml" )
#reader.BookMVA( "MVA_BDT", dirname+prefix+"_final2_"+channel+".weights.xml" )
#reader2.BookMVA( "BDT_from_AN", dirname+prefix2+"_"+channel+".weights.xml" )
#reader.BookMVA( "MVA_BDT", dirname+prefix+"_qcdBDT_"+channel+".weights.xml" )
"""
qcd_mva_cut = -0.15
#qcd_mva_cut = 0.10
if channel == "ele":
    qcd_mva_cut = 0.15
    #qcd_mva_cut = 0.25

###
#qcd_mva_cut = 0.0

#range_cuts = ["nocut", "reversecut", "qcdcut", "qcdcut_new", "bdtcut_old", "bdtcut"]
range_cuts = ["nocut", "reversecut", "qcdcut", "bdtcut"]
cut_points = {"qcd_mva": qcd_mva_cut,
    "mtw": 50, "met": 45}

ranges = {}
ranges["qcd_mva"] = (40, -1, 1)
ranges["qcd_mva_new"] = (40, -1, 1)
ranges["qcd_mva_mixed"] = (40, -1, 1)
ranges["met"] = (40, 0, 200)
ranges["mtw"] = (40, 0, 200)
ranges["bdt_sig_bg"] = (40, -1, 1)
ranges["bdt_sig_bg_old"] = (40, -1, 1)
ranges["lepton_pt"] = (40,0,100)
ranges["lepton_eta"] = (40,-4,4) 
ranges["lepton_iso"] = (40,0,0.5) 
ranges["lepton_phi"] = (40,-3.14,3.14) 
ranges["bjet_pt"] = (40,0,200) 
ranges["bjet_eta"] = (40,-4,4) 
ranges["bjet_mass"] = (40,0,40)
ranges["bjet_bd_b"] = (40, -1, 1)
ranges["bjet_phi"] = (40,-3.14,3.14) 
ranges["bjet_dr"] = (40,0,5) 
ranges["bjet_pumva"] = (40,0.5,1) 
ranges["ljet_pt"] = (40,0,300) 
ranges["ljet_eta"] = (40,-6,6) 
ranges["ljet_mass"] = (40,0,60) 
ranges["ljet_bd_b"] = (40,-1,1)
ranges["ljet_phi"] = (40,-3.14,3.14) 
ranges["ljet_dr"] = (40,0,6) 
ranges["ljet_pumva"] = (40,-1,1)
ranges["sjet1_pt"] = (40,0,600) 
ranges["sjet1_eta"] = (40,-6,6) 
ranges["sjet1_bd"] = (40,-1,1) 
ranges["sjet2_pt"] = (40,0,600) 
ranges["sjet2_eta"] = (40,-6,6) 
ranges["sjet2_bd"] = (40,-1,1) 
ranges["cos_theta_lj"] = (40,-1,1) 
ranges["cos_theta_whel_lj"] = (40,-1,1) 
ranges["cos_theta_bl"] = (40,-1,1)
ranges["met_phi"] = (40,-3.14,3.14) 
ranges["C"] = (40,0,1) 
ranges["D"] = (40,0,1) 
ranges["circularity"] = (40,0,1) 
ranges["sphericity"] = (40,0,1) 
ranges["isotropy"] = (40,0,1) 
ranges["aplanarity"] = (40,0,1) 
ranges["thrust"] = (40,0,1) 
ranges["C_with_nu"] = (40,0,1) 
ranges["top_mass"] = (40,100,500) 
ranges["top_pt"] = (40,0,300) 
ranges["top_eta"] = (40,-6,6) 
ranges["top_phi"] = (40,-3.14,3.14)  
ranges["w_mass"] = (40,79,82) 
ranges["w_pt"] = (40,0,200)  
ranges["w_eta"] = (40,-6,6) 
ranges["w_phi"] = (40,-3.14,3.14)  
ranges["jet_cls"] = (20,-0.5,19.5)  
ranges["hadronic_pt"] = (40,0,250)  
ranges["hadronic_eta"] = (40,-6,6) 
ranges["hadronic_phi"] = (40,-3.14,3.14)  
ranges["hadronic_mass"] = (40,0,1000) 
ranges["shat_pt"] = (40,0,150) 
ranges["shat_eta"] = (40,-6,6)  
ranges["shat_phi"] = (40,-3.14,3.14)  
ranges["shat_mass"] = (40,0,1200)  
ranges["shat"] = (40,0,1500) 
ranges["ht"] = (40,0,600) 
ranges["lepton_met_dr"] = (60,0,6)
ranges["bjet_met_dr"] = (60,0,6)
ranges["ljet_met_dr"] = (60,0,6)
ranges["sjet1_met_dr"] = (60,0,6)
ranges["sjet2_met_dr"] = (60,0,6)

ranges["lepton_met_dphi"] = (40, -4, 4)
ranges["jet1_met_dphi"] = (40, -4, 4)
ranges["jet2_met_dphi"] = (40, -4, 4)
ranges["ljet_met_dphi"] = (40, -4, 4)
ranges["bjet_met_dphi"] = (40, -4, 4)
ranges["ljet_dphi"] = (40, -4, 4)
ranges["bjet_dphi"] = (40, -4, 4)



jettag = ["2j1t", "2j0t", "3j1t", "3j2t"]

infile =  TFile.Open(base_filename, "read")
infile2 =  TFile.Open(added_filename, "read")

events = infile.Get('dataframe')
events2 = infile2.Get('dataframe')

colnames = [ "xsweight", "wjets_ct_shape_weight", "wjets_fl_yield_weight"]

histograms = dict()

c = channel

luminosity = 19670
if channel == "ele":
    luminosity = 19637
#luminosity = 19700

for var in ranges.keys():
    #if var not in variables and "qcd_mva" not in var and "bdt" not in var: continue
    for jt in jettag:
        for cut in range_cuts:
            #histograms[c][var][jt] = dict()
            dataset_name = dataset
            if dataset.startswith("Single"):
                dataset_name = "data"
            elif dataset.startswith("QCD"):
                dataset_name = "QCD"
            name = "histo__%s__%s__%s__%s__%s__%s" % (cut, channel, var, jt, iso, dataset_name)
            histograms[c+var+jt+cut] = TH1D(name, name, ranges[var][0], ranges[var][1], ranges[var][2])
            #histograms[c+var][jt].SetDirectory(0)
            histograms[c+var+jt+cut].Sumw2()        

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
    #run = event.run
    #lumi = event.lumi
    #eventid = event.event    

    #f not run in outdata[channel]: continue
    #f not lumi in outdata[channel][run]: continue
    #f not eventid in outdata[channel][run][lumi]: continue

    xsweight = extra_data[i][0]
    wjets_shape_weight = extra_data[i][1]
    wjets_yield_weight = extra_data[i][2]
    wjets_pt_weight = extra_data[i][5]

    jt = "%sj%st" % (event.njets, event.ntags)
    

    #if math.isnan(event.b_weight): 
    #    event.b_weight = 1
    #total_weight = event.pu_weight * wjets_shape_weight * xsweight
    total_weight = event.pu_weight * event.lepton_weight__id * event.lepton_weight__iso * event.lepton_weight__trigger \
             * wjets_shape_weight * xsweight
    if math.isnan(event.b_weight * event.top_weight * event.pu_weight * event.lepton_weight__id * event.lepton_weight__iso * event.lepton_weight__trigger * wjets_shape_weight * xsweight):
        print "NAN", dataset, event.b_weight, event.top_weight, event.pu_weight, event.lepton_weight__id, event.lepton_weight__iso, event.lepton_weight__trigger, wjets_shape_weight, xsweight
        nan_events += 1
    if event.top_weight > 0:
        total_weight *= event.top_weight
    #if not math.isnan(event.b_weight):
    total_weight *= event.b_weight
    total_weight *= wjets_pt_weight
    total_weight *= luminosity

    if math.isnan(total_weight): continue
    
    
    #if total_weight == 0:
    #    continue

    if "Single" in dataset:
        total_weight = 1

    #for bdtvar in bdt_vars:
    #    bdt_vars[bdtvar][0] = val = getattr(event, bdtvar.replace("mu_mtw", "mtw"))

    event_vars = {}
    #event_vars["qcd_mva"] = reader.EvaluateMVA("MVA_BDT")
    event_vars["qcd_mva"] = extra_data[i][4]
    #event_vars["qcd_mva_new"] = extra_data[i][5]
    #event_vars["qcd_mva_mixed"] = extra_data[i][6]
    event_vars["bdt_sig_bg"] = extra_data[i][3]
    #event_vars["bdt_sig_bg_old"] = extra_data[i][7]
    for var in variables:    
        event_vars[var] = getattr(event, var)
    

    for v in event_vars:
        #if bdt_sig_bg in v and event_vars[v] > 0.2 and "Single" in dataset and event.njets==2 and event.ntags == 1: continue
        histograms[c+v+jt+"nocut"].Fill(event_vars[v], total_weight)
        if event_vars["qcd_mva"] > cut_points["qcd_mva"]:
            histograms[channel+v+jt+"qcdcut"].Fill(event_vars[v], total_weight)
            if event_vars["bdt_sig_bg"] > 0.45:
                histograms[channel+v+jt+"bdtcut"].Fill(event_vars[v], total_weight)
            #if event_vars["bdt_sig_bg_old"] > 0.6:
            #    histograms[channel+v+jt+"bdtcut_old"].Fill(event_vars[v], total_weight)
        else:
            histograms[channel+v+jt+"reversecut"].Fill(event_vars[v], total_weight)
        #if event_vars["qcd_mva_new"] > cut_points["qcd_mva_new"]:
        #    histograms[channel+v+jt+"qcdcut_new"].Fill(event_vars[v], total_weight)
        

print "writing"
print "total events:", total_events, " nans:", nan_events
outfilename = os.path.join(os.environ["STPOL_DIR"], "src/qcd_ntuples/var_histos/",  channel , "histos_%s_%s_%s_%s.root" % (dataset, channel, iso, counter))

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

        
