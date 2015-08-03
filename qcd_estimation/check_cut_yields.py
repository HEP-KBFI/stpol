#from rootpy.io import File
from os.path import join
#import argparse
#from plots.common.tdrstyle import tdrstyle
from ROOT import TCanvas, THStack, TFile, TH1D
import ROOT


from fit_components import *
from colors import *
from make_templates import add_other_components, subtract_MC
from fitted_scale_factors import *

def get_histos(fname, channel, isovar=None):
    f = TFile(fname)
    histos = {}
    for cut in ["nocut"]:
        for var in ["qcd_mva", "qcd_mva_nomet", "bdt_qcd_dphis_nomet", "bdt_qcd_dphis_withmet", "met", "mtw"]:#,"qcd_mva_new", "qcd_mva_mixed"]:
            for jt in ["2j1t", "2j0t", "3j1t", "3j2t"]:
                for iso in ["iso", "antiiso"]:
                    for dataset in all_datasets_reproc:
                        if "QCD" in dataset:continue
                        name = "qcd__%s__%s__%s__%s__%s__%s" % (cut, channel, var, jt, iso, dataset)
                        #name = "histo__%s__%s__%s__%s__%s__%s" % (cut, channel, var, jt, iso, dataset)
                        #if not ("data" in dataset or "T_t_ToLeptons" in dataset or "Tbar_t_ToLeptons" in dataset ): continue
                        #print dataset, iso
                        #if not ("data" in fname or "T_t_ToLeptons__iso" in fname or "Tbar_t_ToLeptons__iso" in fname or ("antiiso" in fname and "QCD" not in fname)): continue
                                    
                        if not isovar==None and iso == "antiiso":
                            name += "__isovar__%s" % isovar
                            #print "ISOVAR"
                        #print fname, name, cut+var+jt+iso+dataset
                        histos[cut+var+jt+iso+dataset] = f.Get(name)
                        histos[cut+var+jt+iso+dataset].SetLineColor(sample_colors_same[dataset])
                        #histos[cut+var+jt+iso+dataset].Rebin()
    return histos


def make_histos_sig_vs_qcd(histos, channel, var, jt, cut, components, isovar=None, variateMC=None):
    hData = histos[cut+var+jt+"iso"+"data"]
    print "data", isovar, hData.GetEntries(), hData.Integral()
    hData.SetNameTitle("%s__DATA" % var, "%s__DATA" % var)
    if variateMC == "QCDMC":
        hQCD = histos[cut+var+jt+"iso"+"QCD"]
    elif variateMC == "QCDMC2J0T":
        hQCD = histos[cut+var+"2j0t"+"iso"+"QCD"]
    else:
        hQCD = histos[cut+var+jt+"antiiso"+"data"]
        print "qcd", isovar, hQCD.GetEntries(), hQCD.Integral()
        subtract_MC(hQCD, histos, cut, var, jt, variateMC)
        print "qcd_sub", isovar, hQCD.GetEntries(), hQCD.Integral()
        
    hQCD.SetNameTitle("%s__QCD" % var, "%s__QCD" % var)
    print hQCD.GetEntries(), hData.Integral()
    signal = add_other_components(histos, cut, var, jt, components = "just_signal")
    return (hData, hQCD, signal)
        
    

if __name__=="__main__":
    #parser = argparse.ArgumentParser(description='')
    #parser.add_argument('--path', dest='path', default="/".join([os.environ["STPOL_DIR"], "src", "qcd_ntuples", "histos"]))
    #parser.add_argument('--channel', dest='channel' , default='mu')
    #args = parser.parse_args()
    components = "regular"

    ROOT.TH1.AddDirectory(False)
    ROOT.gROOT.SetStyle("Plain")
    ROOT.gStyle.SetOptStat(0)
    ROOT.gROOT.SetBatch()
    for channel in ["mu", "ele"]:
        total_string_bins = ""
        total_string_sig = ""
        total_string_qcd = ""
        total_string_varname = ""
        myvars = ["qcd_mva", "qcd_mva_nomet", "bdt_qcd_dphis_nomet"]#, "bdt_qcd_dphis_withmet"]
        #if channel == "ele":
        myvars.append("met")
        #if channel == "mu":
        myvars.append("mtw")
        #added = "10Nov_reproc_oldbdt" ##Nov_reproc"
        #added = "May11_nomet" ##Nov_reproc"
        added = "Jun10"
    	for varname in myvars:
            for jt in ["2j1t"]:#, "2j0t", "3j1t", "3j2t"]:
                for cut in ["nocut"]:
                    print channel, varname, jt
                    for variateMC in [None]:#, "up", "down", "QCDMC", "QCDMC2J0T"]:
                        for isovar in [None]:#, "up", "down"]:
                            histos = get_histos("input_histos/%s/%s.root" % (added, channel), channel, isovar)
                            #histos = get_histos("var_histos/%s/%s.root" % (added, channel), channel, isovar)    
                            (hData, hQCD, hSig) = make_histos_sig_vs_qcd(histos, channel, varname, jt, cut, components, isovar, variateMC)
                            #if not variateMC:
                            #    plot_QCD_template(hQCD, channel, varname, jt, cut)
                            for bin in range(hQCD.GetNbinsX()+2):
                                if hQCD.GetBinContent(bin) < 0:
                                    hQCD.SetBinContent(bin, 0) 
                            hQCD.Scale(qcd_scale_factors[channel][jt])
                            print hSig, hQCD
                            string_bins = ""
                            string_sig = ""
                            string_qcd = ""
                            string_varname = ""
                            for bin in range(0, hQCD.GetNbinsX()+2):
                    
                                print "\t %.2f:" % (hQCD.GetBinLowEdge(bin)),
                                
                                for h in [hSig[0], hQCD]:                                                        
                                    print "\t %.1f" % (h.Integral(bin, 100)),
                                print ""

                                if bin > 0:
                                    string_bins += str(hQCD.GetBinLowEdge(bin)) + ", "
                                    string_sig += str(hSig[0].Integral(bin, 100)) + ", "
                                    string_qcd += str(hQCD.Integral(bin, 100)) + ", "
                                    string_varname += varname.replace("qcd_mva_nomet", "'QCD BDT without MET'").replace("bdt_qcd_dphis_nomet", "'QCD BDT with dPhis, without MET'").replace("bdt_qcd_dphis_withmet", "'QCD BDT with dPhis & MET'").replace("qcd_mva", "'QCD BDT'").replace("met", "'MET'").replace("mtw", "'MTW'").replace("_deltaR","")+ ", "
                            #print string_bins
                            #print string_sig
                            #print string_qcd
                            #print string_varname
                            total_string_bins += string_bins
                            total_string_sig += string_sig
                            total_string_qcd += string_qcd
                            total_string_varname += string_varname
        print "TOTAL", channel
        print "bins_%s = c(%s)" % (channel, total_string_bins[:-2])
        print "signal_%s = c(%s)" % (channel, total_string_sig[:-2])
        print "qcd_%s = c(%s)" % (channel, total_string_qcd[:-2])
        print "var_%s = c(%s)" % (channel, total_string_varname[:-2])
            
        
