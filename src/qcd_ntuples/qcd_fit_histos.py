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

CT_BIN = False
BDT_BIN = False
BIN = 6

print "args", sys.argv
channel = sys.argv[1]
dataset = sys.argv[2]
counter = sys.argv[3]
iso = sys.argv[4]
isovar = sys.argv[7]
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
#prefix = "anti_QCD_MVA_07_04"
prefix = "anti_QCD_MVA_27Jan_fullData"
#prefix2 = "MVA_BDT_AN_BDT_from_AN"
#reader.BookMVA( "MVA_BDT", dirname+prefix+"_final2_"+channel+".weights.xml" )
reader.BookMVA( "MVA_BDT", dirname+prefix+"_qcdBDT_"+channel+".weights.xml" )
#reader.BookMVA( "MVA_BDT", dirname+prefix+"_test_final2_withmtw_"+channel+".weights.xml" )
#reader2.BookMVA( "BDT_from_AN", dirname+prefix2+"_"+channel+".weights.xml" )


qcd_mva_cut = -0.15
if channel == "ele":
    qcd_mva_cut = 0.15

range_cuts = ["nocut", "reversecut", "qcdcut"]
cut_points = {"qcd_mva": qcd_mva_cut,
    "mtw": 50, "met": 45}

ranges = {}
ranges["reversecut"] = {}
ranges["reversecut"]["qcd_mva"] = (20, -1, qcd_mva_cut)
#ranges["reversecut"]["qcd_mva_deltaR"] = (20, -1, qcd_mva_cut_deltaR)
ranges["reversecut"]["met"] = (9, 0, 45)
ranges["reversecut"]["mtw"] = (10, 0, 50)
ranges["qcdcut"] = {}
ranges["qcdcut"]["qcd_mva"] = (20, qcd_mva_cut, 1)
#ranges["qcdcut"]["qcd_mva_deltaR"] = (20, qcd_mva_cut_deltaR, 1)
ranges["qcdcut"]["met"] = (31, 45, 200)
ranges["qcdcut"]["mtw"] = (30, 50, 200)    
ranges["nocut"] = {}
ranges["nocut"]["qcd_mva"] = (40, -1, 1)
#ranges["nocut"]["qcd_mva_deltaR"] = (40, -1, 1)
ranges["nocut"]["met"] = (40, 0, 200)
ranges["nocut"]["mtw"] = (40, 0, 200)

jettag = ["2j1t", "2j0t", "3j1t", "3j2t"]

infile =  TFile.Open(base_filename, "read")
infile2 =  TFile.Open(added_filename, "read")

print base_filename, added_filename

events = infile.Get('dataframe')
events2 = infile2.Get('dataframe')

colnames = [ "xsweight", "wjets_ct_shape_weight", "wjets_fl_yield_weight"]

histograms = dict()

c = channel

#luminosity  = 19764
luminosity = 19670
if channel == "ele":
    luminosity = 19637

for var in variables:
    for jt in jettag:
        for cut in range_cuts:
            #histograms[c][var][jt] = dict()
            dataset_name = dataset
            if dataset.startswith("Single"):
                dataset_name = "data"
            elif dataset.startswith("QCD"):
                dataset_name = "QCD"
            name = "qcd__%s__%s__%s__%s__%s__%s" % (cut, channel, var, jt, iso, dataset_name)
            if isovar != None and isovar != "None":
                name += "__isovar__" + isovar
            histograms[c+var+jt+cut] = TH1D(name, name, ranges[cut][var][0], ranges[cut][var][1], ranges[cut][var][2])
            #histograms[c+var][jt].SetDirectory(0)
            histograms[c+var+jt+cut].Sumw2()        
"""                         
path = os.path.join("/hdfs/local/andres/stpol/qcd", "eventlists")
picklename = "%s/events_%s_%s_%s_%s.pkl" % (path, channel, dataset, iso, counter)
with open(picklename, 'rb') as f:
    outdata = pickle.load(f)
    #outdatai = pickle.load(f)
"""
extra_data = {}
i=-1
for event in events2:
    i+=1
    #extra_data[i] = [event.bdt_qcd, event.bdt_sig_bg, event.xsweight, event.wjets_ct_shape_weight, event.wjets_fl_yield_weight]
    extra_data[i] = [event.xsweight, event.wjets_ct_shape_weight, event.wjets_fl_yield_weight, event.bdt_qcd, event.bdt_sig_bg, event.wjets_pt_weight]
    #print extra_data[i]

