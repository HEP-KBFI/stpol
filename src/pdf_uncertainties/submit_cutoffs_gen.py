import sys
import os
from parse_input import datasets
from utils import pdfs
import time
#Monkey-patch the system path to import the stpol header
sys.path.append(os.path.join(os.environ["STPOL_DIR"], "src/headers"))
from subprocess import call

for ds in datasets:
    if not "ToLeptons" in ds:continue
    bf_name = "/tmp/andres/cutoffs_%s.sh" % (ds)
    batch_outfile = open(bf_name, "w")
    batch_outfile.write("#!/bin/bash\n")
    batch_outfile.write("source $STPOL_DIR/setenv.sh\n")
    batch_outfile.write("python $STPOL_DIR/src/pdf_uncertainties/gen_calc_weight_cutoffs.py " +ds+ "\n")
    batch_outfile.close()
    call(["chmod", "755", bf_name])
    suc = 1
    while not suc == 0:
        suc = call(["sbatch", "-x comp-d-058", bf_name])
        print bf_name, suc
        if not suc == 0:
            print "XXX"
            time.sleep(10)
    time.sleep(1)
