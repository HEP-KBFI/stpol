import sys
import os
from array import array
import time
#import argparse

#Monkey-patch the system path to import the stpol header
#from stpol import stpol, list_methods
from subprocess import call
#import ROOT
#from ROOT import TH1D, TFile
#import TMVA
# prepare the FWLite autoloading mechanism
#ROOT.gSystem.Load("libFWCoreFWLite.so")
#ROOT.AutoLibraryLoader.enable()
#from PhysicsTools.PythonAnalysis import *
#from DataFormats.FWLite import Events, Handle, Lumis

from utils import *
from parse_input import datasets, datasets_qcd, datasets_syst, datasets_data
#from Dataset import *


#indir = "/home/andres/single_top/stpol/filelists/Oct3_nomvacsv_nopuclean_e224b5/step2/"
#indir_mc = indir + "mc/iso/nominal/"
#indir_antiiso = indir + "data/antiiso/"
#indir_data = indir + "data/iso/"
#mc/iso/nominal/

channels = ["mu", "ele"]
isos = ["antiiso"]
systematics = ["nominal"]
#, "SYST"
infile_lists = {}

for iso in isos:
    infile_lists[iso] = {}
    for ds in datasets:
        infile_lists[iso][ds] = {}
        for syst in systematics:
            if iso == "antiiso" and not syst == "nominal": continue
            infile_lists[iso][ds][syst] = os.path.join("/home", "andres", "single_top", "stpol_pdf", "filelists", "Apr21_btags", "step2", "mc", iso, syst, "%s.files.txt" % ds)
    
    """
    for ds in datasets_qcd:
        infile_lists[iso][ds] = {}
        infile_lists[iso][ds]["nominal"] = os.path.join("/home", "andres", "single_top", "stpol_pdf", "filelists", "Apr21_btags", "step2", "mc", iso, "nominal", "%s.files.txt" % ds)
    """
    """
    for ds in datasets_syst:
        if iso == "antiiso": continue
        infile_lists[iso][ds] = {}
        infile_lists[iso][ds]["SYST"] = os.path.join("/home", "andres", "single_top", "stpol_pdf", "filelists", "Apr21_btags", "step2", "mc_syst", iso, "nominal", "%s.files.txt" % ds)
    """
    """
    for ds in datasets_data:
        infile_lists[iso][ds] = {}
        infile_lists[iso][ds]["data"] = os.path.join("/home", "andres", "single_top", "stpol_pdf", "filelists", "Jan22_fullData", "step2", "data", iso, "%s.files.txt" % ds)
    """
size = 1
path = "/home/andres/single_top/stpol_pdf/src/step3/output/Apr21_btags"
try:
    if not os.path.isdir(path): 
        os.makedirs(path)
except OSError:
    if not os.path.isdir(path):
        raise
total_jobs = 0



