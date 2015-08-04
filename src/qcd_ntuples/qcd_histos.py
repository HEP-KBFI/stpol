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

from utils import *
#from mva_variables import *
from Dataset import *


print "args", sys.argv[0], sys.argv[1]
#system.exit(1)
channel = sys.argv[1]
dataset = sys.argv[2]
counter = sys.argv[3]
iso = sys.argv[4]
cut = sys.argv[5]=="True"
reverse_cut = sys.argv[6]=="True"
#print sys.argv[5], cut
infile_list = sys.argv[7:]

print sys.argv[0:7]

qcd_mva_cut = 0.0
if channel == "ele":
    qcd_mva_cut = 0.2


#Print what methods are available for an object in a "flat" format for a simple overview
print "Muon properties (stpol.stable.signal.muon):"
list_methods(stpol.stable.tchan.muon)
print "Electron properties (stpol.stable.signal.electron):"
list_methods(stpol.stable.tchan.electron)


#ROOT.TMVA.Tools.Instance()
#reader = ROOT.TMVA.Reader( "Color:!Silent" )
#reader2 = ROOT.TMVA.Reader( "Color:!Silent" )

varlist = get_fixed(channel)

varlist_final = [ 'top_mass','ljet_eta','c','met','bjet_mass','ljet_mass','bjet_pt' ]
varlist_final.extend([channel+"_pt", channel+"_mtw"])

ranges = {}
ranges["mva_bdt"] = (20, -1, 1)
ranges["cos_theta"] = (20, -1, 1)
ranges["cos_theta_bl"] = (20, -1, 1)
if not reverse_cut:
    ranges["qcd_mva"] = (40, -1, 1)
    ranges["met"] = (40, 0, 200)
    ranges[channel+"_mtw"] = (40, 0, 200)
else:
    ranges["qcd_mva"] = (20, -1, qcd_mva_cut)
    ranges["met"] = (20, 0, 45)
    ranges[channel+"_mtw"] = (20, 0, 50)

ranges["c"] = (20, 0, 1)
ranges["top_mass"] = (20, 90, 490)
ranges["top_eta"] = (24, -6, 6)
ranges["D"] = (20, 0, 1)
ranges["circularity"] = (20, 0, 1)
ranges["aplanarity"] = (20, 0, 0.5)
ranges["isotropy"] = (20, 0, 1)
ranges["thrust"] = (20, 0.5, 1)
#ranges["bjet_bd_csv"]
ranges["bjet_dr"] = (20, 0, 6)
ranges["bjet_eta"] = (20, -3, 3)
ranges["bjet_mass"] = (20, 0, 100)
#ranges["bjet_phi"]
ranges["bjet_pt"] = (20, 40, 440)
#ranges["bjet_pu_mvaid"]
#ranges["bjet_rms"]
#ranges["ljet_bd_csv"]
ranges["ljet_dr"] = ranges["bjet_dr"]
ranges["ljet_eta"] = ranges["bjet_eta"]
ranges["ljet_mass"] = ranges["bjet_mass"]
#ranges["ljet_phi"]
ranges["ljet_pt"] = ranges["bjet_pt"]
#ranges["ljet_pu_mvaid"]
#ranges["ljet_rms"]
ranges[channel+"_pt"] = (40, 20, 220)
ranges[channel+"_eta"] = (40, -2.5, 2.5)
ranges[channel+"_phi"] = (40, -6, 6)
ranges["iso"] = (100, 0, 1)

vars={}
for v in varlist:
    vars[v] = array('f',[0])

#for v in varlist:
#    reader.AddVariable(v,vars[v])
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
#reader.BookMVA( "MVA_BDT", dirname+prefix+"_final2_"+channel+".weights.xml" )
#reader.BookMVA( "MLPBNN", dirname+prefix+"_MLPBNN.weights.xml" )

#reader2.BookMVA( "BDT_from_AN", dirname+prefix2+"_"+channel+".weights.xml" )

cross_sections = read_cross_sections()

lumi = 19728
if channel == "mu":
    lumi = 19739 


    
