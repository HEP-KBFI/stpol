import sys
import os

#Monkey-patch the system path to import the stpol header
sys.path.append(os.path.join(os.environ["STPOL_DIR"], "src/headers"))
from stpol import stpol, list_methods

import ROOT
# prepare the FWLite autoloading mechanism
ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()
from PhysicsTools.PythonAnalysis import *
from DataFormats.FWLite import Events, Handle, Lumis
#from PhysicsTools.FWLite import TFileService
#from FWCore.ServiceRegistry import Service
#from CommonTools.UtilAlgos import TFileService
#from PhysicsTools.FWLite import TFileService


def get_file_list(file_list_file):
    lines = [line.strip() for line in open(file_list_file)]
    return lines


#Print what methods are available for an object in a "flat" format for a simple overview
print "Muon properties (stpol.stable.signal.muon):"
list_methods(stpol.stable.tchan.muon)
print "Electron properties (stpol.stable.signal.electron):"
list_methods(stpol.stable.tchan.electron)


#indir = "/home/andres/single_top/stpol/filelists/Oct3_nomvacsv_nopuclean_e224b5/step2/"
indir = "/home/andres/single_top/stpol/filelists/Nov29_tW_etabl_CSVT_genwhgt_2fdd84/step2/"

indir_mc = indir + "mc/iso/nominal/Jul15/"
indir_data = indir + "data/antiiso/"

infile_lists = []
infile_lists.append(("mva_T_t_ToLeptons.txt", indir_mc + "T_t_ToLeptons.txt"))
infile_lists.append(("mva_Tbar_t_ToLeptons.txt", indir_mc + "Tbar_t_ToLeptons.txt"))
infile_lists.append(("mva_T_t.txt", indir_mc + "T_t.txt"))
infile_lists.append(("mva_Tbar_t.txt", indir_mc + "Tbar_t.txt"))
infile_lists.append(("mva_SingleMu1.txt", indir_data + "Jul15/SingleMu1.txt"))
infile_lists.append(("mva_SingleMu2.txt", indir_data + "Jul15/SingleMu2.txt"))
infile_lists.append(("mva_SingleMu3.txt", indir_data + "Jul15/SingleMu3.txt"))
infile_lists.append(("mva_SingleMu4.txt", indir_data + "Aug1/SingleMu_miss.txt"))


for (outfile_name, file_list_file) in infile_lists:
    outfile = open(outfile_name+"_0tags", "w")
    file_list = get_file_list(file_list_file)
    #Open the list of files supplied on the command line
    #file_list = sys.argv[1:]
    print file_list_file
    events = Events(file_list)

    #Very temporary short names for convenience
    e = stpol.stable.event
    sigmu = stpol.stable.tchan.muon
    sigele = stpol.stable.tchan.electron

    bjet = stpol.stable.tchan.bjet
    ljet = stpol.stable.tchan.specjet1
    top = stpol.stable.tchan.top
    
    #Loop over the events
    outfile.write("nelectrons/I:nmuons:njets:ntags:c/D:met:cos_theta:lepton_eta:lepton_pt:mtw:lepton_phi:top_eta:top_mass:bjet_bd_csv:bjet_dr:bjet_eta:bjet_mass:bjet_phi:bjet_pt:bjet_pu_mvaid:ljet_bd_csv:ljet_dr:ljet_eta:ljet_mass:ljet_phi:ljet_pt:ljet_pu_mvaid\n\n")

    for event in events:
        line = ""
        nelectrons = e.nelectrons(event)
        line += str(nelectrons) + " "
        if nelectrons != 0: continue
        nmuons = e.nmuons(event)
        line += str(nmuons) + " "   
        if nmuons != 1: continue
        njets = e.njets(event)
        if njets != 2: continue
        line += str(njets) + " "
        ntags = e.ntags(event)
        if ntags != 0: continue
        line += str(ntags) + " "

        c = e.c(event)
        line += str(c) + " "    
        met = e.met(event)
        line += str(met) + " "
        cos_theta = e.costheta.lj(event)
        line += str(met) + " "
        #<stpol.File instance at 0x45b14d0>
        #sample_type 
        #    Returns the sample dictionary corresponding to a filename.
        #    file:/hdfs/cms/store/user/joosep/Oct3_nomvacsv_nopuclean_e224b5/antiiso/nominal/QCD_Pt_80_170_BCtoE/output_1_1_KCj.root
            
        #total_processed 
        #    Returns the total (unskimmed/filtered) count of events processed per this file.
        #    Only correct when lumi-blocks are never split.
        #    Loops over the lumi blocks in the file, so is not particularly fast.

        mu_iso = sigmu.iso(event)
        if (mu_iso < 0.2 or mu_iso > 0.5) and "Single" in outfile_name: continue
        mu_eta = sigmu.eta(event)
        line += str(mu_eta) + " "
        mu_pt = sigmu.pt(event)
        line += str(mu_pt) + " "
        mtw = sigmu.mtw(event)
        line += str(mtw) + " "
        mu_phi = sigmu.phi(event)
        line += str(mu_phi) + " "
        
        top_eta = top.eta(event)
        line += str(top_eta) + " "
        top_mass = top.mass(event)  
        line += str(top_mass) + " "
        #phi 
        #pt

        bjet_bd_csv = bjet.bd_csv(event)
        line += str(bjet_bd_csv) + " "
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
        
        ljet_bd_csv = ljet.bd_csv(event)
        line += str(ljet_bd_csv) + " "
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

        #print "met=", e.met(event), "mu_pt=",mu_pt, "ele_pt=",ele_pt
        #print "mu_iso=", sigmu.iso(event), "ele_iso=", sigele.iso(event)
        #print line
        outfile.write(line+"\n") 

    outfile.close()
