import sys
import os
from array import array

#Monkey-patch the system path to import the stpol header
sys.path.append(os.path.join(os.environ["STPOL_DIR"], "src/headers"))
from stpol import stpol, list_methods

import ROOT
from DataFormats.FWLite import Events, Handle, Lumis
from utils import *
import math

print "args", sys.argv[0], sys.argv[1]
#system.exit(1)
dataset = sys.argv[1]
counter = sys.argv[2]
iso = sys.argv[3]
file_list = sys.argv[4:]
print "files", file_list
lumi = 19700

outfiles = {}
if not "SingleEle" in dataset:
    outfiles["mu_2j1t"] = open(os.path.join(os.environ["STPOL_DIR"], "src", "qcd_ntuples", "mva_input", dataset+"_mu_2j1t_" + counter + ".txt"), "w")
    outfiles["mu_2j0t"] = open(os.path.join(os.environ["STPOL_DIR"], "src", "qcd_ntuples", "mva_input", dataset+"_mu_2j0t_" + counter + ".txt"), "w")
if not "SingleMu" in dataset:
    outfiles["ele_2j1t"] = open(os.path.join(os.environ["STPOL_DIR"], "src", "qcd_ntuples", "mva_input", dataset+"_ele_2j1t_" + counter + ".txt"), "w")
    outfiles["ele_2j0t"] = open(os.path.join(os.environ["STPOL_DIR"], "src", "qcd_ntuples", "mva_input", dataset+"_ele_2j0t_" + counter + ".txt"), "w")

#print file_list_file
events = Events(file_list)

e = stpol.stable.event
sigmu = stpol.stable.tchan.muon
sigele = stpol.stable.tchan.electron
bjet = stpol.stable.tchan.bjet
ljet = stpol.stable.tchan.specjet1
top = stpol.stable.tchan.top
wboson = stpol.stable.tchan.wboson
shat = stpol.stable.tchan.shat
weight = stpol.stable.weights
ffile = stpol.stable.file
   
i=0
cross_sections = read_cross_sections()
for name, of in outfiles.items():
        of.write("nelectrons/I:nmuons:njets:ntags:C/D:C_with_nu:met:met_phi:cos_theta")
        of.write(":D:circularity:aplanarity:isotropy:thrust:sphericity")

        of.write(":top_eta:top_mass:top_pt:top_phi")
        of.write(":w_mass:w_pt:w_eta:w_phi")
        of.write(":shat_mass:shat_pt:shat_eta:shat_phi")
        of.write(":bjet_dr:bjet_eta:bjet_mass:bjet_phi:bjet_pt:bjet_pu_mvaid:bjet_rms")
        of.write(":ljet_dr:ljet_eta:ljet_mass:ljet_phi:ljet_pt:ljet_pu_mvaid:ljet_rms")
        of.write(":pu_weight:top_weight:b_weight:weight_xs")
        of.write(":lepton_iso:lepton_eta:lepton_pt:mtw:lepton_phi")
        
        #"hlt", "hlt_mu", "hlt_ele", 
        #"hadronic_pt", "hadronic_eta", "hadronic_phi", "hadronic_mass",
        #"shat", "ht", 
        #"xs" !
                
        of.write("\n")

total_events = 0
for f in file_list:
    print f, ffile.total_processed(f)
    total_events += ffile.total_processed(f)    


