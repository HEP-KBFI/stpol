import sys
import os
from parse_input import *
from utils import pdfs
import time
#Monkey-patch the system path to import the stpol header
sys.path.append(os.path.join(os.environ["STPOL_DIR"], "src/headers"))
from subprocess import call


def get_file_list(file_list_file):
    lines = [line.strip() for line in open(file_list_file)]
    return lines



data_files = get_data_files()
#pdfconfs = ["ct10", "nnpdf", "nnpdf_down", "nnpdf_up"] #,"mstw"]

pdfs = {}
pdfs["nnpdf"] = ["NNPDF23nloas0119LHgrid"]
pdfs["nnpdf_down"] = ["NNPDF23nloas0116LHgrid", "NNPDF23nloas0117LHgrid", "NNPDF23nloas0118LHgrid"]
pdfs["nnpdf_up"] = ["NNPDF23nloas0120LHgrid", "NNPDF23nloas0121LHgrid", "NNPDF23nloas0122LHgrid"]


counter = 0
for channel in ["mu", "ele"]:
    for dataset, fileset in data_files.items():
        if not "t_ToLeptons" in dataset: continue
        for p, lst in pdfs.items():
            file_list_file = os.path.join(os.environ["STPOL_DIR"], "filelists", "pdf_Jan11_deltaR", p, dataset+".files.txt")
            file_list = get_file_list(file_list_file)
    
            for l in lst:
                call(["mkdir", "-p", dataset])
                savedPath = os.getcwd()
                os.chdir(savedPath+"/"+dataset)

                i = 0
                for f in file_list:
                    j = 0
                    for base_file in fileset:
                        
                        bf_name = "/tmp/andres/pdf_%s_%s_%s_%d_%d.sh" % (channel, dataset, l, i, j)
                        batch_outfile = open(bf_name, "w")
                        batch_outfile.write("#!/bin/bash\n")
                        batch_outfile.write("source $STPOL_DIR/setenv.sh\n")
                        batch_outfile.write("python $STPOL_DIR/src/pdf_uncertainties/calculate_NNPDF_CL_gen.py " +dataset+ " " +l+ " " +str(i)+ " " +str(j)+" "+channel+" "+"/hdfs/cms/"+f+" "+base_file[0]+" "+base_file[1]+"\n")
                        #print "python $STPOL_DIR/src/pdf_uncertainties/pdf_eventloop.py " +dataset+ " " +str(i)+" "+base_file+" " + added_file + "\n"
                        batch_outfile.close()
                        call(["chmod", "755", bf_name])
                        suc = 1
                        while not suc == 0:
                            suc = call(["sbatch", "-x comp-d-058", bf_name])
                            print bf_name, suc
                            if not suc == 0:
                                print "XXX"
                                time.sleep(10)
                        j+=1
                        counter += 1
                        time.sleep(.05)
                    i += 1
                    time.sleep(.2)
                os.chdir(savedPath )
            
print "submitted", counter        
