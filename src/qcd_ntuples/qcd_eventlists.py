import sys
import os
from array import array
from time import gmtime, strftime
import math
#Monkey-patch the system path to import the stpol header
#sys.path.append(os.path.join(os.environ["STPOL_DIR"], "src/headers"))
#from stpol import stpol, list_methods

import ROOT
from ROOT import TH1D, TFile
#import TMVA
# prepare the FWLite autoloading mechanism
ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()
from PhysicsTools.PythonAnalysis import *
from DataFormats.FWLite import Events, Handle, Lumis

import pickle

print "args", sys.argv
#system.exit(1)
dataset = sys.argv[1]
iso = sys.argv[2]
counter = sys.argv[3]
base_filename = sys.argv[4]
added_filename = sys.argv[5]


infile =  TFile.Open(base_filename, "read")
infile2 = TFile.Open(added_filename, "read")

events = infile.Get('dataframe')
events2 = infile2.Get('dataframe')

#colnames = ["bdt_qcd", "bdt_sig_bg", "xsweight", "wjets_ct_shape_weight", "wjets_fl_yield_weight"]
colnames = ["xsweight", "wjets_ct_shape_weight", "wjets_fl_yield_weight"]
extra_data = {}
                
i=-1
for event in events2:
    i+=1
    #extra_data[i] = [event.bdt_qcd, event.bdt_sig_bg, event.xsweight, event.wjets_ct_shape_weight, event.wjets_fl_yield_weight]
    extra_data[i] = [event.xsweight, event.wjets_ct_shape_weight, event.wjets_fl_yield_weight]

i=-1

outdata = {}
outdata["mu"] = {}
outdata["ele"] = {}
outdatai = {}
outdatai["mu"] = {}
outdatai["ele"] = {}
channels = ["mu", "ele"]
for event in events:
    i+=1
    
    #if not i in extra_data: continue
    
    if event.njets == 2: 
        if event.ntags > 1: continue
    elif event.njets == 3:
        if event.ntags > 2: continue
        if event.ntags < 1: continue
    jt = "%sj%st" % (event.njets, event.ntags)    

    if event.n_signal_mu == 1:
        channel = "mu"
    elif event.n_signal_ele == 1:
        channel = "ele"
    else: continue

    if event.n_veto_mu > 0 or event.n_veto_ele > 0: continue

    if event.bjet_pt <= 40 or event.ljet_pt <= 40: continue
    if abs(event.bjet_eta) >= 4.5 or abs(event.ljet_eta) >= 4.5: continue
    if channel == "mu" and event.lepton_pt <= 26: continue
    if channel == "ele" and event.lepton_pt <= 30: continue
    if channel == "mu" and event.hlt_mu != 1: continue
    if channel == "ele" and event.hlt_ele != 1: continue
    if event.bjet_dr <= 0.3 or event.ljet_dr <= 0.3: continue
        
    run = event.run
    lumi = event.lumi
    eventid = event.event    

    if math.isnan(event.lepton_weight__id): continue
    if math.isnan(event.lepton_weight__iso): continue
    if math.isnan(event.lepton_weight__trigger): continue
    #if math.isnan(event.b_weight): continue
    outdatai[channel][i] = True
    if run not in outdata[channel]:
        outdata[channel][run] = dict()
    if lumi not in outdata[channel][run]:
        outdata[channel][run][lumi] = dict()
    outdata[channel][run][lumi][eventid] = True#extra_data[i]
    
print "writing"
#path = os.path.join(os.environ["STPOL_DIR"], "src", "qcd_ntuples", "eventlists")
path = os.path.join("/hdfs/local/andres/stpol/qcd", "eventlists")
for channel in channels:
    outfilename = "%s/events_%s_%s_%s_%s.pkl" % (path, channel, dataset, iso, counter)
    outfile = open(outfilename, "wb") 
    print outdata
    print outfilename
    pickle.dump(outdata, outfile, pickle.HIGHEST_PROTOCOL)
    pickle.dump(outdatai, outfile)    
    outfile.close()

print "finished"             

        
