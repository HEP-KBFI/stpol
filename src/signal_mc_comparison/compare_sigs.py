#from rootpy.io import File
from os.path import join
#import argparse
#from plots.common.tdrstyle import tdrstyle
from ROOT import TCanvas, THStack, TFile, TH1D
import ROOT


myvars = ["bdt_sig_bg", "cos_theta_lj"]

colors = {
    "Powheg": ROOT.kBlack,
    "aMC@NLO": ROOT.kRed,
    "Comphep": ROOT.kBlue
}

descs = {
    "preqcd": "before QCD cut",
    "preselection": "After QCD cut",
    "bdt": "After signal BDT cut"
}

def get_histos(fname):
    f = TFile(fname)
    histos = {}
    for channel in ["mu", "ele"]:
        for cut in ["preqcd", "preselection", "bdt"]:
            for var in myvars:
                for dataset in ["Powheg", "Comphep", "aMC@NLO"]:
                    name = "histo__%s__%s__%s__%s" % (dataset, channel, var, cut)
                    histos[dataset+channel+var+cut] = f.Get(name)
                    histos[dataset+channel+var+cut].Scale(1/histos[dataset+channel+var+cut].Integral())
                    histos[dataset+channel+var+cut].SetLineColor(colors[dataset])                    
    return histos

def plot_signals(channel, var, cut, histos):
    canv1 = TCanvas("canvas", "canvas", 800,800)
    hPowheg = histos["Powheg"+channel+var+cut]
    hComphep = histos["Comphep"+channel+var+cut]
    haMC = histos["aMC@NLO"+channel+var+cut]
    
    #h.GetXaxis().SetTitle(varname)                                       
    hPowheg.SetLineWidth(3)
    leg = ROOT.TLegend(0.1,0.75,0.4,0.90)
    #leg.SetTextSize(0.037)
    leg.SetBorderSize(0)
    leg.SetLineStyle(0)
    leg.SetTextSize(0.04)
    leg.SetFillColor(0)
    hPowheg.SetTitle("%s %s, %s channel" % (var, descs[cut], channel))
    hPowheg.GetXaxis().SetTitle(var)
    #hQCD.Scale(1/hQCD.Integral())
    hPowheg.SetAxisRange(0, 0.075, "Y")
    if "cos_theta" in var:
        hPowheg.SetAxisRange(0, 0.06, "Y")
    hPowheg.Draw("e1")
    hComphep.Draw("e1 same")
    haMC.Draw("e1 same")
    print "KS aMC:", channel, var, cut, hPowheg.KolmogorovTest(haMC)
    print "KS comphep:", channel, var, cut, hPowheg.KolmogorovTest(hComphep)
    leg.AddEntry(hPowheg,"Powheg","l")
    leg.AddEntry(hComphep,"Comphep","l")
    leg.AddEntry(haMC,"aMC@NLO","l")
    leg.Draw()

    canv1.SaveAs("signal_comparison_plots/sig_comp_"+channel+"_"+var+"_"+cut+".pdf")
    canv1.SaveAs("signal_comparison_plots/sig_comp_"+channel+"_"+var+"_"+cut+".png")
                        

if __name__=="__main__":
    ROOT.TH1.AddDirectory(False)
    ROOT.gROOT.SetStyle("Plain")
    ROOT.gStyle.SetOptStat(0)
    ROOT.gROOT.SetBatch()
    histos = get_histos("sig_comparison_histos/added.root")  
    for channel in ["mu", "ele"]:
        #added = "May30" ##Nov_reproc"
    	for varname in myvars:
            for cut in ["preqcd", "preselection", "bdt"]:
                plot_signals(channel, varname, cut, histos)    
                    
