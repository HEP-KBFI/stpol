from make_histos import eta_bins, pt_bins
import ROOT
from ROOT import TFile
import os
flavours = ["b", "c", "uds", "g", "undefined", "l"]
datasets = ["tchan", "ttjets", "wjets"]
#effs[jets][flavour] = Hist2D(pt_bins, eta_bins, name = title, title = title, type='D')


def plot_stuff():

    effs = {}
    effs_old = {}
    for dataset in ["tchan", "ttjets", "wjets"]:
        effs[dataset] = {}
        effs_old[dataset] = {}
        infile = TFile(os.path.join(os.environ["STPOL_DIR"], "src/btag_effs/eff_histos/", "%s.root" % (dataset)))
        infile_old = TFile(os.path.join(os.environ["STPOL_DIR"], "CMSSW/src/data/b_eff_hists/nocut/", "%s.root" % (dataset)))
        for jets in [2,3]:
            effs[dataset][jets] = {}
            effs_old[dataset][jets] = {}
            for flavour in flavours:
                title = "eff_%s" % flavour
                if flavour not in ["l"]:
                    effs[dataset][jets][flavour] = infile.Get("%dJ/eff_%s" % (jets, flavour))
                if flavour not in ["uds", "g", "undefined"]:
                    effs_old[dataset][jets][flavour] = infile_old.Get("%dJ/eff_%s" % (jets, flavour))

    effs_pt = {}
    effs_eta = {}
    for dataset in ["tchan", "ttjets", "wjets"]:
        effs_pt[dataset] = {}
        effs_eta[dataset] = {}
        infile = TFile(os.path.join(os.environ["STPOL_DIR"], "src/btag_effs/eff_histos/", "%s.root" % (dataset)))
        for jets in [2,3]:
            effs_pt[dataset][jets] = {}
            effs_eta[dataset][jets] = {}
            for flavour in flavours:
                title = "eff_%s" % flavour
                effs_pt[dataset][jets][flavour] = infile.Get("%dJ/pt_eff_%s" % (jets, flavour))
                effs_eta[dataset][jets][flavour] = infile.Get("%dJ/eta_eff_%s" % (jets, flavour))

    compare_to_old(effs, effs_old)
    plot_comps(effs_pt, "pt")    
    plot_comps(effs_eta, "eta")            


def compare_to_old(effs, effs_old):
    outfile = "plots"
    for jets in [2,3]:
        for flavour in ["b", "c", "l"]:
            for ds in datasets:
                canv = ROOT.TCanvas()
                effs_old[ds][jets][flavour].SetTitle("B-tagging efficiency ratio in %d-jet events for true %s-jets, %s" % (jets, flavour, ds))
                if flavour == "l":
                    effs_old[ds][jets][flavour].Divide(effs[ds][jets]["uds"])
                else:
                    effs_old[ds][jets][flavour].Divide(effs[ds][jets][flavour])
                print effs_old[ds][jets][flavour].GetMinimum(), effs_old[ds][jets][flavour].GetMaximum()
                effs_old[ds][jets][flavour].SetMinimum(0)
                effs_old[ds][jets][flavour].SetMaximum(2)
                effs_old[ds][jets][flavour].Draw("colz")
                outfile = "plots/effs_ratio_%s_%dJ_%s" % (ds, jets, flavour)
                canv.Print(outfile + ".png")
                canv.Print(outfile + ".pdf")
    
    for jets in [2,3]:
        for ds in ["ttjets", "tchan"]:
            for flav in ["b", "c"]:
                canv = ROOT.TCanvas()
                ratio = effs["wjets"][jets][flav].Clone()
                ratio.SetTitle("B-tagging efficiency ratio in %d-jet events for true %s-jets, wjets/%s" % (jets, flav, ds))
                ratio.Divide(effs[ds][jets][flav])
                ratio.SetMinimum(0.7)
                ratio.SetMaximum(1.3)
                ratio.Draw("colz")
                outfile = "plots/effs_ratio_wjets_%s_%dJ_%s" % (ds, jets, flav)
                canv.Print(outfile + ".png")
                canv.Print(outfile + ".pdf")      
