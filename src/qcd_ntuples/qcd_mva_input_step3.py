import sys
import os
from array import array
import math

#Monkey-patch the system path to import the stpol header
sys.path.append(os.path.join(os.environ["STPOL_DIR"], "src/headers"))
from stpol import stpol, list_methods

import ROOT
from ROOT import TFile
from DataFormats.FWLite import Events, Handle, Lumis
from utils import *

print "args", sys.argv[0], sys.argv[1]
#system.exit(1)
dataset = sys.argv[1]
iso = sys.argv[2]
counter = sys.argv[3]
filename = sys.argv[4]

outfiles = {}
linenumber = {}
if not "SingleEle" in dataset:
    outfiles["mu_2j1t"] = open(os.path.join(os.environ["STPOL_DIR"], "src", "qcd_ntuples", "mva_input_step3", dataset+"_"+iso+"_mu_2j1t_" + counter + ".txt"), "w")
    outfiles["mu_2j0t"] = open(os.path.join(os.environ["STPOL_DIR"], "src", "qcd_ntuples", "mva_input_step3", dataset+"_"+iso+"_mu_2j0t_" + counter + ".txt"), "w")
    linenumber["mu_2j1t"] = 1
    linenumber["mu_2j0t"] = 1
if not "SingleMu" in dataset:
    outfiles["ele_2j1t"] = open(os.path.join(os.environ["STPOL_DIR"], "src", "qcd_ntuples", "mva_input_step3", dataset+"_"+iso+"_ele_2j1t_" + counter + ".txt"), "w")
    outfiles["ele_2j0t"] = open(os.path.join(os.environ["STPOL_DIR"], "src", "qcd_ntuples", "mva_input_step3", dataset+"_"+iso+"_ele_2j0t_" + counter + ".txt"), "w")
    linenumber["ele_2j1t"] = 1
    linenumber["ele_2j0t"] = 1

variables = ["lepton_pt", "lepton_eta", "lepton_iso", "lepton_phi", 
    #"hlt", "hlt_mu", "hlt_ele", 
    "bjet_pt", "bjet_eta", "bjet_mass", "bjet_bd_b", "bjet_phi", "bjet_dr", "bjet_pumva",
    "ljet_pt", "ljet_eta", "ljet_mass", "ljet_bd_b", "ljet_phi", "ljet_dr", "ljet_pumva",
    "sjet1_pt", "sjet1_eta", "sjet1_bd", "sjet2_pt", "sjet2_eta", "sjet2_bd", 
    #"cos_theta_lj", "cos_theta_bl",
    "met", "mtw", "met_phi", "C", "D", "circularity", "sphericity", "isotropy", "aplanarity", "thrust", "C_with_nu",
    "top_mass", "top_pt", "top_eta", "top_phi", "w_mass", "w_pt", "w_eta", "w_phi",
    "jet_cls", "hadronic_pt", "hadronic_eta", "hadronic_phi", "hadronic_mass",
    "shat_pt", "shat_eta", "shat_phi", "shat_mass", "shat", "ht", "nu_soltype",
    #"n_signal_mu", "n_signal_ele", "n_veto_mu", "n_veto_ele", 
    "n_good_vertices",
    "pu_weight", "lepton_weight__id", "lepton_weight__iso", "lepton_weight__trigger", "gen_weight",
    "top_weight", "b_weight",
    #"run", "lumi", "event", 
    "xs"
]


int_vars = [#"hlt", "hlt_mu", "hlt_ele", 
    "jet_cls", "n_good_vertices"]



for name, of in outfiles.items():
    line = "linenr/I:"+int_vars[0] +  "/I:"
    for i in range(1, len(int_vars)):
        line += int_vars[i] + ":"
    line += variables[0] + "/D:"
    for i in range(1, len(variables)-1):
        if variables[i] in int_vars: continue
        line += variables[i] + ":"
    line += variables[len(variables)-1]
    of.write(line + "\n")

infile =  TFile.Open(filename, "read")
events = infile.Get('dataframe')
channel = ""

c1 = 0
c2 = 0
c3 = 0
c4 = 0
c5 = 0
for event in events:
    c1 += 1
    if event.hlt_mu == 1 and event.n_signal_mu == 1:
        channel = "mu"
    elif event.hlt_ele == 1 and event.n_signal_ele == 1:
        channel = "ele"
    else:
        continue
    #print event.hlt_mu, event.n_signal_mu, event.hlt_ele, event.n_signal_ele, dataset, channel
    if not (event.n_veto_mu == 0 and event.n_veto_ele == 0): continue
    c2 += 1
    if event.njets != 2: continue
    if event.ntags != 0 and event.ntags != 1: continue
    c3 += 1
    line = ""
    if channel == "mu" and "SingleEle" in dataset: continue        
    if channel == "ele" and "SingleMu" in dataset: continue
    line += str(linenumber["%s_%dj%dt" % (channel, event.njets, event.ntags)]) + " "
    for var in int_vars:
        val = getattr(event, var)
        line += str(val) + " "
    for var in variables:
        if var in int_vars: continue
        val = getattr(event, var)
        if var in ["lepton_weight__id", "lepton_weight__trigger"] and channel == "ele":
            val = 1.
        if "Single" in dataset and var in ["pu_weight", "lepton_weight__id", "lepton_weight__iso", "lepton_weight__trigger", "b_weight", "xs"]:
            val = 1.
        line += str(val) + " "
    line += "\n"
    c4 += 1    
    #print event.b_weight
    if math.isnan(event.b_weight): continue
    if event.bjet_dr < 0.3 or event.ljet_dr < 0.3: continue
    c5 += 1
    linenumber["%s_%dj%dt" % (channel, event.njets, event.ntags)] += 1
    outfiles["%s_%dj%dt" % (channel, event.njets, event.ntags)].write(line) 

print "BEE", c1, c2, c3, c4, c5
print "TSEE", c5
for of in outfiles.values():
    of.close()
print "finished"
