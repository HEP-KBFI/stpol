from rootpy.io import root_open
import shutil
import os
import math

def check_wjets(filename):
    
    with root_open(filename) as f:
        #outfile = root_open(outpath + "/" +filename, "RECREATE")
        for path, dirs, objects in f.walk():
            #load all histograms from file
            first = True
            for hist in objects:
                #format 3j2t_abs_lj_eta__tchan__tchan__up
                #ignore jt_var__DATA
                #print hist
                if "heavy" not in hist and "light" not in hist and "W" in hist and "Jets" in hist and (("nominal" in hist or "scale" in hist or "matching" in hist) or len(hist.split("__")) == 3):
                    h = f.Get(hist)
                    print h, h.GetEntries(), h.Integral()*20000



if __name__ == "__main__":
    check_wjets("/home/andres/single_top/stpol_pdf/src/analysis/output/bdt_scan/hists/preselection/2j_1t/mu/bdt_sig_bg.root")


