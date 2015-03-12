#!/usr/bin/python
# -*- coding: utf-8 -*-

import math

from ROOT import *

#from Variable import *
#from DatasetGroup import *
#from plots.common.legend import legend
#from plots.common.utils import lumi_textbox
#from plots.common.tdrstyle import *
import os
import logging
#from plots.common.distribution_plot import plot_hists
from QCDFit import QCDFit

def get_cut(var, channel):
    if var == "met":
        return 45
    if var == "mtw":
        return 50
    if var == "qcd_mva":
        if channel == "mu":
            return -0.15
        else:
            return 0.15
    """if var == "qcd_mva_deltaR":
        if channel == "mu":
            return -0.15
        else:
            return 0.15
    """

def analyze_fit(fit_templates_file, qcd_result, other_results, priors, extra = {}):
    templates_file = fit_templates_file.replace("reversecut", "nocut").replace("qcdcut", "nocut")#.replace("__isovar_down","").replace("__isovar_up","")
    var = templates_file.split("/")[1].split("__")[0]
    jt = templates_file.split("/")[1].split("__")[1]
    channel = templates_file.split("/")[1].split("__")[2]
    reg = fit_templates_file.split("/")[1].split("__")[3]
    f = TFile(templates_file)

    fit = QCDFit(channel = channel, jt = jt, cut = reg, var = var)
    fit.extras = extra    

    hData = TH1D(f.Get(var+"__DATA"))
    hQCDTemplate = TH1D(f.Get(var+"__QCD"))
    #print qcd_result    
    print "analyse initial"    
    print "QCD:", hQCDTemplate.Integral()
    print "Data:", hData.Integral()
    #print "other", hNonQCD.Integral()
    #print "total", hTotal.Integral()
    
    
    hQCDTemplate.Scale(qcd_result[0])
    hTotal = TH1D(hQCDTemplate)
    #print "QCD:", hQCDTemplate.Integral()

    

    cut = get_cut(var, channel)
    for bin in range(hData.GetNbinsX()+2):
        if abs(hData.GetBinLowEdge(bin) - cut) < 1e-8:
            low = bin
            break      
    high = hData.GetNbinsX()+1

    other_templates = {}
    #print other_results  

    fit.result = {} 
    for temp in other_results.keys():
        other_templates[temp] = TH1D(f.Get(var+"__"+temp))
        sf = math.e**(other_results[temp][0] * priors[temp])
        other_templates[temp].Scale(sf)
        hTotal.Add(other_templates[temp])

        delta_sf = math.e**((other_results[temp][0] + abs(other_results[temp][1])) * priors[temp]) - sf
        nonqcd_yield = other_templates[temp].Integral()
        yield_var = other_templates[temp].Integral() * delta_sf / sf
        nonqcd_yield_cut = other_templates[temp].Integral(low, high)
        yield_var_cut = other_templates[temp].Integral(low, high) * delta_sf / sf
        fit.result[temp] = {}
        fit.result[temp]["sf"] = sf
        fit.result[temp]["delta_sf"] = delta_sf
        fit.result[temp]["yield"] = nonqcd_yield
        fit.result[temp]["delta_yield"] = yield_var
        fit.result[temp]["yield_cut"] = nonqcd_yield_cut
        fit.result[temp]["delta_yield_cut"] = yield_var_cut
        #print "SF",  temp, other_templates[temp].Integral()
    chi2 = hData.Chi2Test(hTotal, "UW CHI2/NDF")
    fit.chi2 = chi2
    

    qcd_yield = hQCDTemplate.Integral()# * qcd_result[0] 
    yield_var = 0
    yield_var_cut = 0.
    qcd_yield_cut = hQCDTemplate.Integral(low, high)# * qcd_result[0]

    if qcd_result[0] > 0:
        #print "III",templates_file
        #print "III", hQCDTemplate.Integral(low, high), hQCDTemplate.Integral(), abs(qcd_result[1]) / qcd_result[0]
        yield_var = hQCDTemplate.Integral() * abs(qcd_result[1]) / qcd_result[0]    #CHECK NEG VARIATIONS
        yield_var_cut = hQCDTemplate.Integral(low, high) * abs(qcd_result[1]) / qcd_result[0]
    
    fit.result["QCD"] = {}
    fit.result["QCD"]["sf"] = qcd_result[0]
    fit.result["QCD"]["delta_sf"] = abs(qcd_result[1])
    fit.result["QCD"]["yield"] = qcd_yield
    fit.result["QCD"]["delta_yield"] = yield_var
    fit.result["QCD"]["yield_cut"] = qcd_yield_cut
    fit.result["QCD"]["delta_yield_cut"] = yield_var_cut
    
    print "analyse final"    
    print "QCD:", qcd_yield
    print "Data:", hData.Integral()
    #print "other", hNonQCD.Integral()
    print "total", hTotal.Integral()


    return fit


