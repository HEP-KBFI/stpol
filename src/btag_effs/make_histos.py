# prepare the FWLite autoloading mechanism
from PhysicsTools.PythonAnalysis import *
from DataFormats.FWLite import Events, Handle, Lumis

import ROOT
from ROOT import TFile, TDirectory
ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

from rootpy.plotting import Hist2D, Hist


import sys
import os
from array import array
from time import gmtime, strftime
import math

n_eta_bins = 4
eta_bins = [0.0, 0.8, 1.6, 2.4]
WP_cut = 0.898

n_pt_bins = 18
pt_bins = [
    0,
    20,
    30,
    40,
    50,
    60,
    70,
    80,
    100,
    120,
    160,
    210,
    260,
    320,
    400,
    500,
    600,
    800
]
flavours = ["b", "c", "l", "uds", "g", "undefined"]

if __name__ == "__main__":
    print "args", sys.argv
    channel = sys.argv[1]
    dataset = sys.argv[2]
    counter = sys.argv[3]
    base_filename = sys.argv[4]

    ROOT.TH2.AddDirectory(False)

    def get_flavour(pdgid):
        pdgid = int(round(abs(pdgid)))
        #print pdgid
        if pdgid == 5: return "b"
        elif pdgid == 4: return "c"
        elif pdgid == 21: return "g"
        elif pdgid == 0: return "undefined"        
        else: return "uds"

    infile =  TFile.Open(base_filename, "read")
    events = infile.Get('dataframe')

    histos = {}
    histos_pt = {}
    histos_eta = {}
    for jets in [2,3]:
        histos[jets] = {}
        histos_pt[jets] = {}
        histos_eta[jets] = {}
        for flavour in flavours:
            for tpe in ["total", "tagged"]:
                title = "%s_%s" % (tpe, flavour)
                # 3 variable-width bins along x and 4 fixed-width bins along y
                histos[jets][title] = Hist2D(pt_bins, eta_bins, name = title, title = title, type='D')
                histos[jets][title].Sumw2()
                histos_pt[jets][title] = Hist(pt_bins, name = "pt_"+title, title = "pt_"+title, type='D')
                histos_pt[jets][title].Sumw2()
                histos_eta[jets][title] = Hist(eta_bins, name = "eta_"+title, title = "eta_"+title, type='D')
                histos_eta[jets][title].Sumw2()

    i=-1
    for event in events:
        
        if event.njets > 3 or event.njets < 2: continue
        
        if event.n_signal_mu == 1 and abs(event.lepton_type) == 13:
            ch = "mu"
        elif event.n_signal_ele == 1 and abs(event.lepton_type) == 11:
            ch = "ele"
        else: continue
        if not ch == channel: continue

        if event.n_veto_mu > 0 or event.n_veto_ele > 0: continue
        if event.bjet_pt <= 40 or event.ljet_pt <= 40: continue
        if abs(event.bjet_eta) >= 4.5 or abs(event.ljet_eta) >= 4.5: continue
        
        if channel == "mu" and event.hlt_mu != 1: continue
        if channel == "ele" and event.hlt_ele != 1: continue
        i+=1
        
        #if event.ljet_id_ISNA == 1 or event.bjet_id_ISNA == 1: continue
        #if int(round(abs(event.ljet_id))) == 0:
        #    print event.ljet_id, event.njets, event.ntags, event.ljet_pt, event.ljet_eta, event.ljet_bd_b

        histos[event.njets]["total_"+get_flavour(event.ljet_id)].Fill(event.ljet_pt, abs(event.ljet_eta))
        histos_pt[event.njets]["total_"+get_flavour(event.ljet_id)].Fill(event.ljet_pt)
        histos_eta[event.njets]["total_"+get_flavour(event.ljet_id)].Fill(abs(event.ljet_eta))
        if get_flavour(event.ljet_id) in ["g", "uds"]:#, "undefined"]:
            histos[event.njets]["total_"+"l"].Fill(event.ljet_pt, abs(event.ljet_eta))
            histos_pt[event.njets]["total_"+"l"].Fill(event.ljet_pt)
            histos_eta[event.njets]["total_"+"l"].Fill(abs(event.ljet_eta))

        if event.ljet_bd_b > WP_cut:
            histos[event.njets]["tagged_"+get_flavour(event.ljet_id)].Fill(event.ljet_pt, abs(event.ljet_eta))
            histos_pt[event.njets]["tagged_"+get_flavour(event.ljet_id)].Fill(event.ljet_pt)
            histos_eta[event.njets]["tagged_"+get_flavour(event.ljet_id)].Fill(abs(event.ljet_eta))
            if get_flavour(event.ljet_id) in ["g", "uds"]:#, "undefined"]:
                histos[event.njets]["tagged_"+"l"].Fill(event.ljet_pt, abs(event.ljet_eta))
                histos_pt[event.njets]["tagged_"+"l"].Fill(event.ljet_pt)
                histos_eta[event.njets]["tagged_"+"l"].Fill(abs(event.ljet_eta))

        histos[event.njets]["total_"+get_flavour(event.bjet_id)].Fill(event.bjet_pt, abs(event.bjet_eta))
        histos_pt[event.njets]["total_"+get_flavour(event.bjet_id)].Fill(event.bjet_pt)
        histos_eta[event.njets]["total_"+get_flavour(event.bjet_id)].Fill(abs(event.bjet_eta))
        if get_flavour(event.bjet_id) in ["g", "uds"]:#, "undefined"]:
            histos[event.njets]["total_"+"l"].Fill(event.bjet_pt, abs(event.bjet_eta))
            histos_pt[event.njets]["total_"+"l"].Fill(event.bjet_pt)
            histos_eta[event.njets]["total_"+"l"].Fill(abs(event.bjet_eta))        

        if event.bjet_bd_b > WP_cut:
            histos[event.njets]["tagged_"+get_flavour(event.bjet_id)].Fill(event.bjet_pt, abs(event.bjet_eta))
            histos_pt[event.njets]["tagged_"+get_flavour(event.bjet_id)].Fill(event.bjet_pt)
            histos_eta[event.njets]["tagged_"+get_flavour(event.bjet_id)].Fill(abs(event.bjet_eta))
            if get_flavour(event.bjet_id) in ["g", "uds"]:#, "undefined"]:
                histos[event.njets]["tagged_"+"l"].Fill(event.bjet_pt, abs(event.bjet_eta))
                histos_pt[event.njets]["tagged_"+"l"].Fill(event.bjet_pt)
                histos_eta[event.njets]["tagged_"+"l"].Fill(abs(event.bjet_eta))

        if event.njets == 3:
            histos[3]["total_"+get_flavour(event.sjet1_id)].Fill(event.sjet1_pt, abs(event.sjet1_eta))
            histos_pt[3]["total_"+get_flavour(event.sjet1_id)].Fill(event.sjet1_pt)
            histos_eta[3]["total_"+get_flavour(event.sjet1_id)].Fill(abs(event.sjet1_eta))
            if get_flavour(event.sjet1_id) in ["g", "uds"]:#, "undefined"]:
                histos[event.njets]["total_"+"l"].Fill(event.sjet1_pt, abs(event.sjet1_eta))
                histos_pt[event.njets]["total_"+"l"].Fill(event.sjet1_pt)
                histos_eta[event.njets]["total_"+"l"].Fill(abs(event.sjet1_eta))

            if event.sjet1_bd > WP_cut:
                histos[3]["tagged_"+get_flavour(event.sjet1_id)].Fill(event.sjet1_pt, abs(event.sjet1_eta))
                histos_pt[3]["tagged_"+get_flavour(event.sjet1_id)].Fill(event.sjet1_pt)
                histos_eta[3]["tagged_"+get_flavour(event.sjet1_id)].Fill(abs(event.sjet1_eta))
                if get_flavour(event.sjet1_id) in ["g", "uds"]:#, "undefined"]:
                    histos[event.njets]["tagged_"+"l"].Fill(event.sjet1_pt, abs(event.sjet1_eta))
                    histos_pt[event.njets]["tagged_"+"l"].Fill(event.sjet1_pt)
                    histos_eta[event.njets]["tagged_"+"l"].Fill(abs(event.sjet1_eta))
    

    outfilename = os.path.join(os.environ["STPOL_DIR"], "src/btag_effs/histos/", "btag_histos_%s_%s.root" % (dataset, counter))
    print i, "events"
    print outfilename
    outfile = TFile(outfilename, "RECREATE")
    outfile.cd() 

    for jets in [2,3]:
        #dr = TDirectory("%dJ" % jets, "%dJ" % jets)
        #dr.Write()
        outfile.mkdir("%dJ" % jets)
        outfile.cd("%dJ" % jets)
        for flavour in histos[jets].keys():
            histos[jets][flavour].Write()
            histos_pt[jets][flavour].Write()
            histos_eta[jets][flavour].Write()
    outfile.Close()
    print "finished"             


    """
    if __name__=="__main__":
        ROOT.TH2.AddDirectory(False)
        for channel in ["mu", "ele"]:
            print channel
            histos = get_histos("histos.root", channel)
            (hData, hMC) = make_histos(histos, channel)
            calc_ratios(hData, hMC, channel)
    """