#print "dir00 ", ROOT.gDirectory.pwd()
#mydir = ROOT.gDirectory.pwd()
outfilename = os.environ["STPOL_DIR"]+"/src/qcd_ntuples/histos/"+channel+"/histos_"+docut+"_"+filename+"_"+counter+".root"

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
    histovars = vars.keys()
    extravars = get_extra_vars(channel)
    #histovars.extend(["cos_theta", "cos_theta_bl", "qcd_mva", "mva_bdt"])
    #histovars.extend([channel+"_pt", "iso"])
    #if reverse_cut==True:# or cut==False:
    #    for v in histovars:
    #        if not ("met" in v or "mtw" in v or "qcd_mva" in v or "cos_theta" in v):
    #            histovars.remove(v)
    #if cut==True:# temp
    #    histovars.extend([channel+"_eta", channel+"_phi"])
    # 
    #    for v in histovars:
    #        #if not ("met" in v or "mtw" in v or "mva" in v or "pt" in v or "top" in v or "ljet_eta" in v or v == "c" or "cos_theta" in v):
    #        #    histovars.remove(v)
    
    for varname in histovars:
        #print varname
        hr = ranges[varname]
        for jt in ["2j1t", "2j0t", "3j1t", "3j2t"]:
            #print "dir ", mydir#, ROOT.gDirectory.pwd()
            histo = TH1D(varname+"_"+jt+"_"+iso+"__"+dataset, varname+"_"+jt+"_"+iso+"__"+dataset, hr[0], hr[1], hr[2])
            #histo.SetDirectory(mydir)
            histo.SetDirectory(0)
            histo.Sumw2()
            histos[jt+varname] = histo
    for varname in extravars:
        #print varname
        hr = ranges[varname]
        for jt in ["2j1t", "2j0t", "3j1t", "3j2t"]:
            #print "dir ", mydir#, ROOT.gDirectory.pwd()
            histo = TH1D(varname+"_"+jt+"_"+iso+"__"+dataset, varname+"_"+jt+"_"+iso+"__"+dataset, hr[0], hr[1], hr[2])
            #histo.SetDirectory(mydir)
            histo.SetDirectory(0)
            histo.Sumw2()
            histos[jt+varname] = histo
    print "start event loop"
    i=0
    for event in events:
        i += 1
        #print i, 
        #if i > 25: continue
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
        #if (mu_iso < 0.25 or mu_iso > 0.5) and channel == "mu" and iso == "antiiso": continue
        #if (mu_iso < 0.2 or mu_iso >= 0.25) and channel == "mu" and iso == "antiiso": continue
        #if (mu_iso < 0.3 or mu_iso > 0.9) and channel == "mu" and iso == "antiiso": continue
        #elif mu_iso > 0.12 and channel == "mu" and iso == "iso": continue
        #if (el_iso < 0.2 or el_iso > 0.9) and channel == "ele" and iso == "antiiso": continue
        #if (el_iso < 0.15 or el_iso > 0.5) and channel == "ele" and iso == "antiiso": continue
        #if (el_iso < 0.165 or el_iso > 0.5) and channel == "ele" and iso == "antiiso": continue
        #if (el_iso < 0.15 or el_iso >= 0.165) and channel == "ele" and iso == "antiiso": continue
        #elif el_iso > 0.1 and channel == "ele" and iso == "iso": continue
        #electron_iso = Cut("el_mva > 0.9 & el_iso < 0.1")
        #antiIsolationCutDown = str(Cuts.mu_antiiso_down), 
        #antiIsolationCutUp = str(Cuts.mu_antiiso_up),
        
            

        if iso == "antiiso" and (ljet.dr(event) < 0.3 or bjet.dr(event) < 0.3): continue
        #vars["c"][0] = e.c(event)
        vars["met"][0] = e.met(event)
        vars["top_mass"][0] = top.mass(event)  
        #vars["top_eta"][0] = top.eta(event)

        #vars["D"][0] = e.d(event)
        #vars["aplanarity"][0] = e.aplanarity(event) 
        vars["isotropy"][0] = e.isotropy(event)
        #vars["thrust"][0] = e.thrust(event)
        
        #vars["bjet_dr"][0] = bjet.dr(event)
        #vars["bjet_eta"][0] = bjet.eta(event)
        #vars["bjet_mass"][0] = bjet.mass(event)
        #vars["bjet_phi"][0] = bjet.phi(event)
        if channel == "ele":
            vars["bjet_pt"][0] = bjet.pt(event)
        #vars["bjet_pu_mvaid"][0] = bjet.pu_mvaid(event)

        #vars["ljet_dr"][0] = ljet.dr(event)
        if channel == "mu":
            #vars["ljet_eta"][0] = ljet.eta(event)
            vars["ljet_mass"][0] = ljet.mass(event)
            #vars["ljet_phi"][0] = ljet.phi(event)
            vars["ljet_pt"][0] = ljet.pt(event)
        #vars["ljet_pu_mvaid"][0] = ljet.pu_mvaid(event)
        
        #if ljet.rms(event) > 0.025: continue
        if bjet.pt(event) < 40 or ljet.pt(event) < 40: continue
        if abs(bjet.eta(event)) > 4.5 or abs(ljet.eta(event)) > 4.5: continue
        #if rms_lj > 0.025: ...
        #if abs(vars["ljet_eta"][0]) < 2.5: continue
        #if vars["top_mass"][0] < 130 or vars["top_mass"][0] > 220: continue
        
        if channel == "mu":  
            vars[channel + "_mtw"][0] = siglepton.mtw(event)
        #vars[channel + "_eta"][0] = siglepton.eta(event)
        #vars[channel + "_pt"][0] = siglepton.pt(event)
        #vars[channel + "_phi"][0] = siglepton.phi(event)

        if channel == "mu" and siglepton.pt(event) < 26: continue
        if channel == "ele" and siglepton.pt(event) < 30: continue

        cos_theta[0] = e.costheta.lj(event)
        cos_theta_bl[0] = e.costheta.bl(event)

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
            #val = reader.EvaluateMVA("MVA_BDT")
            for varname in vars.keys():
                if varname not in histovars: continue
                #print "dir2", ROOT.gDirectory.pwd()
                if cut == False:
                    histos[jt+varname].Fill(vars[varname][0], total_weight)
                elif cut == True and val > qcd_mva_cut and reverse_cut == False:
                #elif cut == True and vars[channel+"_mtw"][0] > 50 and reverse_cut == False:
                    histos[jt+varname].Fill(vars[varname][0], total_weight)
                elif cut == True and val <= qcd_mva_cut and reverse_cut == True:
                    histos[jt+varname].Fill(vars[varname][0], total_weight)
            #print "dir2", ROOT.gDirectory.pwd()
            #val2 = reader2.EvaluateMVA("BDT_from_AN")
            if cut == False:
                    histos[jt+"cos_theta"].Fill(cos_theta[0], total_weight)
                    histos[jt+"cos_theta_bl"].Fill(cos_theta_bl[0], total_weight)
                    #histos[jt+"qcd_mva"].Fill(val, total_weight)
                    #histos[jt+"mva_bdt"].Fill(val2, total_weight)
                    histos[jt+"ljet_eta"].Fill(ljet.eta(event), total_weight)
                    histos[jt+"iso"].Fill(siglepton.iso(event), total_weight)
                    histos[jt+channel+"_pt"].Fill(siglepton.pt(event), total_weight)
                    histos[jt+channel+"_eta"].Fill(siglepton.eta(event), total_weight)
                    histos[jt+channel+"_phi"].Fill(siglepton.phi(event), total_weight)
                    if channel == "ele":  
                        histos[jt+channel+"_mtw"].Fill(siglepton.mtw(event), total_weight)
        
            elif cut == True and val > qcd_mva_cut and reverse_cut == False:
            #elif cut == True and vars[channel+"_mtw"][0] > 50 and reverse_cut == False:
                    histos[jt+"cos_theta"].Fill(cos_theta[0], total_weight)
                    histos[jt+"cos_theta_bl"].Fill(cos_theta_bl[0], total_weight)
                    histos[jt+"qcd_mva"].Fill(val, total_weight)
                    #histos[jt+"mva_bdt"].Fill(val2, total_weight)
                    histos[jt+"iso"].Fill(siglepton.iso(event), total_weight)
                    histos[jt+channel+"_pt"].Fill(siglepton.pt(event), total_weight)
                    histos[jt+channel+"_eta"].Fill(siglepton.eta(event), total_weight)
                    histos[jt+channel+"_phi"].Fill(siglepton.phi(event), total_weight)
                    if channel == "ele":  
                        histos[jt+channel+"_mtw"].Fill(siglepton.mtw(event), total_weight)
            elif cut == True and val <= qcd_mva_cut and reverse_cut == True:
                    histos[jt+"cos_theta"].Fill(cos_theta[0], total_weight)
                    histos[jt+"cos_theta_bl"].Fill(cos_theta_bl[0], total_weight)
                    histos[jt+"qcd_mva"].Fill(val, total_weight)
                    #histos[jt+"mva_bdt"].Fill(val2, total_weight)
                    histos[jt+"iso"].Fill(siglepton.iso(event), total_weight)
                    histos[jt+channel+"_pt"].Fill(siglepton.pt(event), total_weight)
                    histos[jt+channel+"_eta"].Fill(siglepton.eta(event), total_weight)
                    histos[jt+channel+"_phi"].Fill(siglepton.phi(event), total_weight)
                    if channel == "ele":  
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

        