"""
def analyze_fit(fit_templates_file, qcd_result, other_results, priors, extra = {}):
    templates_file = fit_templates_file.replace("reversecut", "nocut").replace("qcdcut", "nocut")
    var = templates_file.split("/")[1].split("__")[0]
    jt = templates_file.split("/")[1].split("__")[1]
    channel = templates_file.split("/")[1].split("__")[2]
    reg = fit_templates_file.split("/")[1].split("__")[3]
    f = TFile(templates_file)

    extra_string = ""
    for k,v in extra.items():
        vark = k.replace("varMC_QCDMC",", QCD from MC").replace("varMC_",", MC antiiso").replace("isovar", "Anti-iso range")
        extra_string += "%s %s" % (vark,v)
        #

    display_var = var.replace("qcd_mva", "QCD BDT")
    region = "full variable range"
    if reg == "qcdcut":
        region = "above QCD cut"
    elif reg == "reversecut":
        region = "below QCD cut"

    hData = TH1D(f.Get(var+"__DATA"))
    hQCDTemplate = TH1D(f.Get(var+"__QCD"))
    #print qcd_result    
    hQCDTemplate.Scale(qcd_result[0])
    hTotal = TH1D(hQCDTemplate)
    #print "QCD:", hQCDTemplate.Integral()

    cut = get_cut(var, channel)
    for bin in range(hData.GetNbinsX()+2):
        if abs(hData.GetBinLowEdge(bin) - cut) < 1e-8:
            low = bin
            break      
    high = hData.GetNbinsX()+1

    other_templates = {}
    #print other_results   
    for temp in other_results.keys():
        other_templates[temp] = TH1D(f.Get(var+"__"+temp))
        #print other_templates[temp].Integral(),  other_results[temp][0], priors[temp]
        sf = math.e**(other_results[temp][0] * priors[temp])
        other_templates[temp].Scale(sf)

        hTotal.Add(other_templates[temp])
        #print "SF",  temp, other_templates[temp].Integral()
    chi2 = hData.Chi2Test(hTotal, "UW CHI2/NDF")
    #print "chi2", chi2
    qcd_yield = hQCDTemplate.Integral() * qcd_result[0] 
    yield_var = 0
    yield_var_cut = 0.
    qcd_yield_cut = hQCDTemplate.Integral(low, high) * qcd_result[0]

    if qcd_result[0] > 0:
        #print "III",templates_file
        #print "III", hQCDTemplate.Integral(low, high), hQCDTemplate.Integral(), abs(qcd_result[1]) / qcd_result[0]
        yield_var = hQCDTemplate.Integral() * abs(qcd_result[1])# / qcd_result[0]    #CHECK NEG VARIATIONS
        yield_var_cut = hQCDTemplate.Integral(low, high) * abs(qcd_result[1])# / qcd_result[0]
    if not extra is None and len(extra) > 0:
        table = "%s & %s & %s & %s & QCD: $%.3f \\pm %.3f$ & $%.0f \\pm %.0f$ & $%.1f \\pm %.1f$ & $%.1f$ \\\\ \n" % (display_var, channel, region, extra_string, qcd_result[0], abs(qcd_result[1]), qcd_yield, yield_var, qcd_yield_cut, yield_var_cut, chi2)
    else:
        table = "%s & %s & %s & QCD: $%.3f \\pm %.3f$ & $%.0f \\pm %.0f$ & $%.1f \\pm %.1f$ & $%.1f$ \\\\ \n" % (display_var, channel, region, qcd_result[0], abs(qcd_result[1]), qcd_yield, yield_var, qcd_yield_cut, yield_var_cut, chi2)
    
    for temp in other_results.keys():
        sf = math.e**(other_results[temp][0] * priors[temp])
        delta_sf = math.e**((other_results[temp][0] + abs(other_results[temp][1])) * priors[temp]) - sf
        nonqcd_yield = other_templates[temp].Integral()
        yield_var = other_templates[temp].Integral() * delta_sf / sf
        nonqcd_yield_cut = other_templates[temp].Integral(low, high)
        yield_var_cut = other_templates[temp].Integral(low, high) * delta_sf / sf
        if len(extra) > 0:
            table += " & & & %s: $%.3f \\pm %.3f$ & $%.0f \\pm %.0f$ & $%.1f \\pm %.1f$ & \\\\ \n" % (temp.replace("_","-"), sf, delta_sf, nonqcd_yield, yield_var, nonqcd_yield_cut, yield_var_cut)
        else:
            table += " & & %s: $%.3f \\pm %.3f$ & $%.0f \\pm %.0f$ & $%.1f \\pm %.1f$ & \\\\ \n" % (temp.replace("_","-"), sf, delta_sf, nonqcd_yield, yield_var, nonqcd_yield_cut, yield_var_cut)
    if table == None:
        print var, jt, channel, reg
        print "bummer"
        sys.exit()
    return table
"""
"""
def plot_fit(hData, hQCD, hOthers, qcd_result, other_results):
    tdrstyle()
    gStyle.SetOptTitle(0) #1
    #canvases = []
    
    f2 = TFile(outfile_wd, "recreate")
    f2.cd()

    try:
        os.mkdir("fit_plots")
    except Exception as e:
        logging.warning(str(e))

    outfile_name = "fit_plots/"+var.shortName+"_Fit_"+jt+"_"+channel+"_"+cutid

    qcdsf = hQCD.Integral()/hQCDTemplate.Integral()
    print "templates: ",hData.Integral(), hQCD.Integral(), hQCDTemplate.Integral(), hNonQCD.Integral()
    

    print fit_result
    QCDRATE = fit_result.qcd
    #QCDRATE_UP = fit_result.qcd * math.e**((fit_result.result["qcd"]["beta_signal"][0][0]+fit_result.result["qcd"]["beta_signal"][0][1])) / math.e**((fit_result.result["qcd"]["beta_signal"][0][0]))
    qcdsf_up = fit_result.result["qcd"]["beta_signal"][0][0] + fit_result.result["qcd"]["beta_signal"][0][1]
    QCDRATE_UP = fit_result.qcd * (qcdsf_up / qcdsf)
	#QCDRATE_DOWN = fit_result.qcd * math.e**((fit_result.result["qcd"]["beta_signal"][0][0]-fit_result.result["qcd"]["beta_signal"][0][1])) / math.e**((fit_result.result["qcd"]["beta_signal"][0][0]))
    qcdsf_down = fit_result.result["qcd"]["beta_signal"][0][0] - fit_result.result["qcd"]["beta_signal"][0][1]
    QCDRATE_DOWN = fit_result.qcd * (qcdsf_down / qcdsf)
    #NONQCDRATE = fit_result.nonqcd
    #NONQCDRATE_UP = fit_result.nonqcd + fit_result.nonqcd_uncert
    #NONQCDRATE_DOWN = fit_result.nonqcd - fit_result.nonqcd_uncert
    NONQCDRATE = math.e**((fit_result.result["qcd"]["nonqcd_rate"][0][0])*fit_result.coeff["nonqcd"])
    NONQCDRATE_UP = math.e**((fit_result.result["qcd"]["nonqcd_rate"][0][0]+fit_result.result["qcd"]["nonqcd_rate"][0][1])*fit_result.coeff["nonqcd"])
    NONQCDRATE_DOWN = math.e**((fit_result.result["qcd"]["nonqcd_rate"][0][0]-fit_result.result["qcd"]["nonqcd_rate"][0][1])*fit_result.coeff["nonqcd"])


    #WJETS = fit_result.wjets
    #WJETS_UP = fit_result.wjets + fit_result.wjets_uncert
    #WJETS_DOWN = fit_result.wjets - fit_result.wjets_uncert
"""

