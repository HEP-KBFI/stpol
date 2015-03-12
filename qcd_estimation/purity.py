#from rootpy.io import File
from os.path import join
#import argparse
#from plots.common.tdrstyle import tdrstyle
from ROOT import TCanvas, THStack, TFile, TH1D
import ROOT


from fit_components import *
from colors import *


def get_histos(fname, channel, isovar=None):
    f = TFile(fname)
    histos = {}
    for cut in ["nocut", "reversecut"]:
        for var in ["qcd_mva"]:#, "met", "mtw"]:
            for jt in ["2j1t", "2j0t", "3j1t", "3j2t"]:
                for iso in ["antiiso"]:
                    for dataset in all_datasets_reproc:
                        if dataset == "QCD":continue
                        name = "qcd__%s__%s__%s__%s__%s__%s" % (cut, channel, var, jt, iso, dataset)
                        if not isovar==None and iso == "antiiso":
                            name += "__isovar__%s" % isovar
                            #print "ISOVAR"
                        #print fname, name, cut+var+jt+iso+dataset
                        histos[cut+var+jt+iso+dataset] = f.Get(name)
                        #print sample_colors_same
                        histos[cut+var+jt+iso+dataset].SetLineColor(sample_colors_same[dataset])
                        if not "Single" in dataset:
                            histos[cut+var+jt+iso+dataset].SetFillColor(sample_colors_same[dataset])
                        #histos[cut+var+jt+iso+dataset].Rebin()
    return histos

def subtract_MC(hQCD, histos, cut, var, jt, variation=None):
    for dataset in fit_components_regular_reproc["non_qcd"]:
        h = histos[cut+var+jt+"antiiso"+dataset]
        coeff = -1
        if variation == "up":
            coeff *= (1+priors[dataset])
        elif variation == "down":
            coeff *= (1-priors[dataset])
        hQCD.Add(h, coeff)
        #print variation, dataset, priors[dataset]
        #print hQCD.Integral()

    for bin in range(hQCD.GetNbinsX()+1):
        if hQCD.GetBinContent(bin) < 0:
            hQCD.SetBinContent(bin, 0)
            hQCD.SetBinError(bin, 10.)

def subtract_MC_with_stack(hQCD, stack, variation=None):
    for h in stack.GetHists():
        coeff = -1
        if variation == "up":
            coeff *= (1+priors[dataset])
        elif variation == "down":
            coeff *= (1-priors[dataset])
        hQCD.Add(h, coeff)
        #print hQCD.Integral()

    for bin in range(hQCD.GetNbinsX()+1):
        if hQCD.GetBinContent(bin) < 0:
            hQCD.SetBinContent(bin, 0)
            hQCD.SetBinError(bin, 1.)

def add_other_components_ai(histos, cut, var, jt, components = "regular"):
    others = THStack("stack", "stack")
    for (comp, datasets) in components.items():
        hist = histos[cut+var+jt+"antiiso"+datasets[0]].Clone()
        name = hist.GetName().split("__")
        new_name = "__".join([var, comp])
        hist.SetNameTitle(new_name, new_name)
        #print datasets[0], hist.Integral()
        for i in range(1, len(datasets)):
            h = histos[cut+var+jt+"antiiso"+datasets[i]].Clone()
            hist.Add(h)
            #print datasets[i], h.GetEntries(), h.Integral()
        others.Add(hist)
    return others
        
    

def make_histos_purity(histos, channel, var, jt, cut, components, isovar=None, variateMC=None):
    hQCD = histos[cut+var+jt+"antiiso"+"data"]    
    others = add_other_components_ai(histos, cut, var, jt, components)
    return (hQCD, others)

def plot_purity(channel, var, jt, cut, hQCD, others):
    canv1 = TCanvas("canvas", "canvas", 800,800)
    #hQCD.SetAxisRange(0, HQC0.25, "Y")
    #h.GetXaxis().SetTitle(varname)                                       
    hQCD.SetLineWidth(2)
    leg = ROOT.TLegend(0.65,0.6,0.9,0.90)
    #leg.SetTextSize(0.037)
    leg.SetBorderSize(0)
    leg.SetLineStyle(0)
    leg.SetTextSize(0.015)
    leg.SetFillColor(0)
    hQCD.Draw()
    other_int = 0.
    #leghistos.items()[1].Draw("hist")
    for h in others.GetHists():
        #print h.GetName()
        other_int += h.Integral()
        h.Draw("hist same")
        leg.AddEntry(h, h.GetTitle().split("__")[1],"f")
    leg.AddEntry(hQCD,"QCD","l")
    leg.Draw()
    print "Purity", 100*hQCD.Integral() / (hQCD.Integral()+ other_int)
    #print "normQCD", normQCD.Integral()
    #normQCD.Draw("same hist")        
    canv1.SaveAs("purity_plots/purity_"+varname+"_"+channel+"_"+jt+"_"+cut+".pdf")
    canv1.SaveAs("purity_plots/purity_"+varname+"_"+channel+"_"+jt+"_"+cut+".png")
                        

if __name__=="__main__":
    #parser = argparse.ArgumentParser(description='')
    #parser.add_argument('--path', dest='path', default="/".join([os.environ["STPOL_DIR"], "src", "qcd_ntuples", "histos"]))
    #parser.add_argument('--channel', dest='channel' , default='mu')
    #args = parser.parse_args()
    components = fit_components_datasets

    ROOT.TH1.AddDirectory(False)
    ROOT.gROOT.SetStyle("Plain")
    ROOT.gStyle.SetOptStat(0)
    ROOT.gROOT.SetBatch()
    for channel in ["mu", "ele"]:
        myvars = ["qcd_mva"]#, "met"]
        #if channel == "mu":
        #myvars.append("mtw")
        added = "Feb18_pubfix" ##Nov_reproc"
    	for varname in myvars:
            for jt in ["2j1t", "2j0t", "3j1t", "3j2t"]:
                for cut in ["nocut", "reversecut"]:#, "qcdcut"]:
                    histos = get_histos("input_histos/%s/%s.root" % (added, channel), channel)  
                    #print "OUTFILE", "templates/"+varname+"__"+jt+"__"+channel+"__"+cut+"__"+added+".root"
                    (hQCD, others) = make_histos_purity(histos, channel, varname, jt, cut, components)
                    plot_purity(channel, varname, jt, cut, hQCD, others)    
                    
