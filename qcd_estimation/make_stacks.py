#from rootpy.io import File
from os.path import join
#import argparse
#from plots.common.tdrstyle import tdrstyle
from ROOT import TCanvas, THStack, TFile, TH1D
import ROOT


from fit_components import *
from colors import *
from fitted_scale_factors import *
from make_templates import *


variables = ["bdt_sig_bg"]:#, "bdt_sig_bg_old", "qcd_mva", "qcd_mva_new", "met", "mtw", "lepton_pt", "lepton_eta", "lepton_iso", "lepton_phi", "bjet_pt", "bjet_eta", "bjet_mass", "bjet_bd_b",
    "bjet_phi", "bjet_dr", "bjet_pumva", "ljet_pt", "ljet_eta", "ljet_mass", "ljet_bd_b", "ljet_phi", "ljet_dr", "ljet_pumva",
    "sjet1_pt", "sjet1_eta", "sjet1_bd", "sjet2_pt", "sjet2_eta", "sjet2_bd", "cos_theta_lj", "cos_theta_bl", "cos_theta_whel_lj", "met_phi", "C", "D", "circularity", "sphericity", "isotropy", "aplanarity", "thrust", "C_with_nu", "top_mass", "top_pt",
    "top_eta", "top_phi", "w_mass", "w_pt", "w_eta", "w_phi", "jet_cls", "hadronic_pt", "hadronic_eta", "hadronic_phi", "hadronic_mass",
    "shat_pt", "shat_eta", "shat_phi", "shat_mass", "shat", "ht"
]

#variables = ["bdt_sig_bg", "cos_theta_lj"
#]



def get_histos(fname, channel):
    f = TFile(fname)
    histos = {}
    #for cut in ["qcdcut", "nocut", "reversecut", "bdtcut", "bdtcut_old"]:
    for cut in ["bdtcut"]:
        for var in variables:
            for jt in ["2j1t"]:#, "2j0t", "3j1t", "3j2t"]:
                for iso in ["iso"]:#, "antiiso"]:
                    for dataset in all_datasets_reproc:
                        name = "histo__%s__%s__%s__%s__%s__%s" % (cut, channel, var, jt, iso, dataset)
                        print fname, name
                        histos[cut+var+jt+iso+dataset] = f.Get(name)
                        histos[cut+var+jt+iso+dataset].SetLineColor(sample_colors_same[dataset])
                        histos[cut+var+jt+iso+dataset].SetFillColor(sample_colors_same[dataset])
                        if not dataset == "data":
                            #histos[cut+var+jt+iso+dataset].SetFillColor(sample_colors_same[dataset])
                            pass
                        #histos[cut+var+jt+iso+dataset].Rebin(2)
                        if ("Single" in dataset or "data" in dataset) and iso == "antiiso": 
                            histos[cut+var+jt+iso+dataset].Scale(qcd_scale_factors[channel][jt])
                        #print dataset, sample_colors_same[dataset]

                        #histos[cut+var+jt+iso+dataset].Rebin()
    #asd
    return histos


def make_stack(histos, channel, var, jt, cut, iso):
    hData = histos[cut+var+jt+iso+"data"]
    print "data", hData.GetEntries(), hData.Integral()
    #hData.SetNameTitle("%s__DATA" % var, "%s__DATA" % var)

    stack = THStack(channel+var+jt+cut+iso, channel+var+jt+cut+iso)

    hQCD = histos[cut+var+jt+"antiiso"+"data"]
    hQCD.SetLineColor(sample_colors_same["QCD"])
    hQCD.SetFillColor(sample_colors_same["QCD"])
    hQCD.SetNameTitle("QCD", "QCD")
                        
    for dataset in all_datasets_reproc:
        if "QCD" in dataset:continue
        if "data" in dataset: continue
        hQCD.Add(histos[cut+var+jt+"antiiso"+dataset], -1)
        
    for dataset in all_datasets_reproc:
        if "QCD" in dataset: continue
        if "data" in dataset: continue
        h = histos[cut+var+jt+iso+dataset]
        print dataset, h.Integral()
        stack.Add(h)
        #hQCD.SetNameTitle("%s__QCD" % var, "%s__QCD" % var)
    print "QCD", hQCD.Integral()
    stack.Add(hQCD)
    return (hData, stack)

