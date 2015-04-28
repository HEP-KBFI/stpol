import ROOT
from ROOT import TFile
from os import path
import os
import sys
from rootpy.plotting import Hist2D, Hist
from make_histos import flavours, eta_bins, pt_bins

def calc_effs(dataset):
    infile = TFile(os.path.join(os.environ["STPOL_DIR"], "src/btag_effs/added_histos/", "%s.root" % (dataset)))

    effs = {}
    effs_pt = {}
    effs_eta = {}
    total_integrals = {}
    tagged_integrals = {}
    int_tot = {}
    int_tot_tagged = {}
    for jets in [2,3]:
        effs[jets] = {}
        effs_pt[jets] = {}
        effs_eta[jets] = {}
        total_integrals[jets] = {}
        tagged_integrals[jets] = {}
        int_tot[jets] = 0.0
        int_tot_tagged[jets] = 0.0
        for flavour in flavours:
            title = "eff_%s" % flavour
            effs[jets][flavour] = Hist2D(pt_bins, eta_bins, name = title, title = title, type='D')
            effs_pt[jets][flavour] = Hist(pt_bins, name = "pt_"+title, title = "pt_"+title, type='D')
            effs_eta[jets][flavour] = Hist(eta_bins, name = "eta_"+title, title = "eta_"+title, type='D')
            total = infile.Get("%dJ/total_%s" % (jets, flavour))
            tagged = infile.Get("%dJ/tagged_%s" % (jets, flavour))
            for binx in range(total.GetNbinsX()+2):
                for biny in range(total.GetNbinsY()+2):
                    print dataset, jets, flavour, binx, biny, tagged.GetBinContent(binx, biny), tagged.GetBinError(binx, biny), total.GetBinContent(binx, biny), total.GetBinError(binx, biny)
            pt_total = infile.Get("%dJ/pt_total_%s" % (jets, flavour))
            pt_tagged = infile.Get("%dJ/pt_tagged_%s" % (jets, flavour))
            eta_total = infile.Get("%dJ/eta_total_%s" % (jets, flavour))
            eta_tagged = infile.Get("%dJ/eta_tagged_%s" % (jets, flavour))
            total_integrals[jets][flavour] = total.Integral()
            tagged_integrals[jets][flavour] = tagged.Integral()
            int_tot[jets] += total.Integral()
            int_tot_tagged[jets] += tagged.Integral()
            effs[jets][flavour] = tagged.Clone(title)
            effs[jets][flavour].Divide(total)
            for binx in range(total.GetNbinsX()+2):
                for biny in range(total.GetNbinsY()+2):
                    print dataset, jets, flavour, binx, biny, effs[jets][flavour].GetBinContent(binx, biny), effs[jets][flavour].GetBinError(binx, biny)
            effs_pt[jets][flavour] = pt_tagged.Clone("pt_"+title)
            effs_pt[jets][flavour].Divide(pt_total)
            effs_eta[jets][flavour] = eta_tagged.Clone("eta_"+title)
            effs_eta[jets][flavour].Divide(eta_total)
        


                    

    outfilename = os.path.join(os.environ["STPOL_DIR"], "src/btag_effs/eff_histos/", "%s.root" % (dataset))
    print outfilename
    outfile = TFile(outfilename, "RECREATE")
    outfile.cd() 

    for jets in [2,3]:
        outfile.mkdir("%dJ" % jets)
        outfile.cd("%dJ" % jets)
        print "%dJ" % jets
        for flavour in effs[jets].keys():
            effs[jets][flavour].Write()
            effs_pt[jets][flavour].Write()
            effs_eta[jets][flavour].Write()
            print "total %s %.3f" % (flavour, 100 * total_integrals[jets][flavour] / int_tot[jets])
            print "tagged %s %.3f" % (flavour, 100 * tagged_integrals[jets][flavour] / int_tot_tagged[jets])
            print "efficiency %s %.3f" % (flavour, 100 * tagged_integrals[jets][flavour] / total_integrals[jets][flavour])


if __name__=="__main__":
    ROOT.TH2.AddDirectory(False)
    for dataset in ["tchan", "ttjets", "wjets"]:
        print dataset
        calc_effs(dataset)
        print ""
