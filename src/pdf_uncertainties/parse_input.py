import json
from pprint import pprint
import os
import fnmatch

datasets = [
    "T_t_ToLeptons", 
    "Tbar_t_ToLeptons", 
    "T_s", 
    "Tbar_s", 
    "T_tW", 
    "Tbar_tW", 
    "DYJets", 
    "TTJets_FullLept", 
    "TTJets_SemiLept", 
    "W1Jets_exclusive", 
    "W2Jets_exclusive", 
    "W3Jets_exclusive", 
    "W4Jets_exclusive", 
    "WW",
    "WZ", 
    "ZZ", 
    #"T_t", 
    #"WJets_inclusive", 
    #"TTJets_MassiveBinDECAY", 
    #"WJets_sherpa", 
    #"Tbar_t", 
]

groups = {
    "DYJets": "wzjets", 
    #"T_t", 
    "Tbar_tW": "ttjets", 
    "W4Jets_exclusive": "wzjets", 
    "ZZ": "wzjets", 
    "TTJets_FullLept": "ttjets", 
    "T_tW": "ttjets", 
    "Tbar_t_ToLeptons": "tchan", 
    #"WJets_inclusive", 
    #"TTJets_MassiveBinDECAY", 
    "T_t_ToLeptons": "tchan", 
    "W1Jets_exclusive": "wzjets", 
    #"WJets_sherpa", 
    "TTJets_SemiLept": "ttjets", 
    "Tbar_s": "ttjets", 
    "W2Jets_exclusive": "wzjets", 
    "WW": "wzjets", 
    "T_s": "ttjets", 
    #"Tbar_t", 
    "W3Jets_exclusive": "wzjets", 
    "WZ": "wzjets"
}

#datasets = ["T_s"]

base_dir = "/home/andres/single_top/stpol_pdf/src/step3/output/May30_deltaRs/iso/nominal/"

def get_data_files():
    data_files = dict()
    for ds in datasets:
        data_files[ds] = []
        for root, dir, files in os.walk(base_dir+ds):
            base_files = fnmatch.filter(files, "*.root")
            for f in base_files:
                data_files[ds].append((root+'/'+f, root+'/'+f+".added"))            
    return data_files
        