def make_legend(hData, stack, varname):
    if varname in ["aplanarity", "bdt_sig_bg", "bjet_mass", "bjet_pt", "D", "hadronic_mass", "hadronic_pt", "ht", "lepton_pt", "ljet_mass", "ljet_pt", "met", "mtw", "shat_mass", "shat_pt", "shat", "sphericity", "top_mass", "top_pt", "w_pt"]:
        leg = ROOT.TLegend(0.8,0.6,1.0,0.90)
    else:
        leg = ROOT.TLegend(0.1,0.6,0.3,0.90)
    #leg.SetTextSize(0.037)
    leg.SetBorderSize(1)
    leg.SetLineStyle(0)
    leg.SetTextSize(0.025)
    leg.SetFillColor(0)
    
    leg.AddEntry(hData,"Data","ple")
    for h in stack.GetHists():
        dsname = h.GetName().split("__")[-1]
        if dsname in legend_names:
            leg.AddEntry(h, legend_names[dsname],"f")
    return leg

def make_templates_legend(histos):
    leg = ROOT.TLegend(0.1,0.75,0.4,0.90)
    #leg.SetTextSize(0.037)
    leg.SetBorderSize(1)
    leg.SetLineStyle(0)
    leg.SetTextSize(0.025)
    leg.SetFillColor(0)
    
    for (key, h) in histos.items():
        #print g.GetName()
        leg.AddEntry(h, key.replace("qcdcut", "after QCD BDT cut").replace("nocut", "no QCD cut").replace("bdtcut", "after signal BDT cut"),"ple")
    return leg


def plot_stack(hData, stack, channel, varname, jt, cut, iso):
    canv1 = TCanvas(channel+varname+jt+cut, channel+varname+jt+cut, 800,800)
    #h.SetAxisRange(0, 0.25, "Y")
    hData.GetXaxis().SetTitle(varname)
    hData.SetAxisRange(0, 1.1*max(hData.GetBinContent(hData.GetMaximumBin()), stack.GetMaximum()), "Y")
    title = hData.GetTitle().split("__")
    print title
    name = "%s, %s, %s, %s, %s" % (title[3], title[2], title[4], title[5], title[1].replace("qcdcut_old", "above old QCD BDT cut").replace("qcdcut", "above QCD BDT cut").replace("nocut", "no QCD cut").replace("reversecut", "below QCD BDT cut"))
    hData.SetTitle(name)    
    hData.Draw("e1")
    stack.Draw("same hist")
    hData.Draw("same e1")                                                         
    #hQCD.SetLineWidth(2)
    legend = make_legend(hData, stack, varname)
    legend.Draw()

    canv1.SaveAs("plots/"+varname+"_stack_"+channel+"_"+jt+"_"+cut+"_"+iso+".pdf")
    canv1.SaveAs("plots/"+varname+"_stack_"+channel+"_"+jt+"_"+cut+"_"+iso+".png")

def plot_templates(templates, stacks, channel, var, jt, iso=None):
    canv1 = TCanvas(channel+var+jt, channel+var+jt, 800,800)
    #h.SetAxisRange(0, 0.25, "Y")
    first = True
    for (key, template) in templates.items():
        if not stacks == None:
            subtract_MC_with_stack(template, stacks[key])
        template.GetXaxis().SetTitle(var)
        template.SetLineColor(cut_colors[key])
        if template.Integral() > 0:
            template.Scale(1 / template.Integral())
        if first:
            template.SetAxisRange(0, min(0.6, max(0.5, 2*template.GetBinContent(template.GetMaximumBin()))), "Y")
            template.SetTitle("Template comparison with different cuts, %s, %s, %s" % (channel, jt, var))
            if stacks == None:
                template.SetTitle(template.GetTitle()+", MC QCD, %s" % (iso))
            template.Draw("e1 hist")
            first = False
        else:
            template.Draw("e1 hist same")
    legend = make_templates_legend(templates)
    legend.Draw()

    name = "template_plots_reproc/"+var+"_templates_"+channel+"_"+jt
    if stacks == None:
        name = name + "_QCD_MC_"+iso
    canv1.SaveAs(name+".pdf")
    canv1.SaveAs(name+".png")