"""profx = effs_old[ds][jets][flavour].ProfileX()
                profx.GetXaxis().SetTitle("Pt")
                profx.SetTitle("B-tagging efficiency ratio (new/old) in %d-jet events for true %s-jets, %s" % (jets, flavour, ds))
                profx.Draw()
                outfile = "plots/effs_ratio_pt_%s_%dJ_%s" % (ds, jets, flavour)
                canv.Print(outfile + ".png")
                canv.Print(outfile + ".pdf")
                profy = effs_old[ds][jets][flavour].ProfileY()
                profy.GetXaxis().SetTitle("Eta")
                profy.SetTitle("B-tagging efficiency ratio (new/old) in %d-jet events for true %s-jets, %s" % (jets, flavour, ds))
                profy.Draw()
                outfile = "plots/effs_ratio_eta_%s_%dJ_%s" % (ds, jets, flavour)
                canv.Print(outfile + ".png")
                canv.Print(outfile + ".pdf")"""         
    
def plot_comps(effs, var):
    
    """hs.SetTitle("Stack scaled to fit results")
    hs.SetMaximum(hs.GetMaximum()*1.25)
    hs.Draw("BAR HIST")
    hs.GetXaxis().SetTitle(axis_name[hn])
    #hs.Draw("BAR HIST")
    hists["DATA"].Draw("E1 SAME")
    """
    
    outfile = "plots"
    for jets in [2,3]:
        for flavour in ["b", "c"]:
            canv = ROOT.TCanvas()
            effs["tchan"][jets][flavour].SetLineColor(ROOT.kRed)
            effs["tchan"][jets][flavour].SetTitle("B-tagging efficiency in %d-jet events for true %s-jets" % (jets, flavour))
            effs["ttjets"][jets][flavour].SetLineColor(ROOT.kOrange)
            effs["wjets"][jets][flavour].SetLineColor(ROOT.kGreen)
            effs["tchan"][jets][flavour].SetMarkerColor(ROOT.kRed)
            effs["ttjets"][jets][flavour].SetMarkerColor(ROOT.kOrange)
            effs["wjets"][jets][flavour].SetMarkerColor(ROOT.kGreen)
            effs["tchan"][jets][flavour].GetXaxis().SetTitle(var)
    
            for ds in datasets:
                effs[ds][jets][flavour].SetLineWidth(2)
            
            #effs["tchan"][jets][flavour].SetMaximum(effs["tchan"][jets][flavour].GetMaximum()*1.25)
            if var == "eta": 
                effs["tchan"][jets][flavour].SetAxisRange(0, effs["wjets"][jets][flavour].GetMaximum()*1.5, "Y")
            if var == "pt":
                effs["tchan"][jets][flavour].SetAxisRange(0, effs["tchan"][jets][flavour].GetMaximum()*1.5, "Y")
            effs["tchan"][jets][flavour].Draw()
            effs["ttjets"][jets][flavour].Draw("same")
            effs["wjets"][jets][flavour].Draw("same")
            leg = make_legend(effs, jets, flavour)
            leg.Draw()
            outfile = "plots/effs_%s_%dJ_%s" % (var, jets, flavour)
            canv.Print(outfile + ".png")
            canv.Print(outfile + ".pdf")
        #light
        canv = ROOT.TCanvas()
        for flavour in ["uds", "g", "l", "undefined"]:
            effs["tchan"][jets][flavour].SetLineColor(ROOT.kRed)
            effs["tchan"][jets][flavour].SetTitle("B-tagging efficiency in %d-jet events for true  light jets" % (jets))
            effs["ttjets"][jets][flavour].SetLineColor(ROOT.kOrange)
            effs["wjets"][jets][flavour].SetLineColor(ROOT.kGreen)
            effs["tchan"][jets][flavour].SetMarkerColor(ROOT.kRed)
            effs["ttjets"][jets][flavour].SetMarkerColor(ROOT.kOrange)
            effs["wjets"][jets][flavour].SetMarkerColor(ROOT.kGreen)
            effs["tchan"][jets][flavour].GetXaxis().SetTitle(var)
            for ds in datasets:
                effs[ds][jets][flavour].SetLineWidth(2)
            if var == "eta": 
                effs["tchan"][jets][flavour].SetAxisRange(0, effs["tchan"][jets][flavour].GetMaximum()*4.2, "Y")
            if var == "pt":
                if jets == 3:
                    effs["tchan"][jets][flavour].SetAxisRange(0, effs["tchan"][jets][flavour].GetMaximum()*0.1, "Y")
                if jets == 2:
                    effs["tchan"][jets][flavour].SetAxisRange(0, effs["tchan"][jets][flavour].GetMaximum()*1.2, "Y")
        effs["tchan"][jets]["uds"].Draw()
        for flavour in ["uds", "g", "l"]:#, "undefined"]:        
            for ds in datasets:
                if flavour == "g":
                    effs[ds][jets][flavour].SetLineStyle(2)
                    effs[ds][jets][flavour].SetMarkerStyle(26)
                elif flavour == "l":
                    effs[ds][jets][flavour].SetLineStyle(3)
                    effs[ds][jets][flavour].SetMarkerStyle(5)
                
                effs[ds][jets][flavour].Draw("same")
        for ds in datasets:
            print "KS", "uds-g", ds, var, jets, effs[ds][jets]["uds"].KolmogorovTest(effs[ds][jets]["g"])
            print "KS", "uds-l", ds, var, jets, effs[ds][jets]["uds"].KolmogorovTest(effs[ds][jets]["l"])
            print "KS", "g-l", ds, var, jets, effs[ds][jets]["g"].KolmogorovTest(effs[ds][jets]["l"])
        leg = make_legend_light(effs, jets)
        leg.Draw()
        outfile = "plots/effs_%s_%dJ_%s" % (var, jets, "light")
        canv.Print(outfile + ".png")
        canv.Print(outfile + ".pdf")
        
    
