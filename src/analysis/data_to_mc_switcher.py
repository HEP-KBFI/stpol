from rootpy.io import root_open
import shutil
import os
import math

def data_to_mc_switcher(filename, path, outpath):
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
                if not "DATA" in hist and not "DEBUG" in hist:
                    hists[hist] = f.Get(hist).Clone()                    
                    #print hist, f.Get(hist).Clone(), hists[hist]
                if first and not "DEBUG" in hist:
                    first = False
                    hn = hist.split("__")
                    jt = hn[0].split("_")[0]
        #make jt_var__DATA as sum of jt_var__[tchan+ttjets+wzjets+qcd]
        if jt+"_"+varname+"__wzjets" in hists:
            hists[jt+"_"+varname+"__DATA"] = hists[jt+"_"+varname+"__tchan"].Clone()
            hists[jt+"_"+varname+"__DATA"].Add(hists[jt+"_"+varname+"__ttjets"].Clone())
            hists[jt+"_"+varname+"__DATA"].Add(hists[jt+"_"+varname+"__wzjets"].Clone())
            #hists[jt+"_"+varname+"__DATA"].Add(hists[jt+"_"+varname+"__wjets_light"].Clone())
            hists[jt+"_"+varname+"__DATA"].Add(hists[jt+"_"+varname+"__qcd"].Clone())
        else:
            hists[jt+"_"+varname+"__DATA"] = hists[jt+"_"+varname+"__tchan"].Clone()
            hists[jt+"_"+varname+"__DATA"].Add(hists[jt+"_"+varname+"__twchan"].Clone())
            hists[jt+"_"+varname+"__DATA"].Add(hists[jt+"_"+varname+"__schan"].Clone())
            hists[jt+"_"+varname+"__DATA"].Add(hists[jt+"_"+varname+"__ttjets"].Clone())
            hists[jt+"_"+varname+"__DATA"].Add(hists[jt+"_"+varname+"__wjets"].Clone())
            hists[jt+"_"+varname+"__DATA"].Add(hists[jt+"_"+varname+"__dyjets"].Clone())
            hists[jt+"_"+varname+"__DATA"].Add(hists[jt+"_"+varname+"__diboson"].Clone())
            hists[jt+"_"+varname+"__DATA"].Add(hists[jt+"_"+varname+"__qcd"].Clone())
        #signal scaling closure test        
        #hists[jt+"_"+varname+"__tchan"].Scale(1.1)
    
    for name, h in hists.items():
        #print name, h
        h.SetNameTitle(name, name)
        if "DATA" in name:
            for bin in range(h.GetNbinsX()+2):
                h.SetBinError(bin, math.sqrt(h.GetBinContent(bin)))
        h.Write()
    outfile.Close()



if __name__ == "__main__":
    data_to_mc_switcher("bdt_sig_bg.root", "/home/andres/single_top/stpol_pdf/results/hists/Oct28_reproc/merged/preselection/3j_2t/ele/merged/", ".")


