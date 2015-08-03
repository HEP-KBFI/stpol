#from rootpy.io import File
from os.path import join
#import argparse
#from plots.common.tdrstyle import tdrstyle
from ROOT import TCanvas, THStack, TFile, TH1D
import ROOT


from fit_components import *
from colors import *

myvars = ["qcd_mva", "met", "mtw", "lepton_met_dr", "bjet_met_dr", "ljet_met_dr", "sjet1_met_dr", "sjet2_met_dr", "lepton_met_dphi", "bjet_met_dphi", "ljet_met_dphi", "jet1_met_dphi", "jet2_met_dphi", "bjet_dphi", "ljet_dphi"]
        

def get_histos(fname, channel, isovar=None):
    f = TFile(fname)
    histos = {}
    for cut in ["nocut", "reversecut"]:
        for var in myvars:#["qcd_mva"]:#, "met", "mtw"]:
            for jt in ["2j1t", "2j0t", "3j1t", "3j2t"]:
                for iso in ["iso", "antiiso"]:
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
                        if "Single" in dataset and "antiiso" in iso:
                            histos[cut+var+jt+iso+dataset].SetLineColor(ROOT.kGray)
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

def get_other_components(histos, cut, var, jt, components = "regular"):
    others = []
    for (comp, datasets) in components.items():
        hist = histos[cut+var+jt+"iso"+datasets[0]].Clone()
        name = hist.GetName().split("__")
        new_name = "__".join([var, comp])
        hist.SetNameTitle(new_name, new_name)
        #print datasets[0], hist.Integral()
        for i in range(1, len(datasets)):
            h = histos[cut+var+jt+"iso"+datasets[i]].Clone()
            hist.Add(h)
            print datasets[i], h.GetEntries(), h.Integral()
        others.append(hist)
    return others


def make_template_histos(histos, channel, var, jt, cut, components, isovar=None, variateMC=None):
    hData = histos[cut+var+jt+"iso"+"data"]
    hData.SetNameTitle("%s__DATA" % var, "%s__DATA" % var)
    
    hQCD = histos[cut+var+jt+"antiiso"+"data"]
    print "qcd", isovar, hQCD.GetEntries(), hQCD.Integral()
    subtract_MC(hQCD, histos, cut, var, jt, variateMC)
    print "qcd_sub", isovar, hQCD.GetEntries(), hQCD.Integral()
        
    hQCD.SetNameTitle("%s__QCD" % var, "%s__QCD" % var)
    print hQCD.GetEntries(), hData.Integral()
    others = get_other_components(histos, cut, var, jt, components)
    return (hData, hQCD, others)

def plot_templates(channel, var, jt, cut, hData, hQCD, others):
    canv1 = TCanvas("canvas", "canvas", 800,800)
    #h.GetXaxis().SetTitle(varname)                                       
    hQCD.SetLineWidth(3)
    leg = ROOT.TLegend(0.7,0.6,0.95,0.90)
    #leg.SetTextSize(0.037)
    leg.SetBorderSize(0)
    leg.SetLineStyle(0)
    leg.SetTextSize(0.04)
    leg.SetFillColor(0)
    hQCD.SetTitle("%s distribution before QCD cut, %s, %s" % (var, channel, jt))
    hQCD.GetXaxis().SetTitle(var)
    hQCD.Scale(1/hQCD.Integral())
    hQCD.SetAxisRange(0, 0.2, "Y")
    if "dr" in var or "dphi" in var:
        hQCD.SetAxisRange(0, 0.1, "Y")
    hQCD.Draw("hist")
    hData.Scale(1/hData.Integral())
    hData.SetMarkerStyle(20)
    hData.Draw("e1 same")
    
    other_int = 0.
    #leghistos.items()[1].Draw("hist")
    for h in others:
        #print h.GetName()
        h.Scale(1/h.Integral())
        h.SetLineWidth(2)
        h.Draw("hist same")
        leg.AddEntry(h, h.GetTitle().split("__")[1],"l")
    leg.AddEntry(hQCD,"QCD","l")
    leg.AddEntry(hData,"Data","pl")
    leg.Draw()

    #print "normQCD", normQCD.Integral()
    #normQCD.Draw("same hist")        
    canv1.SaveAs("template_plots/"+var+"_shapes_"+channel+"_"+jt+"_"+cut+".pdf")
    canv1.SaveAs("template_plots/"+var+"_shapes_"+channel+"_"+jt+"_"+cut+".png")
                        

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
        #myvars = ["qcd_mva"]#, "met"]
        #if channel == "mu":
        #myvars.append("mtw")
        added = "May30" ##Nov_reproc"
    	for varname in myvars:
            for jt in ["2j1t"]:#, "2j0t", "3j1t", "3j2t"]:
                for cut in ["nocut"]:#, "reversecut"]:#, "qcdcut"]:
                    histos = get_histos("input_histos/%s/%s.root" % (added, channel), channel)  
                    print "OUTFILE", "templates/"+varname+"__"+jt+"__"+channel+"__"+cut+"__"+added+".root"
                    (hData, hQCD, others) = make_template_histos(histos, channel, varname, jt, cut, components)
                    plot_templates(channel, varname, jt, cut, hData, hQCD, others)    
                    