def make_legend(effs, jets, flavour):
    leg = ROOT.TLegend(0.7,0.7,0.9,0.90)
    leg.SetBorderSize(1)
    leg.SetLineStyle(0)
    leg.SetTextSize(0.04)
    leg.SetFillColor(0)
    leg.AddEntry(effs["tchan"][jets][flavour],"t-channel", "lp")
    leg.AddEntry(effs["ttjets"][jets][flavour],"ttbar", "lp")
    leg.AddEntry(effs["wjets"][jets][flavour],"W+Jets", "lp")
    return leg

def make_legend_light(effs, jets):
    leg = ROOT.TLegend(0.7,0.6,0.9,0.90)
    leg.SetBorderSize(1)
    leg.SetLineStyle(0)
    leg.SetTextSize(0.03)
    leg.SetFillColor(0)
    for fl in ["uds", "g", "l"]:#, "undefined"]:
        leg.AddEntry(effs["tchan"][jets][fl],"t-channel, %s" % fl, "lp")
        leg.AddEntry(effs["ttjets"][jets][fl],"ttbar, %s" % fl, "lp")
        leg.AddEntry(effs["wjets"][jets][fl],"W+Jets, %s" % fl, "lp")
    return leg
    
if __name__ == "__main__":
    ROOT.TH1.AddDirectory(False)
    ROOT.TH2.AddDirectory(False)
    ROOT.gROOT.SetStyle("Plain")
    ROOT.gStyle.SetOptStat(0)
    #ROOT.gROOT.SetBatch()
    plot_stuff()
