import sys
import os
from parse_input import *
from utils import pdfs
import time
#Monkey-patch the system path to import the stpol header
sys.path.append(os.path.join(os.environ["STPOL_DIR"], "src/headers"))
from subprocess import call

data_files = get_data_files()
#pdfconfs = ["ct10", "nnpdf", "nnpdf_down", "nnpdf_up"] #,"mstw"]

total_jobs = 0
#time.sleep(10000)
for channel in ["ele"]:
    for dataset, fileset in data_files.items():
        for p in pdfs:
            #if not ("TTJets" in dataset or "exclusive" in dataset):continue
            if not "TTJets_S" in dataset: continue
            if not ("NNPDF" in p or "MSTW" in p): continue
            #if not "exclusive" in dataset: continue
            call(["mkdir", "-p", dataset])
            savedPath = os.getcwd()
            os.chdir(savedPath+"/"+dataset)

            i = 0
            for (base_file, added_file) in fileset:
                counter = base_file.split("output")[2].split(".")[0]
                bf_name = "/tmp/andres/pdfz_%s_%s_%s_%s.sh" % (channel, dataset, p, counter)
                batch_outfile = open(bf_name, "w")
                batch_outfile.write("#!/bin/bash\n")
                batch_outfile.write("source $STPOL_DIR/setenv.sh\n")
                batch_outfile.write("python $STPOL_DIR/src/pdf_uncertainties/pdf_eventloop.py " +dataset+ " " +p+ " " +str(counter)+" "+channel+" "+base_file+" " + added_file + "\n")
                #print "python $STPOL_DIR/src/pdf_uncertainties/pdf_eventloop.py " +dataset+ " " +str(i)+" "+base_file+" " + added_file + "\n"
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
                total_jobs += 1
                time.sleep(0.2)
            os.chdir(savedPath )
print total_jobs, "jobs submitted"            
        
