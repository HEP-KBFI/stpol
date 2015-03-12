import sys
import os
from parse_input import *
#Monkey-patch the system path to import the stpol header
sys.path.append(os.path.join(os.environ["STPOL_DIR"], "src/headers"))
from subprocess import call
import time

data_files = {}
for iso in ["iso"]:#, "antiiso"]:
    data_files[iso] = get_data_files(iso)

#print data_files

for iso in ["iso", "antiiso"]:
    for dataset, fileset in data_files[iso].items():
        i = 0
        print
        print dataset
        
        for (base_file, added_file) in fileset:
            print i, base_file
            bf_name = "/tmp/andres/qcdevents_%s_%s_%d.sh" % (dataset, iso, i)
            batch_outfile = open(bf_name, "w")
            batch_outfile.write("#!/bin/bash\n")
            batch_outfile.write("source $STPOL_DIR/setenv.sh\n")
            batch_outfile.write("python $STPOL_DIR/src/qcd_ntuples/qcd_eventlists.py " +dataset+ " " +iso+" " +str(i)+" "+base_file+" " + added_file + "\n")
            print "python $STPOL_DIR/src/qcd_ntuples/qcd_eventlists.py " +dataset+ " " +iso+" " +str(i)+" "+base_file+" " + added_file + "\n"
            batch_outfile.close()
            call(["chmod", "755", bf_name])
            suc = 1
            while not suc == 0:
                suc = call(["sbatch", "-x comp-d-058", bf_name])
                print bf_name, suc
                if not suc == 0:
                    print "XXX"
                    time.sleep(10)
            i+=1
            time.sleep(1)