for (iso, stuff) in infile_lists.items():
    try: 
        if not os.path.isdir(path+"/"+iso):
            os.makedirs(path+"/"+iso)
    except OSError:
        if not os.path.isdir(path+"/"+iso):
            raise
    for (dataset, stuff2) in stuff.items():
        print dataset
        #if not dataset in ["TTJets_MS_matchingdown", "TTJets_MS_mass175_5", "TTJets_MS_mass169_5"]: continue
        #if not ("Jets_exclusive" in dataset): continue
        #if not "FSIM" in dataset:continue
        #if not (dataset in ["QCD_Pt_250_350_EMEnriched", "QCD_Pt_250_350_BCtoE", "QCD_Pt_30_80_EMEnriched", "GJets1", "GJets2", "QCD_Pt_350_EMEnriched", "QCD_Pt_170_250_EMEnriched", "QCD_Pt_20_30_EMEnriched"] and iso == "iso"): continue
        #if not (dataset in ["QCD_Pt_20_30_EMEnriched", "QCD_Pt_170_250_EMEnriched", "QCD_Pt_170_250_BCtoE", "QCD_Pt_350_BCtoE", "QCD_Pt_350_EMEnriched", "GJets1", "GJets2", "QCD_Pt_20_30_BCtoE", "QCD_Pt_250_350_BCtoE", "QCD_Pt_30_80_BCtoE", "QCD_Pt_250_350_EMEnriched"] and iso == "antiiso"): continue
        #if dataset == "SingleMu" and iso == "antiiso": continue
        #if "TToLeptons_t-channel_aMCatNLO" not in dataset: continue
        #if not ("WJets" in dataset or "Jets_exclusive" in dataset or "JetsToLNu" in dataset): continue
        #if not ("W2JetsToLNu_scaleup" in dataset): continue
        #if not ("TTJets_MS_scaleup" in dataset): continue
        #if (not "TTJets_FullLept" in dataset): continue
        if "W2JetsToLNu_scaleup" in dataset: size = 4
        elif "QCD" in dataset or "GJets" in dataset or "JetsTo" in dataset or "WJets" in dataset or "Jets_exclusive" in dataset or "Single" in dataset: size = 10
        elif "_MS" in dataset: size=2
        else: size = 1
        #if not "Single" in dataset:continue        
        #print infile_lists[iso]
        for (syst, file_list_file) in stuff2.items():
            #if not dataset in ["WW", "WJets_inclusive", "TTJets_MassiveBinDECAY", "DYJets", "TTJets_SemiLept", "T_tW", "T_t_ToLeptons", "W3Jets_exclusive", "TTJets_FullLept"]: continue   
            print syst, file_list_file
            call(["mkdir", "-p", iso+"/"+syst+"/"+dataset])
            savedPath = os.getcwd()
            os.chdir(savedPath+"/"+iso+"/"+syst+"/"+dataset)
            try: 
                if not os.path.isdir(path+"/"+iso+"/"+syst):
                    os.makedirs(path+"/"+iso+"/"+syst)
                if not os.path.isdir(path+"/"+iso+"/"+syst+"/"+dataset):
                    os.makedirs(path+"/"+iso+"/"+syst+"/"+dataset)
            except OSError:
                if not os.path.isdir(path+"/"+iso+"/"+syst+"/"+dataset):
                    raise
            #print dataset
            if "Single" in dataset and iso == "iso": #"/hdfs/local", so don't prepend /hdfs/cms
                file_list = get_file_list(file_list_file, True)
            else:
                file_list = get_file_list(file_list_file)
                #if "JetsToLNu" in dataset and "1JetsToLNu" not in dataset and "down" not in dataset and "up" not in dataset:
                #if "JetsToLNu" in dataset and "1JetsToLNu" not in dataset and "down" not in dataset and "up" not in dataset and "JetsToLNu2" not in dataset:
                #    continue
                #    file_list.extend(get_file_list(file_list_file.replace("JetsToLNu", "JetsToLNu2")))
                #    print "Extending file list %s by file list %s" % (file_list_file, file_list_file.replace("JetsToLNu", "JetsToLNu2"))
            """try: 
                os.makedirs(path)
            except OSError:
                if not os.path.isdir(path):
                    raise"""
            for start in range(len(file_list) / size + 1):
                current_list = list_to_string(file_list[start*size:(start+1)*size])
                
                #dataset = dataset.replace("JetsToLNu2", "JetsToLNu")
                #dataset = dataset.replace("T_t_mass", "T_t_ToLeptons_mass")
                bf_name = "/tmp/andres/step3_"+str(start)+"_"+dataset+iso+syst+".sh"
                batch_outfile = open(bf_name, "w")
                batch_outfile.write("#!/bin/bash\n")
                #batch_outfile.write("source $STPOL_DIR/setenv.sh\n")
                outname = path+"/"+iso+"/"+syst+"/"+dataset+"/output%d" % start
                batch_outfile.write("/home/software/.julia/v0.3/CMSSW/julia /home/andres/single_top/stpol_pdf/src/skim/skim.jl %s %s" % (outname, current_list))
                batch_outfile.close()
                call(["chmod", "755", bf_name])
                suc = 1
                while not suc == 0:
                    #suc = call(["sbatch", bf_name])
                    suc = call(["sbatch", "-x comp-c-012", bf_name])
                    print bf_name, suc
                    if not suc == 0:
                        print "XXX"
                        time.sleep(10)
                total_jobs += 1
                #i+=1
                time.sleep(1)
                #print bf_name
                #print current_list

            time.sleep(5)
            os.chdir(savedPath )
print "total jobs submitted", total_jobs
