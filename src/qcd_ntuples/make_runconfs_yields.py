import sys
import os
from parse_input import *
import time
#Monkey-patch the system path to import the stpol header
sys.path.append(os.path.join(os.environ["STPOL_DIR"], "src/headers"))
from subprocess import call

data_files = {}
for iso in ["iso", "antiiso"]:
    for channel in ["mu", "ele"]:
        data_files[iso+channel] = get_data_files_reproc(iso, channel)

#print data_files
total = 0
isovar = ["up", "down", None]
for iso in ["iso"]:#, "antiiso"]:
    for channel in ["mu", "ele"]:
        for dataset, fileset in data_files[iso+channel].items():
            #if not ("Lept" in dataset or "Single" in dataset): continue# or "Single" in dataset): continue
            if not "W1" in dataset:continue
            if iso == "antiiso" and not "Single" in dataset: continue
            i = 0
            print
            print channel, dataset, iso
            
            for (base_file, added_file) in fileset:
                print i, base_file
                bf_name = "/tmp/andres/yield_%s_%s_%s_%d.sh" % (dataset, channel, iso, i)
                batch_outfile = open(bf_name, "w")
                batch_outfile.write("#!/bin/bash\n")
                batch_outfile.write("source $STPOL_DIR/setenv.sh\n")
                batch_outfile.write("python $STPOL_DIR/src/qcd_ntuples/qcd_eventyield_histos.py " +channel+" "+dataset+ " " +str(i)+" "+iso+" " +base_file+" " + added_file + "\n")
                batch_outfile.close()
                call(["chmod", "755", bf_name])
                suc = 1
                while not suc == 0:
                    suc = call(["sbatch", "-x comp-d-058", bf_name])
                    print bf_name, suc
                    if not suc == 0:
                        print "XXX"
                        time.sleep(0.1)
                i+=1
                total +=1
                time.sleep(0.01)
print "submitted", total
