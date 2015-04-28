import sys
import os
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) + "/qcd_ntuples" )
from qcd_ntuples import parse_input
import time
#Monkey-patch the system path to import the stpol header
#sys.path.append(os.path.join(os.environ["STPOL_DIR"], "src/headers"))
from subprocess import call

for iso in ["iso"]:
    for channel in ["mu"]:
        data_files = parse_input.get_data_files_reproc(iso, channel)

#print data_files
total_jobs = 0
for dataset, fileset in data_files.items():
    print
    print dataset
    if not ("ToLeptons" in dataset or ("TTJets" in dataset and "Lept" in dataset) or "Jets_exclusive" in dataset): continue
    i = 0
    for (base_file, added_file) in fileset:
        total_jobs += 1
        print i, base_file
        bf_name = "/tmp/andres/btageffs_%s_%s_%s_%d.sh" % (dataset, channel, iso, i)
        batch_outfile = open(bf_name, "w")
        batch_outfile.write("#!/bin/bash\n")
        batch_outfile.write("source $STPOL_DIR/setenv.sh\n")
        batch_outfile.write("python $STPOL_DIR/src/btag_effs/make_histos.py " +channel+" "+dataset+ " " +str(i)+" " +base_file+ "\n")
        batch_outfile.close()
        call(["chmod", "755", bf_name])
        suc = 1
        while not suc == 0:
            suc = call(["sbatch", "-x comp-c-012 comp-c-013", bf_name])
            print bf_name, suc
            if not suc == 0:
                print "XXX"
                time.sleep(10)
        i+=1
        time.sleep(0.1)

print "total jobs", total_jobs
