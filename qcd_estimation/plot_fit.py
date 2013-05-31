#!/usr/bin/python
# -*- coding: utf-8 -*-

import math

from ROOT import *

from Variable import *
from DatasetGroup import *
from plots.common.legend import legend
from plots.common.utils import lumi_textbox
from plots.common.tdrstyle import *
    
def plot_fit(var, fitConf, hData, fit_result):
   tdrstyle()
   canvases = []
   infile = "fits/"+var.shortName+"_fit_"+fitConf.name+".root"
   f = TFile(infile)
   
   print fitConf.name
   outfile_name = "fit_plots/"+var.shortName+"_Fit_"+fitConf.name
   
   #print fit_result
   QCDRATE = fit_result.qcd
   QCDRATE_UP = fit_result.qcd + fit_result.qcd_uncert
   QCDRATE_DOWN = fit_result.qcd - fit_result.qcd_uncert
   NONQCDRATE = fit_result.nonqcd
   NONQCDRATE_UP = fit_result.nonqcd + fit_result.nonqcd_uncert
   NONQCDRATE_DOWN = fit_result.nonqcd - fit_result.nonqcd_uncert
        
   #print QCDRATE, QCDRATE_UP, QCDRATE_DOWN, NONQCDRATE, NONQCDRATE_UP,NONQCDRATE_DOWN
      
   cst = TCanvas("Histogram_"+fitConf.name,fitConf.name,10,10,1000,1000)
   
   hNonQCD = TH1D(f.Get(var.shortName+"__nonqcd"))
   hNonQCD.SetTitle("Non-QCD")   
   hNonQCD.SetLineColor(kRed)
      
   hNonQCDp=TH1D(hNonQCD)
   hNonQCDp.Scale(NONQCDRATE_UP/NONQCDRATE)
   hNonQCDm=TH1D(hNonQCD)
   hNonQCDm.Scale(NONQCDRATE_DOWN/NONQCDRATE)
      
   hNonQCDp.SetLineColor(kOrange)
   hNonQCDp.SetTitle("non-QCD + 1 sigma")
   hNonQCDm.SetLineColor(kOrange)
   hNonQCDm.SetTitle("non-QCD - 1 sigma")
      
   hData.SetNameTitle(var.shortName+"__DATA", "Data")
   hData.SetMarkerStyle(20)

   #print "data integral: ",hData.Integral()
   hQCD = f.Get(var.shortName+"__qcd")
   hQCD.SetNameTitle(var.shortName+"__qcd", "QCD")
   hQCD.SetLineColor(kYellow)
   hQCD.SetLineWidth(3)      
      
   hQCDp=TH1D(hQCD)
   hQCDp.Scale(QCDRATE_UP/QCDRATE)
   hQCDm=TH1D(hQCD)   
   hQCDm.Scale(QCDRATE_DOWN/QCDRATE)
      
   hQCDp.SetLineColor(kGreen)
   hQCDp.SetTitle("QCD #pm 1 sigma")
   hQCDm.SetLineColor(kGreen)
   hQCDm.SetTitle("QCD #pm 1 sigma")
      
   hTotal=TH1D(hNonQCD)
   hTotal.Add(hQCD)
   hTotal.SetLineColor(kBlue)
   max_bin = hData.GetMaximum()*1.6
   hData.SetAxisRange(0, max_bin, "Y")
   hData.GetXaxis().SetTitle(var.displayName)
   #hTotal.Draw("")
   title = fit_result.getTitle()
   hData.SetMarkerStyle(20)
   hData.Draw("E1")
   hNonQCDp.Draw("same")
   hQCD.Draw("same")
   hNonQCD.Draw("same")
   hNonQCDm.Draw("same")
   hQCDp.Draw("same")
   hQCDm.Draw("same")
   hTotal.Draw("same")
   #hData.SetTitle("QCD fit, "+title)
   hData.Draw("E1 same")

   lumibox = lumi_textbox(19739)

   leg = legend(
        [hData, hQCD, hNonQCD, hNonQCDp, hQCD, hQCDp, hTotal],
        styles=["p", "f"],
        width=0.2
    ) 

   leg.Draw()
          
   #print hNonQCD.Integral(), hData.Integral(), hQCD.Integral(), hTotal.Integral(), hQCDp.Integral(), hQCDm.Integral()
   cst.Update()
   cst.SaveAs(outfile_name+".png")
   cst.SaveAs(outfile_name+".pdf")
   cst.Draw()
   return cst
