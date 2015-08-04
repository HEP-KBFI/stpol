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
total_jobs = 0
isovar = ["up", "down", None]
for iso in ["iso", "antiiso"]:
    for channel in ["mu", "ele"]:
        for dataset, fileset in data_files[iso+channel].items():
            for iv in isovar:
                #if not "T_t_ToLeptons" in dataset: continue
                if iso == "iso" and not iv==None: continue
                i = 0
                print
                print channel, dataset, iso
                
                for (base_file, added_file) in fileset:
                    total_jobs += 1
                    print i, base_file
                    bf_name = "/tmp/andres/qcdfit_%s_%s_%s_%s_%d.sh" % (dataset, channel, iso, iv, i)
                    batch_outfile = open(bf_name, "w")
                    batch_outfile.write("#!/bin/bash\n")
                    batch_outfile.write("source $STPOL_DIR/setenv.sh\n")
                    batch_outfile.write("python $STPOL_DIR/src/qcd_ntuples/qcd_fit_histos.py " +channel+" "+dataset+ " " +str(i)+" "+iso+" " +base_file+" " + added_file + " " +str(iv) +"\n")
                    batch_outfile.close()
                    call(["chmod", "755", bf_name])
                    suc = 1
                    while not suc == 0:
                        suc = call(["sbatch", "-x comp-c-012", bf_name])
                        print bf_name, suc
                        if not suc == 0:
                            print "XXX"
                            time.sleep(10)
                    i+=1
                    time.sleep(0.005)

print "total jobs", total_jobs
