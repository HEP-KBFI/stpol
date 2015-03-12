import sys
import os
from array import array
from time import gmtime, strftime
#Monkey-patch the system path to import the stpol header
sys.path.append(os.path.join(os.environ["STPOL_DIR"], "src/headers"))
from stpol import stpol, list_methods

import ROOT
from ROOT import TH1D, TFile
#import TMVA
# prepare the FWLite autoloading mechanism
ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()
from PhysicsTools.PythonAnalysis import *
from DataFormats.FWLite import Events, Handle, Lumis

from src.qcd_mva.utils import *
from src.qcd_mva.mva_variables import *
from Dataset import *


print "args", sys.argv[0], sys.argv[1]
#system.exit(1)
channel = sys.argv[1]
dataset = sys.argv[2]
counter = sys.argv[3]
iso = sys.argv[4]
syst = sys.argv[5]
cut = sys.argv[6]=="True"
reverse_cut = sys.argv[7]=="True"
#print sys.argv[5], cut
infile_list = sys.argv[8:]

print sys.argv[0:7]

qcd_mva_cut = 0.4
if channel == "ele":
    qcd_mva_cut = 0.55


ROOT.TMVA.Tools.Instance()
reader = ROOT.TMVA.Reader( "Color:!Silent" )
#reader2 = ROOT.TMVA.Reader( "Color:!Silent" )

varlist = get_fixed(channel)

ranges = {}
if not reverse_cut:
    ranges["qcd_mva"] = (40, -1, 1)
    ranges["met"] = (40, 0, 200)
    ranges[channel+"_mtw"] = (40, 0, 200)
else:
    ranges["qcd_mva"] = (20, -1, qcd_mva_cut)
    ranges["met"] = (20, 0, 45)
    ranges[channel+"_mtw"] = (20, 0, 50)


vars={}
for v in varlist:
    vars[v] = array('f',[0])

for v in varlist:
    reader.AddVariable(v,vars[v])
#for v in varlist_final:
    #reader2.AddVariable(v,vars[v])

#// Spectator variables declared in the training have to be added to the reader, too

cos_theta = array('f',[0])
cos_theta_bl = array('f',[0])
#reader.AddSpectator( "cos_theta", cos_theta )
#reader2.AddSpectator( "cos_theta", cos_theta )


filename = dataset
if "antiiso" in iso:
        filename += "_antiiso"
else:
        filename += "_iso"

filename += "_"+syst

docut = "nocut"
if cut == True:
    docut = "cut"
    if reverse_cut == True:
        docut = "reversecut"

values = {}
cut_values = {}
for jt in ["2j1t", "2j0t", "3j1t", "3j2t"]:
    values[jt] = {}
    cut_values[jt] = {}

for (name, dic) in values.items():
    for v in varlist:
        dic[v] = []
    dic["cos_theta"] = []
    dic["cos_theta_bl"] = []
    dic["qcd_mva"] = []
    dic["mva_bdt"] = []

histos = {}

"""for (name, dic) in cut_values.items():
    for v in varlist:
        dic[v] = []
    dic["cos_theta"] = []
"""


               
dirname = os.environ["STPOL_DIR"]+"/src/qcd_mva/weights/"
prefix = "anti_QCD_MVA_07_04"
prefix2 = "MVA_BDT_AN_BDT_from_AN"
#reader.BookMVA( "MVA_BDT", dirname+prefix+"_BDT_from_AN_"+channel+".weights.xml" )
reader.BookMVA( "MVA_BDT", dirname+prefix+"_final2_"+channel+".weights.xml" )
#reader.BookMVA( "MLPBNN", dirname+prefix+"_MLPBNN.weights.xml" )
#reader2.BookMVA( "BDT_from_AN", dirname+prefix2+"_"+channel+".weights.xml" )

cross_sections = read_cross_sections()

lumi = 19728
if channel == "mu":
    lumi = 19739 



    
