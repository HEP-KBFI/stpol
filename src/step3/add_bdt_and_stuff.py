import sys
import os
from array import array
import time
#import argparse

from subprocess import call

from utils import *
from parse_input import datasets, datasets_qcd, datasets_syst

METADATA = "/home/andres/single_top/stpol_pdf/src/step3/metadata.json"

infile = open("/home/andres/single_top/stpol_pdf/src/step3/all_files.dat")
total_jobs = 0
print infile
for line in infile:
    if not line.strip().endswith("root"): continue
    #if not "Single" in line:continue
    #if not ("UnclusteredEnUp" in line and "W2" in line):continue
    #if not "/iso/nominal" in line: continue
    #if not ("Jets" in line and "SYST" not in line and "GJets" not in line): continue
    #if not ("WJets" in line or "Jets_exclusive" in line or "JetsToLNu" in line): continue
    #if not ("W2JetsToLNu_scaleup" in line): continue
    #if "exclusive" in line or "T_" in line or "Tbar_" in line or "Single" in line or "herpa" in line: continue
    #if not (("exclusive" in line or "JetsToLNu" in line) and "SYST" in line): continue
    #if ("sherpa" in line): continue
    #if not ("WJets" in line or "Jets_exclusive" in line or "JetsToLNu" in line): continue
    #if not "MCatNLO" in line: continue
    bf_name = "/tmp/andres/s3_added_"+line.strip().replace(".","_").replace("/","_")+".sh"
    batch_outfile = open(bf_name, "w")
    batch_outfile.write("#!/bin/bash\n")
    batch_outfile.write("source /home/software/julia/setenv.sh\n")
    batch_outfile.write("export FILE_NAMES=%s\n" % line)
    batch_outfile.write("bash /home/andres/single_top/stpol_pdf/src/skim/merge.sh %s" % (METADATA))
    batch_outfile.close()
    call(["chmod", "755", bf_name])
    suc = 1
    while not suc == 0:
        suc = call(["sbatch", "-x comp-c-012 comp-c-013", bf_name])
        suc = 0
        print bf_name, suc
        if not suc == 0:
            print "XXX"
            time.sleep(10)
    total_jobs += 1
    time.sleep(.5)
    #print bf_name
print "total jobs submitted", total_jobs