"""
def plot_fit2(channel, var, fitConf, fit_result, lumi, jt, cutid):
    print channel, jt    
    tdrstyle()
    gStyle.SetOptTitle(1)
    canvases = []
    infile = "fits/"+var.shortName+"_fit_"+jt+"_"+channel+"_"+cutid+".root"
    infile2 = "templates/"+var.shortName+"_templates_"+jt+"_"+channel+"_"+cutid+".root"
    cutinfo = "_".join(cutid.split("_")[1:])
    infile3 = "templates/"+var.shortName+"_templates_"+jt+"_"+channel+"_nocut_"+cutinfo+".root"
    outfile_wd = "fits/"+var.shortName+"_fit_"+jt+"_"+channel+"_"+cutid+"_withData.root"
    f = TFile(infile)
    f0 = TFile(infile2)
    f3 = TFile(infile3)
    f2 = TFile(outfile_wd, "recreate")
    f2.cd()

    try:
        os.mkdir("fit_plots")
    except Exception as e:
        logging.warning(str(e))

    outfile_name = "fit_plots/"+var.shortName+"_Fit_"+jt+"_"+channel+"_"+cutid

    hData = TH1D(f0.Get(var.shortName+"__DATA"))
    hQCDTemplate = TH1D(f0.Get(var.shortName+"__qcd"))
    hQCDTemplateNocut = TH1D(f3.Get(var.shortName+"__qcd"))
    hQCD = f.Get(var.shortName+"__qcd")
    hNonQCD = TH1D(f.Get(var.shortName+"__nonqcd"))
    qcdsf = hQCD.Integral()/hQCDTemplate.Integral()
    print "templates: ",hData.Integral(), hQCD.Integral(), hQCDTemplate.Integral(), hNonQCD.Integral()
    

    print fit_result
    QCDRATE = fit_result.qcd
    #QCDRATE_UP = fit_result.qcd * math.e**((fit_result.result["qcd"]["beta_signal"][0][0]+fit_result.result["qcd"]["beta_signal"][0][1])) / math.e**((fit_result.result["qcd"]["beta_signal"][0][0]))
    qcdsf_up = fit_result.result["qcd"]["beta_signal"][0][0] + fit_result.result["qcd"]["beta_signal"][0][1]
    QCDRATE_UP = fit_result.qcd * (qcdsf_up / qcdsf)
	#QCDRATE_DOWN = fit_result.qcd * math.e**((fit_result.result["qcd"]["beta_signal"][0][0]-fit_result.result["qcd"]["beta_signal"][0][1])) / math.e**((fit_result.result["qcd"]["beta_signal"][0][0]))
    qcdsf_down = fit_result.result["qcd"]["beta_signal"][0][0] - fit_result.result["qcd"]["beta_signal"][0][1]
    QCDRATE_DOWN = fit_result.qcd * (qcdsf_down / qcdsf)
    #NONQCDRATE = fit_result.nonqcd
    #NONQCDRATE_UP = fit_result.nonqcd + fit_result.nonqcd_uncert
    #NONQCDRATE_DOWN = fit_result.nonqcd - fit_result.nonqcd_uncert
    NONQCDRATE = math.e**((fit_result.result["qcd"]["nonqcd_rate"][0][0])*fit_result.coeff["nonqcd"])
    NONQCDRATE_UP = math.e**((fit_result.result["qcd"]["nonqcd_rate"][0][0]+fit_result.result["qcd"]["nonqcd_rate"][0][1])*fit_result.coeff["nonqcd"])
    NONQCDRATE_DOWN = math.e**((fit_result.result["qcd"]["nonqcd_rate"][0][0]-fit_result.result["qcd"]["nonqcd_rate"][0][1])*fit_result.coeff["nonqcd"])


    #WJETS = fit_result.wjets
    #WJETS_UP = fit_result.wjets + fit_result.wjets_uncert
    #WJETS_DOWN = fit_result.wjets - fit_result.wjets_uncert
    
    cst = TCanvas("Histogram_","histo",10,10,1000,1000)
    cst.SetTopMargin(0.9)
    #print infile
    #print f
    #print f.Get(var.shortName+"__nonqcd")
    hNonQCD.Write()
    hNonQCD.SetTitle("Non-QCD")
    hNonQCD.SetLineColor(kRed)

    hNonQCDp=TH1D(hNonQCD)
    hNonQCDp.SetName(var.shortName+"__nonqcd__plus")
    hNonQCDp.Scale(NONQCDRATE_UP/NONQCDRATE)
    hNonQCDp.Write()
    hNonQCDm=TH1D(hNonQCD)
    
    hNonQCDm.Scale(NONQCDRATE_DOWN/NONQCDRATE)
    hNonQCDm.SetName(var.shortName+"__nonqcd__minus")
    hNonQCDm.Write()
    hNonQCDp.SetLineColor(kOrange)
    hNonQCDp.SetTitle("Non-QCD #pm 1 #sigma")
    hNonQCDm.SetLineColor(kOrange)
    hNonQCDm.SetTitle("non-QCD - 1 sigma")
    
    hData.Write()    
    hData.SetMarkerStyle(20)
     
    #print "data integral: ",hData.Integral()
    hQCD.Write()
    hQCD.SetNameTitle(var.shortName+"__qcd", "QCD")
    hQCD.SetLineColor(kYellow)

    hQCDp=TH1D(hQCD)
    hQCDp.Scale(QCDRATE_UP/QCDRATE)
    hQCDm=TH1D(hQCD)
    hQCDm.Scale(QCDRATE_DOWN/QCDRATE)
    hQCDp.SetName(var.shortName+"__qcd_plus")
    hQCDp.Write()
    hQCDm.SetName(var.shortName+"__qcd_minus")
    hQCDm.Write()

    hQCDp.SetLineColor(kGreen)
    hQCDp.SetTitle("QCD #pm 1 #sigma")
    hQCDm.SetLineColor(kGreen)
    hQCDm.SetTitle("QCD #pm 1 #sigma")
    
    hTotal=TH1D(hNonQCD)
    hTotal.Add(hQCD)
    
    print "Results with fit uncertainty included"
    qcdval = "%.2f +- %.2f" % (qcdsf, qcdsf_up - qcdsf)
    print "QCD: ", qcdval
    nonqcdval = "%.3f +- %.3f" % (NONQCDRATE, (NONQCDRATE_UP - NONQCDRATE))
    print "Non-QCD: ", nonqcdval

    chi2 = hData.Chi2Test(hTotal, "UW CHI2/NDF")
    print "chi2", chi2
    nocutScale = hQCDTemplateNocut.Integral()/hQCDTemplate.Integral()
    retval = "%s \t & %.1f +- %.1f" % (qcdval, QCDRATE * nocutScale, (QCDRATE_UP-QCDRATE)*nocutScale) #fit_result.chi2[0]
    

    #print "data", hData.Integral()
    print hTotal.Integral(), hNonQCD.Integral(), hQCD.Integral()
    #print "QCD scale factor:", hQCD.Integral()/hQCDTemplate.Integral(), "+"
    hTotal.SetLineColor(kBlue)
    hTotal.SetTitle("Fitted total")
    max_bin = hData.GetBinContent(hData.GetMaximumBin())*1.5
    hData.SetAxisRange(0, max_bin, "Y")
    hData.GetXaxis().SetTitle(var.displayName)
    #hTotal.Draw("")
    title = jt + ", "+channel
    hData.SetTitle(title)
    hData.SetMarkerStyle(20)
    #print "data", hData.Integral()
    hData.Draw("E1")
    #print "data", hData.Integral()
    hNonQCDp.Draw("same")
    hQCD.SetLineColor(kGreen+2)
    hQCD.SetLineWidth(3)
    hQCD.Draw("same")
    hNonQCD.Draw("same")
    hNonQCDm.Draw("same")
    hQCDp.Draw("same")
    hQCDm.Draw("same") 
   
    hTotal.Draw("same")
    #hData.SetTitle("QCD fit, "+title)
    hData.Draw("E1 same")

    lumibox = lumi_textbox(lumi)
    hDataCopy = TH1D(hData)
    hDataCopy.SetTitle("Data")
    
    leg = legend(
         [hDataCopy, hQCD, #hQCDp, 
            hNonQCD, #hNonQCDp, 
            hTotal],
         styles=["p", "l"],
         width=0.2
     )
"""
#print "total", hQCD.Integral(), 
#for bin in range(hQCD.GetNbinsX()):
#    print "cut at", gQCD.GetBinLowEdge(bin)
"""
    leg.Draw()

    #print hNonQCD.Integral(), hData.Integral(), hQCD.Integral(), hTotal.Integral(), hQCDp.Integral(), hQCDm.Integral()
    cst.Update()
    cst.SaveAs(outfile_name+".png")
    cst.SaveAs(outfile_name+".pdf")
    cst.Draw()
    return (cst, retval, nonqcdval)
"""