def plot_template(hData, stack, channel, var, jt, cut):
    canv1 = TCanvas(channel+varname+jt+cut, channel+varname+jt+cut, 800,800)
    #h.SetAxisRange(0, 0.25, "Y")
    
    subtract_MC_with_stack(hData, stack)
    hData.GetXaxis().SetTitle(varname)
    hData.SetAxisRange(0, 1.1*hData.GetBinContent(hData.GetMaximumBin()), "Y")
    title = hData.GetTitle().split("__")
    if hData.Integral() > 0:
        hData.Scale(1./hData.Integral())
    print title
    #name = "%s, %s, %s, %s, %s" % (title[3], title[2], title[4], title[5], title[1].replace("qcdcut", "above QCD BDT cut").replace("nocut", "no QCD cut").replace("reversecut", "below QCD BDT cut"))
    #hData.SetTitle(name)    
    hData.Draw("e1")
    #legend = make_legend(hData, stack)
    #legend.Draw()

    canv1.SaveAs("template_plots/"+varname+"_template_"+channel+"_"+jt+"_"+cut+".pdf")
    canv1.SaveAs("template_plots/"+varname+"_template_"+channel+"_"+jt+"_"+cut+".png")                      



if __name__=="__main__":
    #parser = argparse.ArgumentParser(description='')
    #parser.add_argument('--path', dest='path', default="/".join([os.environ["STPOL_DIR"], "src", "qcd_ntuples", "histos"]))
    #parser.add_argument('--channel', dest='channel' , default='mu')
    #args = parser.parse_args()
    ROOT.TH1.AddDirectory(False)
    ROOT.gROOT.SetStyle("Plain")
    ROOT.gStyle.SetOptStat(0)
    ROOT.gROOT.SetBatch()
    for iso in ["iso"]:#, "antiiso"]:
        for channel in ["mu", "ele"]:
            #added = "02_10_newvars"
            added = "Jan11_deltaR"
            histos = get_histos("var_histos/%s/%s.root" % (added, channel), channel)  
            for varname in variables:
                for jt in ["2j1t"]:#, "2j0t", "3j1t", "3j2t"]:
                    templates = {}
                    stacks = {}
                    for cut in ["bdtcut"]:#["qcdcut", "qcdcut_new", "nocut", "reversecut", "bdtcut", "bdtcut_old"]:
                        #outfile = TFile("templates/%s__%s__%s__%s__%s__%s.root" % (varname, jt, channel, cut, added, iso), "recreate")
                        (hData, stack) = make_stack(histos, channel, varname, jt, cut, iso)
                        plot_stack(hData, stack, channel, varname, jt, cut,iso)    
                        if cut != "reversecut" and not (cut == "bdtcut" and varname == "bdt_sig_bg"):
                            templates[cut] = hData    
                            stacks[cut] = stack
                    #plot_templates(templates, stacks, channel, varname, jt)
                    #outfile.Close()
    """for iso in ["iso", "antiiso"]:
        for channel in ["mu", "ele"]:
            added = "15_09_elemtw"
            histos = get_histos("var_histos/%s/%s.root" % (added, channel), channel)  
            for var in variables:
                for jt in ["2j0t", "2j1t", "3j1t", "3j2t"]:
                    templates = {}
                    stacks = {}
                    for cut in ["qcdcut", "nocut", "bdtcut"]:                        
                        hQCD = histos[cut+var+jt+iso+"QCD"]                        
                        if cut != "reversecut" and not (cut == "bdtcut" and var == "bdt_sig_bg"):
                            templates[cut] = hQCD

                    plot_templates(templates, None, channel, var, jt, iso)"""
