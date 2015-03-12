#from rootpy.io import File
from os.path import join
#import argparse
#from plots.common.tdrstyle import tdrstyle
from ROOT import TCanvas, THStack, TFile, TH1D
import ROOT


from fit_components import *
from colors import *


def get_histos(fname, channel):
    f = TFile(fname)
    histos = {}
    for var in ["mtw"]:
        for jt in ["alljt"]:#"2j1t", "2j0t", "3j1t", "3j2t"]:
            for iso in ["iso"]:#, "antiiso"]:
                for dataset in all_datasets_reproc:
                    if iso == "antiiso" and not dataset == "data":continue
                    name = "qcd__%s__%s__%s__%s__%s" % (channel, var, jt, iso, dataset)
                    if "QCD" in name:continue
                    #print fname 
                    #print name
                    print channel+var+jt+iso+dataset
                    histos[var+jt+iso+dataset] = f.Get(name)
                    histos[var+jt+iso+dataset].SetLineColor(sample_colors_same[dataset])
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

def add_other_components(histos, cut, var, jt, components = "regular"):
    others = []
    for (comp, datasets) in fit_components_reproc[components].items():
        hist = histos[cut+var+jt+"iso"+datasets[0]].Clone()
        name = hist.GetName().split("__")
        new_name = "__".join([var, comp])
        hist.SetNameTitle(new_name, new_name)
        print datasets[0], hist.GetEntries(), hist.Integral()
        for i in range(1, len(datasets)):
            h = histos[cut+var+jt+"iso"+datasets[i]].Clone()
            hist.Add(h)
            print datasets[i], h.GetEntries(), h.Integral()
        others.append(hist)
    return others
        
    

def make_histos(histos, channel, var, jt, cut, components, isovar=None, variateMC=None):
    hData = histos[cut+var+jt+"iso"+"data"]
    #print "data", isovar, hData.GetEntries(), hData.Integral()
    hData.SetNameTitle("%s__DATA" % var, "%s__DATA" % var)
    """if variateMC == "QCDMC":
        hQCD = histos[cut+var+jt+"iso"+"QCD"]
    elif variateMC == "QCDMC2J0T":
        hQCD = histos[cut+var+"2j0t"+"iso"+"QCD"]
    else:
        hQCD = histos[cut+var+jt+"antiiso"+"data"]
        #print "qcd", isovar, hQCD.GetEntries(), hQCD.Integral()
        #subtract_MC(hQCD, histos, cut, var, jt, variateMC)
        #print "qcd_sub", isovar, hQCD.GetEntries(), hQCD.Integral()
        
    hQCD.SetNameTitle("%s__QCD" % var, "%s__QCD" % var)"""
    #print hQCD.GetEntries(), hData.Integral()
    
    others = add_other_components(histos, cut, var, jt, components)
    #return (hData, hQCD, others)
    return (hData, None, others)
    
           

if __name__=="__main__":
    components = "datasets"

    ROOT.TH1.AddDirectory(False)
    ROOT.gROOT.SetStyle("Plain")
    ROOT.gStyle.SetOptStat(0)
    ROOT.gROOT.SetBatch()
    for channel in ["mu", "ele"]:
        myvars = ["mtw"]
    	for varname in myvars:
            histos = get_histos("yield_histos/%s.root" % channel, channel)  
            (hData, hQCD, others) = make_histos(histos, channel, varname, "alljt", cut="", components=components)
            #if not variateMC and not isovar:
            #    plot_QCD_template(hQCD, channel, varname, jt, cut)
            print channel, "YIELDS:"
            #print "QCD: ", hQCD.GetEntries(), hQCD.Integral()
            print "Data: ", hData.GetEntries(), hData.Integral()
            for h in others:
                print h.GetName(), h.GetEntries(), h.Integral()
          
           
