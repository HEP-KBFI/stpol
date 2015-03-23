import ROOT
from ROOT import TFile
from os import path
import os
import sys
sys.path.append( path.dirname( path.dirname( path.dirname( path.abspath(__file__) ) ) ) )
sys.path.append( path.dirname( path.dirname( path.dirname( path.abspath(__file__) ) ) ) + "/qcd_estimation")
from fit_components import all_datasets_reproc

var = "w_pt"
jt = "2j0t"
#%FIXME load from qcd_sfs.json
qcd_sfs = {"mu":  0.909, "ele": 1.122}


def get_histos(fname, channel):
    f = TFile(fname)
    histos = {}
    #print all_datasets_reproc
    for iso in ["iso", "antiiso"]:
        for dataset in all_datasets_reproc:
            if "QCD" in dataset: continue
            name = "%s__%s__%s__%s__%s" % (var, channel, jt, iso, dataset)
            #print fname, name
            histos[iso+dataset] = f.Get(name)
            #if ("Single" in dataset or "data" in dataset) and iso == "antiiso": 
            #    histos[cut+var+jt+iso+dataset].Scale(qcd_scale_factors[channel][jt])
            #print dataset, sample_colors_same[dataset]

            #histos[cut+var+jt+iso+dataset].Rebin()
    return histos

def subtract_MC(hQCD, histos):
    for dataset in all_datasets_reproc:
        if "data" in dataset or "QCD" in dataset: continue
        h = histos["antiiso"+dataset]
        hQCD.Add(h, -1)
        
    for bin in range(hQCD.GetNbinsX()+1):
        if hQCD.GetBinContent(bin) < 0:
            hQCD.SetBinContent(bin, 0)
            hQCD.SetBinError(bin, 10.)



def make_histos(histos, channel):
    hData = histos["iso"+"data"]
    #hData.SetNameTitle("%s__DATA" % var, "%s__DATA" % var)
    
    hQCD = histos["antiiso"+"data"]
    subtract_MC(hQCD, histos)
        
    #hQCD.SetNameTitle("%s__QCD" % var, "%s__QCD" % var)
    #print hQCD.GetEntries(), hData.Integral()
    hQCD.Scale(qcd_sfs[channel])
    
    hData.Add(hQCD, -1)

    for dataset in all_datasets_reproc:
        if "Jets_exclusive" in dataset or "data" in dataset or "QCD" in dataset: continue
        h = histos["iso"+dataset]
        hData.Add(h, -1)
        
    hMC = histos["iso"+"W1Jets_exclusive"].Clone()
    hMC.Add(histos["iso"+"W2Jets_exclusive"])
    hMC.Add(histos["iso"+"W3Jets_exclusive"])
    hMC.Add(histos["iso"+"W4Jets_exclusive"])
    
    return (hData, hMC)


def calc_ratios(hData, hMC, channel):
    hData.Scale(1/hData.Integral())
    hMC.Scale(1/hMC.Integral())
    
    outfile ="/".join([os.environ["STPOL_DIR"], "results", "wjets_pt_weight", "weights_%s.csv" % channel])
    f = open(outfile, "w")
    f.write('"edges","entries", "contents"\n')
    bin_vals = []
    for bin in range(1, hData.GetNbinsX()+2):
        if hMC.GetBinContent(bin) == 0: 
            print hMC.GetBinLowEdge(bin), "div0"
        else:
            print hMC.GetBinLowEdge(bin), hData.GetBinContent(bin)/hMC.GetBinContent(bin)
            f.write("%f,%f,%f\n" % (hMC.GetBinLowEdge(bin), hData.GetBinContent(bin)/hMC.GetBinContent(bin), hData.GetBinContent(bin)/hMC.GetBinContent(bin)))
            bin_vals.append(hData.GetBinContent(bin)/hMC.GetBinContent(bin))
    f.write("Inf,0.0,0.0")
    f.close()
    print bin_vals

if __name__=="__main__":
    ROOT.TH1.AddDirectory(False)
    for channel in ["mu", "ele"]:
        print channel
        histos = get_histos("histos.root", channel)
        (hData, hMC) = make_histos(histos, channel)
        calc_ratios(hData, hMC, channel)
