from rootpy.io import root_open
import shutil
import os
import math

def matching_doubler(filename, path, outpath):
    #filename is varname.root
    varname = filename.split(".")[0]
    if "nopdf" in varname: return
    if "*" in varname: return
    print filename, varname
    hists = {}
    try: 
        if not os.path.isdir(outpath):
            os.makedirs(outpath)
    except OSError:
            raise
    if "tmatrix" in filename:
        shutil.copy(path+"/"+filename, outpath)
        return
    with root_open(path+"/"+filename) as f:
        outfile = root_open(outpath + "/" +filename, "RECREATE")
        for path, dirs, objects in f.walk():
            #load all histograms from file
            first = True
            for hist in objects:
                #format 3j2t_abs_lj_eta__tchan__tchan__up
                #ignore jt_var__DATA
                #print hist
                if not "DEBUG" in hist:
                    hists[hist] = f.Get(hist).Clone()
                    if "wzjets" in hist and "matching__down" in hist:
                        hists[hist].Scale(2.0)
                    elif "wzjets" in hist and "matching__up" in hist:
                        hists[hist].Scale(0.7)
                    elif "wzjets" in hist and "scale__down" in hist:
                        hists[hist].Scale(1.5)
                    elif "wzjets" in hist and "scale__up" in hist:
                        hists[hist].Scale(1.25)
                    elif "wzjets" in hist and "flavour_heavy__down" in hist:
                        hists[hist].Scale(1.65)
                    elif "wzjets" in hist and "flavour_heavy__up" in hist:
                        hists[hist].Scale(0.55)
                    elif "wjets_light" in hist and "matching__down" in hist:
                        hists[hist].Scale(2.0)
                    elif "wjets_light" in hist and "matching__up" in hist:
                        hists[hist].Scale(0.7)
                    elif "wjets_light" in hist and "scale__down" in hist:
                        hists[hist].Scale(1.5)
                    elif "wjets_light" in hist and "scale__up" in hist:
                        hists[hist].Scale(1.25)
                    #elif "wjets_light" in hist:
                    #    hists[hist].Scale(0.5) 
                    if "2j0t" in hist and "bdt_sig_bg" in hist:
                        hists[hist].Rebin(hists[hist].GetNbinsX())
                    """if "wzjets" in hist and "ele" in outpath:
                        hists[hist].Scale(1.062726)
                    if "ttjets" in hist and "ele" in outpath:
                        hists[hist].Scale(1.122156)    
                    if "wzjets" in hist and "mu" in outpath:
                        hists[hist].Scale(1.427254)
                    if "ttjets" in hist and "mu" in outpath:
                        hists[hist].Scale(1.122473)"""
    for name, h in hists.items(): 
        prefix = ""
        if "preselection" in outpath and "bdt_sig_bg" in name:
            if "_top" in outpath.split("stpol")[1]: 
                prefix = "top_"
            elif "_antitop" in outpath.split("stpol")[1]: 
                prefix = "antitop_" 
        h.SetNameTitle(prefix+name, prefix+name)      
        h.Write()
    #outfile.Write()
    outfile.Close()



if __name__ == "__main__":
    data_to_mc_switcher("bdt_sig_bg.root", "/home/andres/single_top/stpol_pdf/results/hists/Oct28_reproc/merged/preselection/3j_2t/ele/merged/", ".")


