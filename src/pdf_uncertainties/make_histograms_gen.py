#rom get_weights import *
from utils import sizes
import os
import math
from ROOT import TFile
from parse_input import datasets, groups
import pickle
from make_histograms import make_envelope, pdf_uncertainty_nnpdf, pdf_uncertainty, CT10_alphas, CT10_total, toabsolute


C90 = 1.64485 #Conversion factor from 90% to 68%

indir = os.path.join(os.environ["STPOL_DIR"], "src", "pdf_uncertainties", "gen_output_antitop2", "added")

scale_factors = {}
scale_factors["CT10"] = 1 / C90
scale_factors["NNPDF23"] = 1.
scale_factors["MSTW2008CPdeutnlo68cl"] = 1.

variables = ["cos_theta_lj_gen"]
pdfsets = ["CT10", "MSTW2008CPdeutnlo68cl"]#, "NNPDF23"]
channels = ["mu"]#, "ele"]

def main():
    for ds in groups.keys():
        for dataset in ["T_t_ToLeptons", "Tbar_t_ToLeptons"]:
            for ch in channels:
                for var in variables:
                    make_histos(dataset, ch, var)

def test():
    #make_histos("T_t_ToLeptons", "mu", "cos_theta", "2j1t")
    #make_histos("T_s", "mu", "cos_theta", "2j1t")
    make_histos("ZZ", "mu", "bdt_sig_bg", "2j1t", "0.00000")
    #make_histos("W2Jets_Exclusive", "mu", "cos_theta", "2j1t")

def make_histos(dataset, channel, var):
    best_fits = []
    ups = []
    downs = [] 
    outdir = "histos_gen"
    print "OUT", outdir + "/%s_%s_%s_pdf_antitop.root" % (channel, dataset, var)
    outfile = TFile(outdir + "/%s_%s_%s_pdf_antitop.root" % (channel, dataset, var), "RECREATE")
    for pdf in pdfsets:
        print pdf, dataset, channel, var
        (best_fit, up, down) = make_pdf_histos(pdf, dataset, channel, var)
        best_fits.append(best_fit)
        ups.append(up)
        downs.append(down)
        best_fit.SetNameTitle("%s_best" % pdf, "%s_best" % pdf)
        up.SetNameTitle("%s_up" % pdf, "%s_up" % pdf)
        down.SetNameTitle("%s_down" % pdf, "%s_down" % pdf)
        outfile.cd()
        #best_fit.Write()
        #up.Write()
        #down.Write()
        print "integrals", pdf, best_fit.Integral(), up.Integral(), down.Integral()
    (env_best, env_up, env_down) = make_envelope(ups, downs)
    outfile.cd()
    best_name = "%s__%s__pdf__%s" % ("cos_theta_lj_gen", groups[dataset], "bestfit")    
    env_best.SetNameTitle(best_name, best_name)
    env_best.Write()
    up_name = "%s__%s__pdf__%s" % ("cos_theta_lj_gen", groups[dataset], "up")
    env_up.SetNameTitle(up_name, up_name)
    env_up.Write()
    down_name = "%s__%s__pdf__%s" % ("cos_theta_lj_gen", groups[dataset], "down")
    env_down.SetNameTitle(down_name, down_name)
    env_down.Write()
    outfile.Close()
    

def make_pdf_histos(pdfset, dataset, channel, var):
    hname_up = "%s__%s__pdf__up" % (var, "a")
    hname_down = "%s__%s__pdf__down" % (var, "b")
    
    #outfile = File(outdir + "/%s_%s.root" % (sampn,hname), "RECREATE")
    inputFile = TFile("%s/%s_%s.root" % (indir, channel, dataset))
    
    pdfsetname = pdfset+"LHgrid"
    if pdfset == "CT10" or pdfset == "MSTW2008CPdeutnlo68cl":
        weighted_histos = []
        print "%s/%s_%s.root" % (indir, channel, dataset)
        print var
        print "%s__%s__%s_nominal" % ("cos_theta_lj_gen", dataset, pdfsetname)
        best_fit = inputFile.Get( "%s__%s__%s__nominal" % ("cos_theta_lj_gen", dataset, pdfsetname) )
        print best_fit.GetEntries(), best_fit.Integral()
        for i in range(sizes[pdfsetname]):
            hist = inputFile.Get( "%s__%s__%s__weighted_%d" % ("cos_theta_lj_gen", dataset, pdfsetname, i) )
            #print "pdf__%s_%s__%s__%s_weighted_%d" % (jettag, var, dataset, pdfsetname, i)
            #print hist.GetEntries(), hist.Integral()
            weighted_histos.append(hist)
        (pdf_up, pdf_down) = pdf_uncertainty(best_fit, weighted_histos, scale_factors[pdfset])
        print pdf_up.Integral(), pdf_down.Integral()
        if pdfset == "CT10":
            alpha_down = inputFile.Get( "%s__%s__%s__weighted_%d" % (var, dataset, pdfset+"as"+"LHgrid", 2) )
            alpha_up = inputFile.Get( "%s__%s__%s__weighted_%d" % (var, dataset, pdfset+"as"+"LHgrid", 6) )
            print  "%s__%s__%s__weighted_%d" % (var, dataset, pdfset+"as"+"LHgrid", 2)
            print alpha_up, alpha_down
            (total_up, total_down) = CT10_total(best_fit, pdf_up, pdf_down, alpha_up, alpha_down)
        elif pdfset == "MSTW2008CPdeutnlo68cl": #Alphas incorporated
            print "x", type(best_fit), type(pdf_up)
            (total_up, total_down) = toabsolute(best_fit, pdf_up, pdf_down)
        print "ct10", total_up.Integral(), total_down.Integral()
    elif pdfset == "NNPDF23":
        print "%s/%s_%s.root" % (indir, channel, dataset)
        print "%s__%s__%snloas0%sLHgrid__nominal" % (var, dataset, pdfset, "119")
        hist = inputFile.Get( "%s__%s__%snloas0%sLHgrid__nominal" % (var, dataset, pdfset, "119"))
        infile = os.path.join(os.environ["STPOL_DIR"], "src", "pdf_uncertainties", "cutoffs_gen", "cutoffs_%s.pkl" % dataset)
        with open(infile, 'rb') as f:
            cutoffs = pickle.load(f)
            print "cutoff_file", infile
            #print cutoffs[dataset],
            #print cutoffs[dataset][var][channel]
            (best_fit, total_up, total_down) = pdf_uncertainty_nnpdf(hist, cutoffs[dataset][var][channel])
    #print type(best_fit), type(total_up)
    best_fit.SetDirectory(0)
    total_up.SetNameTitle(hname_up, hname_up)
    total_down.SetNameTitle(hname_down, hname_down)
    total_up.SetDirectory(0)
    total_down.SetDirectory(0)
    return (best_fit, total_up, total_down)
    

        
if __name__ == "__main__":
    main()
    #test()
