import sys
import ROOT
from ROOT import TMVA
import numpy as np

from adder import setup_mva, rv, zero_buffers, treename, mva_loop_lepton_separate, STPOL_DIR

def main():
    mvaname = sys.argv[1]
    weightname = sys.argv[2]
    infiles = sys.argv[3:]
    print infiles

    mvas = dict()
    mvas[13] = setup_mva(mvaname, STPOL_DIR + "/src/qcd_mva/weights/%s_mu.weights.xml" % weightname)
    mvas[11] = setup_mva(mvaname, STPOL_DIR + "/src/qcd_mva/weights/%s_ele.weights.xml" % weightname)

    varmaps = dict()
    varmaps[13] = {"mu_mtw":"mtw", "c":"C"}
    varmaps[11] = {"ele_mtw":"mtw", "c":"C"}

    mva_loop_lepton_separate(mvaname, infiles, mvas, varmaps)

if __name__=="__main__":
    main()
