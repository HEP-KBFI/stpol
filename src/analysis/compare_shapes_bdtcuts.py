#from rootpy.io import File
from os.path import join
#import argparse
#from plots.common.tdrstyle import tdrstyle
from ROOT import TCanvas, THStack, TFile, TH1D, TText
import ROOT


systs = ["matching", "scale"]
variations = ["up", "down"]
keys = ["pre-cut", "bdt cut"]

def get_histos(filenames):
    histos = {}
    for which, fn in filenames.items():
        f = TFile(fn)
        #"2j1t__cos_theta_lj__wjets__matching__down"
        for syst in systs:
            for var in variations:
                name = "2j1t_cos_theta_lj__wjets__%s__%s" % (syst, var)
                #sys.exit
                histos["%s__%s__%s" % (which, syst, var)] = f.Get(name).Clone()
                histos["%s__%s__%s" % (which, syst, var)].SetDirectory(0)
    return histos

def plot_comparisons(filenames, histos, title):
    histkeys = histos.keys()
    for syst in systs:
        for var in variations:
            desc = title + "_%s_%s" % (syst, var)
            mytitle = "2J1T, %s %s, %s channel, BDT > %s vs no BDT cut" % (syst, var, title.split("_")[0], title.split("_")[1][:4])
            key0 = "%s__%s__%s" % (keys[0], syst, var)
            key1 = "%s__%s__%s" % (keys[1], syst, var)
            plot_templates(histos[key0], histos[key1], mytitle, desc)
    

def plot_templates(histo1, histo2, title, desc):
    canv1 = TCanvas("canvas", "canvas", 1000,1000)

    histo1.SetLineWidth(2)
    histo2.SetLineWidth(2)
    leg = ROOT.TLegend(0.15,0.75,0.4,0.9)
    #leg.SetTextSize(0.037)
    leg.SetBorderSize(1)
    leg.SetLineStyle(0)
    leg.SetTextSize(0.02)
    leg.SetFillColor(0)
    histo1.Scale(1/histo1.Integral())
    histo2.Scale(1/histo2.Integral())
    histo1.SetTitle(title)
    histo1.SetAxisRange(0, histo1.GetMaximum()*1.4, "Y")
    histo1.GetXaxis().SetTitle("cos (#theta *)")
    histo1.GetYaxis().SetTitle("")
    histo1.SetLineColor(ROOT.kRed)
    histo1.Draw("hist")
    histo1.SetLineColor(ROOT.kBlue)
    histo2.Draw("e1 same")
    txt = TText(0.3, histo1.GetMaximum() / 10, "KS = %.2f" % histo1.KolmogorovTest(histo2))
    txt.Draw()
    print "KS", histo1.KolmogorovTest(histo2)
    print histo1.Integral(), histo2.Integral()
    other_int = 0.
    #leghistos.items()[1].Draw("hist")
    #for h in others:
    #    #print h.GetName()
    #    h.Scale(1/h.Integral())
    #    h.SetLineWidth(2)
    #    h.Draw("hist same")
    #    leg.AddEntry(h, h.GetTitle().split("__")[1],"l")
    leg.AddEntry(histo1,"With BDT cut -0.2","l")
    leg.AddEntry(histo2,"With BDT cut","pl")
    leg.Draw()

    outname = "comparison_plots/bdtcut_"+desc
    canv1.SaveAs(outname+".pdf")
    canv1.SaveAs(outname+".png")


if __name__ == "__main__":
    #ROOT.SetDirectory(0)
    ROOT.gStyle.SetOptStat(0)
    #ROOT.gROOT.SetBatch()
    for channel in ["mu", "ele"]:
        for cut in ["0.30000", "0.45000", "0.60000"]:
            files = {}
            #files["pre-cut"] = "/home/andres/single_top/stpol_pdf/results/hists/Mar9/merged/preselection/2j_1t/%s/cos_theta_lj.root" % (channel)
            files["pre-cut"] = "/home/andres/single_top/stpol_pdf/results/hists/Mar9/merged/%s/%s/cos_theta_lj.root" % ("-0.20000", channel)
            files["bdt cut"] = "/home/andres/single_top/stpol_pdf/results/hists/Mar9/merged/%s/%s/cos_theta_lj.root" % (cut, channel)
            histos = get_histos(files)
            title = channel+"_"+cut
            plot_comparisons(files, histos, title)
