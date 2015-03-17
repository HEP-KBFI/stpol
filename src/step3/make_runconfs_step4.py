import sys
import os
from array import array
import time
#import argparse

from subprocess import call
from read_csv_info import *
from utils import *
from parse_input import datasets, datasets_qcd, datasets_syst

METADATA = "/home/andres/single_top/stpol_pdf/src/step3/metadata.json"

path = "/home/andres/single_top/stpol_pdf/src/step4/output/"
infile = open("/home/andres/single_top/stpol_pdf/src/step3/all_files.dat")
total_jobs = 0
print infile
for line in infile:
    if not line.strip().endswith("root"): continue
    #if not "_MS_" in line: continue
    compos = line.strip().split("/")
    fn = compos[-1]
    ds = compos[-2]
    syst = compos[-3]
    iso = compos[-4]
    #if not ("ToLeptons" in ds): continue
    #if not "TTJets" in ds: continue
    if not ("WJets" in line or "Jets_exclusive" in line or "JetsToLNu" in line): continue
    #if not ("W2JetsToLNu_scaleup" in line): continue
    #if not "FSIM" in line:continue
    #if not ("nominal" in syst or "data" in syst): continue
    #if "exclusive" in line or "T_" in line or "Tbar_" in line or "Single" in line or "herpa" in line: continue
    #if not ("nominal" in line): continue
    #if not (("exclusive" in line or "JetsToLNu" in line or "TTJets" in line) and "SYST" in line): continue
    try: 
        if not os.path.isdir(path+"/"+iso+"/"+syst+ "/"+ds):
            os.makedirs(path+"/"+iso+"/"+syst+ "/"+ds)
    except OSError:
        if not os.path.isdir(path+"/"+iso+"/"+syst+ "/"+ds):
            raise
    #if ds == "W2JetsToLNu" or ds == "W3JetsToLNu" or ds == "W4JetsToLNu": continue
    #if not "ToLNu" in ds: continue
    step = 500000000000000
    #if "T_t" in line or "TToB" in line: step = 10000
    event_count = get_event_count(line.strip().replace(".root", "_processed.csv"))
    nr_procs = event_count / step
    if not event_count % step == 0:
        nr_procs += 1
    for proc in range(nr_procs):
        start = 0 + step * proc
        end = step * (proc + 1) - 1
        outfile = path+"/"+iso+"/"+syst+ "/"+ds+"/"+str(proc)+"_"+fn
        bf_name = "/tmp/andres/s4_spl_it_"+line.strip().replace(".","_").replace("/","_")+"_"+str(proc)+".sh"
        batch_outfile = open(bf_name, "w")
        batch_outfile.write("#!/bin/bash\n")
        batch_outfile.write("source /home/software/julia/setenv.sh\n")
        batch_outfile.write("source /home/software/root_v_5_34_21/bin/thisroot.sh\n")
        batch_outfile.write("julia /home/andres/single_top/stpol_pdf/src/analysis/evloop2.jl %s /home/andres/single_top/stpol_pdf/src/analysis/infile.json %d %d %s" % (outfile, start, end, line))
        batch_outfile.close()
        call(["chmod", "755", bf_name])
        suc = 1
        while not suc == 0:
            suc = call(["sbatch", "-x comp-c-012", bf_name])
            print bf_name, suc
            if not suc == 0:
                print "XXX"
                time.sleep(10)
        total_jobs += 1
        time.sleep(.4)
    #print bf_name
print "total jobs submitted", total_jobs
