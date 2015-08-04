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
counter = sys.argv[2]
base_filename = sys.argv[3]
added_filename = sys.argv[4]

SIGNAL_BDT_CUT = 0.45

infile =  TFile.Open(base_filename, "read")
infile2 = TFile.Open(added_filename, "read")

events = infile.Get('dataframe')
events2 = infile2.Get('dataframe')

extra_data = {}
                
i=-1
for event in events2:
    i+=1
    #if not selection == "loose":
    #    if event.bdt_qcd <= -0.15: continue
    extra_data[i] = [event.bdt_qcd, event.bdt_sig_bg]

i=-1

missing_present = 0

missing = 0
outdata = {}
outdatai = {}
channels = ["mu", "ele"]
for selection in ["preqcd", "preselection", "final"]:
    outdata[selection] = {}
    outdatai[selection] = {}
    for channel in channels:
        outdata[selection][channel] = {}
        outdatai[selection][channel] = {}

for event in events:
    i+=1
    if not i in extra_data: continue
    
    if event.njets == 2: 
        if event.ntags > 1: continue
    elif event.njets == 3:
        if event.ntags > 2: continue
        if event.ntags < 1: continue
    else: continue
    jt = "%sj%st" % (event.njets, event.ntags)    

    if event.n_signal_mu == 1 and abs(event.lepton_type) == 13:
        channel = "mu"
    elif event.n_signal_ele == 1 and abs(event.lepton_type) == 11:
        channel = "ele"
    else: continue

    if event.n_veto_mu > 0 or event.n_veto_ele > 0: continue

    if event.bjet_pt <= 40 or event.ljet_pt <= 40: continue
    if abs(event.bjet_eta) >= 4.5 or abs(event.ljet_eta) >= 4.5: continue
    if channel == "mu" and event.lepton_pt <= 26: continue
    if channel == "ele" and event.lepton_pt <= 30: continue
    if channel == "mu" and event.hlt_mu != 1: continue
    if channel == "ele" and event.hlt_ele != 1: continue
    if event.bjet_dr <= 0.3 or event.ljet_pt <= 0.3: continue
    qcd_mva_cut = -0.15
    if channel == "ele":
        qcd_mva_cut = 0.15
    
    run = event.run
    lumi = event.lumi
    eventid = event.event    

    if math.isnan(event.lepton_weight__id): continue
    if math.isnan(event.lepton_weight__iso): continue
    if math.isnan(event.lepton_weight__trigger): continue
    if math.isnan(event.b_weight): continue

    outdatai["preqcd"][channel][i] = True
    if run not in outdata["preselection"][channel]:
        outdata["preqcd"][channel][run] = dict()
    if lumi not in outdata["preqcd"][channel][run]:
        outdata["preqcd"][channel][run][lumi] = dict()
    outdata["preqcd"][channel][run][lumi][eventid] = True

    qcd_bdt = extra_data[i][0]
    if qcd_bdt <= qcd_mva_cut: continue    

    outdatai["preselection"][channel][i] = True
    if run not in outdata["preselection"][channel]:
        outdata["preselection"][channel][run] = dict()
    if lumi not in outdata["preselection"][channel][run]:
        outdata["preselection"][channel][run][lumi] = dict()
    outdata["preselection"][channel][run][lumi][eventid] = True
    
    signal_bdt = extra_data[i][1]
    if signal_bdt <= SIGNAL_BDT_CUT: continue    

    outdatai["final"][channel][i] = True
    if run not in outdata["final"][channel]:
        outdata["final"][channel][run] = dict()
    if lumi not in outdata["final"][channel][run]:
        outdata["final"][channel][run][lumi] = dict()
    outdata["final"][channel][run][lumi][eventid] = True

print "missing present", missing_present
print "writing"
path = os.path.join(os.environ["STPOL_DIR"], "src", "pdf_uncertainties", "eventlists")

outfilename = "%s/events_%s_%s.pkl" % (path, dataset, counter)
outfile = open(outfilename, "wb")    
pickle.dump(outdata, outfile)    
pickle.dump(outdatai, outfile)    
outfile.close()

print "finished"