#print "dir00 ", ROOT.gDirectory.pwd()
#mydir = ROOT.gDirectory.pwd()
outfilename = os.environ["STPOL_DIR"]+"/src/qcd_ntuples/histos/"+channel+"/qcdfit_"+docut+"_"+filename+"_"+counter+".root"

if True:
    #print file_list_file
    events = Events(infile_list)


    e = stpol.stable.event
    sigmu = stpol.stable.tchan.muon
    sigele = stpol.stable.tchan.electron

    if channel == "mu":
        siglepton = sigmu
    elif channel == "ele":
        siglepton = sigele

    bjet = stpol.stable.tchan.bjet
    ljet = stpol.stable.tchan.specjet1
    top = stpol.stable.tchan.top
    ffile = stpol.stable.file
    weight = stpol.stable.weights

    total_events = events.size()
    print "Total ev:",total_events
    if total_events < 1: sys.exit(0)
    
    """total_events = 0
    for f in infile_list:
        print strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print f, ffile.total_processed(f)
        total_events += ffile.total_processed(f)
    strftime("%Y-%m-%d %H:%M:%S", gmtime())    
    """
    outfile = TFile(outfilename, "RECREATE")
    #mydir = ROOT.gDirectory.GetDirectory(out"/home/andres/single_top/stpol/src/qcd_ntuples/histos/mu/histos_cut_T_tW_iso_0.root:/")
    #print "dir0 ", mydir, ROOT.gDirectory.pwd()
    #print mydir
    #system.exit(1)
    histovars = ["qcd_mva", "met"]
    
    if channel == "mu":
        histovars.extend([channel+"_mtw"])
    
    if "Down" in syst:
        sys = syst[:-4]
        ud = "Down"
        sysname = sys+"__"+ud
    elif "Up" in syst:
        sys = syst[:-2]
        ud = "Up"
        sysname = sys+"__"+ud
    else:
        sysname = syst        
    for varname in histovars:
        #print varname
        hr = ranges[varname]
        for jt in ["2j1t", "2j0t", "3j1t", "3j2t"]:
            #print "dir ", mydir#, ROOT.gDirectory.pwd()
            histo = TH1D(varname+"__"+jt+"__"+sysname, varname+"__"+jt+"__"+sysname, hr[0], hr[1], hr[2])
            #histo.SetDirectory(mydir)
            histo.SetDirectory(0)
            histo.Sumw2()
            histos[jt+varname] = histo
    
    print "start event loop"
    i=0
    for event in events:
        i += 1
        remainder = total_events % 100
        if total_events != remainder and ((i * 100) % (total_events - remainder) == 0):
            print (i * 101) / total_events, "%", strftime("%Y-%m-%d %H:%M:%S", gmtime())
        
        nelectrons = e.nelectrons(event)
        nmuons = e.nmuons(event)
        if channel == "mu":        
            if nelectrons != 0: continue
            if nmuons != 1: continue
        elif channel == "ele":
            if nelectrons != 1: continue
            if nmuons != 0: continue
        njets = e.njets(event)
        ntags = e.ntags(event)
        
        if njets == 2: 
            if ntags > 1: continue
        elif njets == 3:
            if ntags < 1 or ntags > 2: continue

        vetomuons = e.vetolepton.nmuons(event)
        vetoeles = e.vetolepton.nelectrons(event)
        #print nmuons, nelectrons, vetomuons, vetoeles
        if vetomuons > 0 or vetoeles > 0: continue

        mu_iso = sigmu.iso(event)
        el_iso = sigele.iso(event)
        #if (mu_iso < 0.2 or mu_iso > 0.25) and channel == "mu" and iso == "antiiso": continue
        if (mu_iso < 0.25 or mu_iso > 0.5) and channel == "mu" and iso == "antiiso": continue
        #if (mu_iso < 0.2 or mu_iso >= 0.25) and channel == "mu" and iso == "antiiso": continue
        #if (mu_iso < 0.3 or mu_iso > 0.9) and channel == "mu" and iso == "antiiso": continue
        #elif mu_iso > 0.12 and channel == "mu" and iso == "iso": continue
        #if (el_iso < 0.2 or el_iso > 0.9) and channel == "ele" and iso == "antiiso": continue
        #if (el_iso < 0.15 or el_iso > 0.5) and channel == "ele" and iso == "antiiso": continue
        if (el_iso < 0.165 or el_iso > 0.5) and channel == "ele" and iso == "antiiso": continue
        #if (el_iso < 0.15 or el_iso >= 0.165) and channel == "ele" and iso == "antiiso": continue
        #elif el_iso > 0.1 and channel == "ele" and iso == "iso": continue
        #electron_iso = Cut("el_mva > 0.9 & el_iso < 0.1")
        #antiIsolationCutDown = str(Cuts.mu_antiiso_down), 
        #antiIsolationCutUp = str(Cuts.mu_antiiso_up),
        
            

        if channel == "mu" and siglepton.pt(event) < 26: continue
        if channel == "ele" and siglepton.pt(event) < 30: continue
        if iso == "antiiso" and (ljet.dr(event) < 0.3 or bjet.dr(event) < 0.3): continue
        if bjet.pt(event) < 40 or ljet.pt(event) < 40: continue
        if abs(bjet.eta(event)) > 4.5 or abs(ljet.eta(event)) > 4.5: continue
        
        vars["met"][0] = e.met(event)
        vars["top_mass"][0] = top.mass(event)  
        vars["isotropy"][0] = e.isotropy(event)
        if channel == "ele":
            vars["bjet_pt"][0] = bjet.pt(event)
        if channel == "mu":
            vars["ljet_mass"][0] = ljet.mass(event)
            vars["ljet_pt"][0] = ljet.pt(event)
            vars[channel + "_mtw"][0] = siglepton.mtw(event)
            
        
        weight_pu = weight.pileup.nominal(event)

        total_weight = weight_pu
        if "Single" in dataset:
            total_weight = 1.
        calc=True
        for v in varlist:
            #print v, vars[v]
            if not vars[v] == vars[v]:
               calc = False
               continue
        if not total_weight == total_weight:
            calc = False
        
        

        if calc:
            jt = "%sj%st" % (njets, ntags)
            val = reader.EvaluateMVA("MVA_BDT")
            if cut == False:
                    histos[jt+"qcd_mva"].Fill(val, total_weight)
                    histos[jt+"met"].Fill(vars["met"][0], total_weight)
                    if channel == "mu":  
                        histos[jt+channel+"_mtw"].Fill(siglepton.mtw(event), total_weight)
        
            elif cut == True and val > qcd_mva_cut and reverse_cut == False:
                histos[jt+"qcd_mva"].Fill(val, total_weight)
                histos[jt+"met"].Fill(vars["met"][0], total_weight)
                if channel == "mu":  
                    histos[jt+channel+"_mtw"].Fill(siglepton.mtw(event), total_weight)
            elif cut == True and val <= qcd_mva_cut and reverse_cut == True:
                histos[jt+"qcd_mva"].Fill(val, total_weight)
                histos[jt+"met"].Fill(vars["met"][0], total_weight)
                if channel == "mu":  
                    histos[jt+channel+"_mtw"].Fill(siglepton.mtw(event), total_weight)
                            

    outfile.cd() 
    for h in histos.values():
        if not "Single" in dataset:
            xs = cross_sections[dataset]
            #print dataset
            h.Scale(scale_to_lumi(lumi, xs, getEventCount(dataset)))
        #h.SetDirectory(mydir)
        #print "writing", outfilename, h.GetDirectory()
        h.Write()
    outfile.Close()

    for f in ROOT.gROOT.GetListOfFiles():
        #print "closing", f
        f.Close("R")
print "finished"             

        
