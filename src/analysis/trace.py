from rootpy.io import root_open
import shutil
import os
import math
def tracer(filename):
    #filename is varname.root
    with root_open(filename) as f:
        for path, dirs, objects in f.walk():
            for hist in objects:
                print hist
                print f.Get("object=bdt_sig_bg_old;sample=T_t_ToLeptons_scaledown;iso=iso;systematic=scaledown;scenario=nominal;selection_major=bdt;selection_minor=-0.20000;lepton=ele;njets=2;ntags=1")#.Integral()
                f#.ReadObj(hist)


if __name__ == "__main__":
    tracer("/home/andres/single_top/stpol_pdf/src/step4/output_nomet/iso/SYST/T_t_ToLeptons_scaledown/0_output0.root")

