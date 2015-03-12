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
            data_to_mc_switcher(hf, root.replace(indir, outdir), root.replace(indir, mcdir))

if __name__ == "__main__":
    in_dir = "/home/andres/single_top/stpol_pdf/results/hists/raw_Mar9/"    
    out_dir = "/home/andres/single_top/stpol_pdf/results/hists/Mar9/"    
    out_dir_mconly = "/home/andres/single_top/stpol_pdf/results/hists/Mar9_mconly/"
    converter(in_dir, out_dir, out_dir_mconly)