i=-1
missing = 0
asd = 0
for event in events:
    i+=1
    if i not in extra_data: continue
    if not passes_cuts(event, channel, iso, isovar): continue
    if CT_BIN == True:    
        if not cos_theta_bin(event.cos_theta_lj, BIN):
            continue
        else: asd += 1
    elif BDT_BIN == True:    
        if not cos_theta_bin(extra_data[i][4], BIN):
            continue
        else: asd += 1
    
    #run = event.run
    #lumi = event.lumi
    #eventid = event.event    

    #f not run in outdata[channel]: continue
    #f not lumi in outdata[channel][run]: continue
    #f not eventid in outdata[channel][run][lumi]: continue

    xsweight = extra_data[i][0]
    wjets_shape_weight = extra_data[i][1]
    wjets_pt_weight = extra_data[i][5]
    #wjets_yield_weight = extra_data[i][2]
    #print dataset, xsweight
    jt = "%sj%st" % (event.njets, event.ntags)
    
    if math.isnan(event.b_weight): 
        event.b_weight = 1
    total_weight = event.pu_weight * wjets_shape_weight * xsweight
    #total_weight = event.pu_weight * event.lepton_weight__id * event.lepton_weight__iso * event.lepton_weight__trigger \
    #         * wjets_shape * wjets_yield * xsweight
    if math.isnan(event.b_weight * event.top_weight * event.pu_weight * event.lepton_weight__id * event.lepton_weight__iso * event.lepton_weight__trigger * wjets_shape_weight * xsweight):
        print "NAN", dataset, event.b_weight, event.top_weight, event.pu_weight, event.lepton_weight__id, event.lepton_weight__iso, event.lepton_weight__trigger, wjets_shape_weight, xsweight
    if event.top_weight > 0:
        total_weight *= event.top_weight
    if not math.isnan(event.b_weight):
        total_weight *= event.b_weight
    total_weight *= wjets_pt_weight
    total_weight *= luminosity
    
    
    if "Single" in dataset:
        total_weight = 1
    #print "weights", dataset, event.b_weight, event.top_weight, event.pu_weight, event.lepton_weight__id, event.lepton_weight__iso, event.lepton_weight__trigger, wjets_shape_weight, wjets_yield_weight, xsweight, luminosity
    
    bdt_vars["met"][0] = event.met
    bdt_vars["isotropy"][0] = event.isotropy
    bdt_vars["top_mass"][0] = event.top_mass
    
    if channel == "mu":
        bdt_vars["mtw"][0] = event.mtw
        bdt_vars["ljet_pt"][0] = event.ljet_pt
        #bdt_vars["ljet_mass"][0] = event.ljet_mass
    
    if channel == "ele":
        bdt_vars["bjet_pt"][0] = event.bjet_pt
        bdt_vars["top_eta"][0] = event.top_eta
        #bdt_vars["ele_mtw"][0] = event.mtw

    #print "iso", event.lepton_iso
    event_vars = {}
    event_vars["qcd_mva"] = reader.EvaluateMVA("MVA_BDT")
    #event_vars["qcd_mva_deltaR"] = extra_data[i][4]
    event_vars["met"] = event.met
    event_vars["mtw"] = event.mtw
    if extra_data[i][3] - event_vars["qcd_mva"] > 0.00001:
        print "ALARM", extra_data[i][3], event_vars["qcd_mva"]
    if abs(event.bjet_eta) >= 4.5 or abs(event.ljet_eta) >= 4.5: print "JAMA", dataset, iso, channel, event_vars["qcd_mva"], extra_data[i][4]
    if abs(event.bjet_eta) >= 4.5 or abs(event.ljet_eta) >= 4.5 and event_vars["qcd_mva"] > qcd_mva_cut: print "JA_MA", dataset, iso, channel, event_vars["qcd_mva"], extra_data[i][4]    
    if abs(event.bjet_eta) >= 4.5 or abs(event.ljet_eta) >= 4.5 and event_vars["qcd_mva"] > qcd_mva_cut and extra_data[i][4] > 0.6 : print "JA__MA", dataset, iso, channel, event_vars["qcd_mva"], extra_data[i][4]    



    for v in event_vars:
        histograms[c+v+jt+"nocut"].Fill(event_vars[v], total_weight)
        if event_vars[v] > cut_points[v]:
            histograms[channel+v+jt+"qcdcut"].Fill(event_vars[v], total_weight)
        else:
            histograms[channel+v+jt+"reversecut"].Fill(event_vars[v], total_weight)

print "EVENTS", channel, histograms[channel+"qcd_mva2j1tnocut"].GetEntries(), histograms[channel+"qcd_mva2j1tnocut"].Integral()

print "writing"

isovardesc = ""
if iso == "antiiso" and (isovar != None and isovar != "None"):
    isovardesc = "_isovar_" + isovar
outfilename = os.path.join(os.environ["STPOL_DIR"], "src/qcd_ntuples/histos/",  channel , "histos_%s_%s_%s%s_%s.root" % (dataset, channel, iso, isovardesc, counter))

if CT_BIN == True:
    outfilename = os.path.join(os.environ["STPOL_DIR"], "src/qcd_ntuples/histos_bin%d/" % BIN,  channel , "histos_%s_%s_%s%s_%s.root" % (dataset, channel, iso, isovardesc, counter))
elif BDT_BIN == True:
    outfilename = os.path.join(os.environ["STPOL_DIR"], "src/qcd_ntuples/histos_bdtbin%d/" % BIN,  channel , "histos_%s_%s_%s%s_%s.root" % (dataset, channel, iso, isovardesc, counter))

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

print asd
print "finished"             

        