c1 = 0
c2 = 0
c3 = 0
c4 = 0
c5 = 0
b = 0
for event in events:
        c1 += 1
        #if i > 10:
        #    break
        line = ""
        nelectrons = e.nelectrons(event)
        line += str(nelectrons) + " "
        if nelectrons > 1: continue
        nmuons = e.nmuons(event)
        line += str(nmuons) + " "   
        if nmuons > 1: continue
        njets = e.njets(event)
        
        vetomuons = e.vetolepton.nmuons(event)
        vetoeles = e.vetolepton.nelectrons(event)
        #print nmuons, nelectrons, vetomuons, vetoeles
        if vetomuons > 0 or vetoeles > 0: continue
        c2 += 1
        
        if njets != 2: continue
        line += str(njets) + " "
        ntags = e.ntags(event)
        if ntags != 0 and ntags != 1: continue
        line += str(ntags) + " "
        c3 += 1
        c = e.c(event)
        line += str(c) + " " + str(e.c_with_nu(event)) +  " "
        met = e.met(event)
        line += str(met) + " " + str(e.met_phi(event)) + " "
        cos_theta = e.costheta.lj(event)
        line += str(cos_theta) + " "

        #of.write(":D:circularity:aplanarity:isotropy:thrust")
        line += str(e.d(event)) + " " + str(e.circularity(event)) + " " + str(e.aplanarity(event)) + " " + str(e.isotropy(event)) + " " + str(e.thrust(event)) + " " + str(e.sphericity(event)) + " "
    
        mu_iso = sigmu.iso(event)
        el_iso = sigele.iso(event)
        #print dataset, mu_iso, el_iso
        if (mu_iso < 0.2 or mu_iso > 0.5) and "SingleMu" in dataset: continue
        if (el_iso < 0.15 or el_iso > 0.5) and "SingleEle" in dataset: continue

        top_eta = top.eta(event)
        line += str(top_eta) + " "
        top_mass = top.mass(event)  
        line += str(top_mass) + " "
        line += str(top.pt(event)) + " " + str(top.phi(event)) + " "        
        #phi 
        #pt
        line += str(wboson.mass(event)) + " " + str(wboson.pt(event))  + " " + str(wboson.eta(event))  + " " + str(wboson.phi(event)) + " "
        line += str(shat.mass(event)) + " " + str(shat.pt(event))  + " " + str(shat.eta(event))  + " " + str(shat.phi(event)) + " "  

        #bjet_bd_csv = bjet.bd_csv(event)
        #line += str(bjet_bd_csv) + " "
        bjet_dr = bjet.dr(event)
        line += str(bjet_dr) + " "
        bjet_eta = bjet.eta(event)
        line += str(bjet_eta) + " "
        bjet_mass = bjet.mass(event)
        line += str(bjet_mass) + " "
        bjet_phi = bjet.phi(event)
        line += str(bjet_phi) + " "
        bjet_pt = bjet.pt(event)
        line += str(bjet_pt) + " "
        bjet_pu_mvaid = bjet.pu_mvaid(event)
        line += str(bjet_pu_mvaid) + " "
        line += str(bjet.rms(event)) + " "
        
        #ljet_bd_csv = ljet.bd_csv(event)
        #line += str(ljet_bd_csv) + " "
        ljet_dr = ljet.dr(event)
        line += str(ljet_dr) + " "
        ljet_eta = ljet.eta(event)
        line += str(ljet_eta) + " "
        ljet_mass = ljet.mass(event)
        line += str(ljet_mass) + " "
        ljet_phi = ljet.phi(event)
        line += str(ljet_phi) + " "
        ljet_pt = ljet.pt(event)
        line += str(ljet_pt) + " "
        ljet_pu_mvaid = ljet.pu_mvaid(event)
        line += str(ljet_pu_mvaid) + " "
        line += str(ljet.rms(event)) + " "
        
        xs = cross_sections[replace_name(dataset)]
        if "Single" in dataset:
            line += "1 1 1 1 "
        else:
            weight_pu = weight.pileup.nominal(event)
            line += str(weight_pu) + " "
            weight_top = weight.toppt.nominal(event)
            if not "TTJets" in dataset:
                weight_top = 1.
            line += str(weight_top) + " "
            weight_b = weight.btag.nominal(event)
            if math.isnan(weight_b): 
                b += 1
                continue
            line += str(weight_b) + " "
            line += str(scale_to_lumi(lumi, xs, total_events))+" "
        #i+= 1   

        if nmuons == 1 and nelectrons == 0:
            lepton = "mu"
            line += str(mu_iso) + " "
            mu_eta = sigmu.eta(event)
            line += str(mu_eta) + " "
            mu_pt = sigmu.pt(event)
            line += str(mu_pt) + " "
            mtw = sigmu.mtw(event)
            line += str(mtw) + " "
            mu_phi = sigmu.phi(event)
            line += str(mu_phi) + " "
        elif nelectrons == 1 and nmuons == 0:
            lepton = "ele"
            line += str(el_iso) + " "
            ele_eta = sigele.eta(event)
            line += str(ele_eta) + " "
            ele_pt = sigele.pt(event)
            line += str(ele_pt) + " "
            ele_mtw = sigele.mtw(event)
            line += str(ele_mtw) + " "
            ele_phi = sigele.phi(event)
            line += str(ele_phi) + " "
        else:
            continue
        if lepton == "mu" and "SingleEle" in dataset: continue        
        if lepton == "ele" and "SingleMu" in dataset: continue
        c4 += 1

        if bjet_dr < 0.3 or ljet_dr < 0.3: continue
        outfiles["%s_%dj%dt" % (lepton,njets, ntags)].write(line+"\n") 

        c5 += 1
        #print "met=", e.met(event), "mu_pt=",mu_pt, "ele_pt=",ele_pt
        #print "mu_iso=", sigmu.iso(event), "ele_iso=", sigele.iso(event)
        #print line
        #system.exit(1)
        
print "BEE", c1, c2, c3, c4, c5, "bw", b
print "TSEE", c5
for of in outfiles.values():
    of.close()
print "finished"
