import os
import fnmatch
from data_to_mc_switcher import *
from matching_doubler import *    

def converter(indir, outdir, mcdir):
    for root, dir, files in os.walk(indir):
        histofiles = fnmatch.filter(files, "*.root")
        #print root, dir
        for hf in histofiles:
            print hf, root, root.replace(indir, outdir)
            matching_doubler(hf, root, root.replace(indir, outdir))
            #if not "_top" in  mcdir.split("stpol_pdf")[1] and not "_antitop" in mcdir.split("stpol_pdf")[1] and not "bin" in mcdir:
            #    data_to_mc_switcher(hf, root.replace(indir, outdir), root.replace(indir, mcdir))

if __name__ == "__main__":
    """for bin in range(4,5):
        in_dir = "/home/andres/single_top/stpol_pdf/results/hists/raw_Mar30_bin%d/" % bin    
        out_dir = "/home/andres/single_top/stpol_pdf/results/hists/Mar30_bin%d/" % bin    
        out_dir_mconly = "/home/andres/single_top/stpol_pdf/results/hists/Mar30_bin%d_mconly/" %bin
        converter(in_dir, out_dir, out_dir_mconly)"""
    in_dir = "/home/andres/single_top/stpol_pdf/results/hists/raw_Apr28_lept/"
    out_dir = "/home/andres/single_top/stpol_pdf/results/hists/Apr28/"   
    out_dir_mconly = "/home/andres/single_top/stpol_pdf/results/hists/Apr28_mconly/"
    converter(in_dir, out_dir, out_dir_mconly)
