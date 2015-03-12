import sys
import os
from array import array

#Monkey-patch the system path to import the stpol header
sys.path.append(os.path.join(os.environ["STPOL_DIR"], "src/headers"))
from stpol import stpol, list_methods
from subprocess import call
import ROOT
from ROOT import TH1D, TFile
#import TMVA
# prepare the FWLite autoloading mechanism
ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()
from PhysicsTools.PythonAnalysis import *
from DataFormats.FWLite import Events, Handle, Lumis

from utils import *
from Dataset import *


infile_lists = []

#for ds in datasets_muons:
#    infile_lists.append((ds.getName(), indir_antiiso + "/" + ds.getFileName()))
#for ds in datasets_electrons:
#    infile_lists.append((ds.getName(), indir_antiiso + "/" + ds.getFileName()))
for ds in datasets_signal:
    infile_lists.append((ds.getName(), indir_mc + "/" + ds.getFileName()))
#for ds in datasets_bg:
#    infile_lists.append((ds.getName(), indir_mc + "/" + ds.getFileName()))
#for ds in datasets_inclusive:
#    infile_lists.append((ds.getName(), indir_mc + "/" + ds.getFileName()))

outfile = open("runconfs_mva_input.sh", "w")

size = 1
for (dataset, file_list_file) in infile_lists:
    file_list = get_file_list(file_list_file)
    
    for start in range(len(file_list) / size + 1):
        #print start, len(file_list)
        current_list = list_to_string(file_list[start*size:(start+1)*size])
        #print start, current_list
        iso = "iso"
        if "antiiso" in file_list_file:
            iso = "antiiso"
        bf_name = "/tmp/andres/qcd_mva_input_"+dataset+"_"+str(start)+"_"+iso+".sh"
        batch_outfile = open(bf_name, "w")
        outfile.write("python qcd_mva_input.py "+dataset+" "+str(start)+" " + iso + " " +current_list+"\n")
        batch_outfile.write("#!/bin/bash\n")
        batch_outfile.write("source $STPOL_DIR/setenv.sh\n")
        batch_outfile.write("python $STPOL_DIR/src/qcd_ntuples/qcd_mva_input.py "+dataset+" "+str(start)+" " + iso + " " +current_list+"\n")
        batch_outfile.close()
        call(["chmod", "755", bf_name])
        call(["sbatch", bf_name])
        print bf_name

