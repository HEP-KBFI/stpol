import json
from pprint import pprint
import os
import fnmatch

datasets = [
    "DYJets", 
    "T_t", 
    "Tbar_tW", 
    "W4Jets_exclusive", 
    "ZZ", 
    "TTJets_FullLept", 
    "T_tW", 
    "Tbar_t_ToLeptons", 
    #"WJets_inclusive", 
    "TTJets_MassiveBinDECAY", 
    "T_t_ToLeptons", 
    "W1Jets_exclusive", 
    #"WJets_sherpa", 
    "TTJets_SemiLept", 
    "Tbar_s", 
    "W2Jets_exclusive", 
    "WW", 
    "T_s", 
    "Tbar_t", 
    "W3Jets_exclusive", 
    "WZ"
]

datasets_reproc = [
    "DYJets", 
    "T_t", 
    "Tbar_tW", 
    #"W4JetsToLNu", 
    #"W4JetsToLNu2", 
    "W4Jets_exclusive",
    "ZZ", 
    "TTJets_FullLept", 
    "T_tW", 
    "Tbar_t_ToLeptons", 
    #"WJets_inclusive", 
    #"TTJets_MassiveBinDECAY", 
    "T_t_ToLeptons", 
    #"W1JetsToLNu", 
    "W1Jets_exclusive",
    #"WJets_sherpa", 
    "TTJets_SemiLept", 
    "Tbar_s", 
    #"W2JetsToLNu", 
    #"W2JetsToLNu2", 
    "W2Jets_exclusive",
    "WW", 
    "T_s", 
    "Tbar_t", 
    #"W3JetsToLNu", 
    #"W3JetsToLNu2", 
    "W3Jets_exclusive",
    "WZ"
]

datasets_mva = [
    "T_t", 
    "Tbar_t_ToLeptons", 
    "T_t_ToLeptons", 
    "Tbar_t",     
]

datasets_data = [
    "SingleEle1",
    "SingleEle2",
    "SingleEle_miss",
    "SingleMu1",
    "SingleMu2",
    "SingleMu3",
    "SingleMu_miss"
]

datasets_data = [
    "SingleEle",
    "SingleMu"
]

datasets_qcd = [
    "QCD_Pt_170_250_BCtoE"
    "QCD_Pt_250_350_BCtoE"
    "QCD_Pt_350_BCtoE"
    "GJets1"
    "QCD_Pt_170_250_EMEnriched",
    "QCD_Pt_250_350_EMEnriched",
    "QCD_Pt_350_EMEnriched",
    "GJets2",
    "QCD_Pt_20_30_BCtoE",
    "QCD_Pt_30_80_BCtoE",
    "QCD_Pt_80_170_BCtoE",
    "QCDMu",
    "QCD_Pt_20_30_EMEnriched",
    "QCD_Pt_30_80_EMEnriched",
    "QCD_Pt_80_170_EMEnriched"
]

groups = {
    "DYJets": "wzjets", 
    #"T_t", 
    "Tbar_tW": "ttjets", 
    "W4Jets_exclusive": "wzjets", 
    "W4JetsToLNu2": "wzjets", 
    #"W4JetsToLNu2": "wzjets",    
    "ZZ": "wzjets", 
    "TTJets_FullLept": "ttjets", 
    "T_tW": "ttjets", 
    "Tbar_t_ToLeptons": "tchan", 
    #"WJets_inclusive", 
    #"TTJets_MassiveBinDECAY", 
    "T_t_ToLeptons": "tchan", 
    "W1Jets_exclusive": "wzjets", 
    "W1JetsToLNu": "wzjets", 
    #"WJets_sherpa", 
    "TTJets_SemiLept": "ttjets", 
    "Tbar_s": "ttjets", 
    "W2Jets_exclusive": "wzjets", 
    "W2JetsToLNu2": "wzjets", 
    #"W2JetsToLNu2": "wzjets",    
    "WW": "wzjets", 
    "T_s": "ttjets", 
    #"Tbar_t", 
    "W3Jets_exclusive": "wzjets", 
    "W3JetsToLNu2": "wzjets", 
    #"W3JetsToLNu2": "wzjets",    
    "WZ": "wzjets"
}

#base_dir = "/hdfs/local/joosep/stpol/skims/step3/tchpt/Aug8_tchpt/"
#base_dir = "/hdfs/local/joosep/stpol/skims/step3/csvt/Jul4_newsyst_newvars_metshift/"
#base_dir = "/hdfs/local/andres/stpol/skims/Oct28_reproc/"
#base_dir = "/home/andres/single_top/stpol_pdf/src/step3/output/Oct28_reproc_small/"
#base_dir = "/home/andres/single_top/stpol_pdf/src/step3/output/Oct28_reproc/"
#base_dir = "/home/andres/single_top/stpol_pdf/src/step3/output/Oct28_reproc_size1_renames/"
#base_dir = "/home/andres/single_top/stpol_pdf/src/step3/output/Jan11_deltaR_v1/"
base_dir = "/home/andres/single_top/stpol_pdf/src/step3/output/Apr21_btags/"

def get_data_files(iso, channel, qcdmva = False):
    data_files = dict()
    for ds in datasets:
        data_files[ds] = []
        for root, dir, files in os.walk(base_dir+iso+"/nominal/"+ds):
            base_file = fnmatch.filter(files, "*.root")
            added_file = fnmatch.filter(files, "*.root.added")
            assert len(base_file) <= 1
            assert len(added_file) <= 1
            if len(base_file) == 1 and len(added_file) == 1:
                data_files[ds].append((root+'/'+base_file[0], root+'/'+added_file[0]))
    if not qcdmva:
        for ds in datasets_qcd:
            if channel == "mu" and not ds == "QCDMu": continue
            if channel == "ele" and ds == "QCDMu": continue
            data_files[ds] = []
            for root, dir, files in os.walk(base_dir+iso+"/nominal/"+ds):
                base_file = fnmatch.filter(files, "*.root")
                added_file = fnmatch.filter(files, "*.root.added")
                assert len(base_file) <= 1
                assert len(added_file) <= 1
                if len(base_file) == 1 and len(added_file) == 1:
                    data_files[ds].append((root+'/'+base_file[0], root+'/'+added_file[0]))
    if not qcdmva or iso == "antiiso":    
        for ds in datasets_data:
            if channel == "mu" and not ds.startswith("SingleMu"): continue
            if channel == "ele" and not ds.startswith("SingleEle"): continue
            data_files[ds] = []
            for root, dir, files in os.walk(base_dir+iso+"/"+ds):
                base_file = fnmatch.filter(files, "*.root")
                added_file = fnmatch.filter(files, "*.root.added")
                assert len(base_file) <= 1
                assert len(added_file) <= 1
                if len(base_file) == 1 and len(added_file) == 1:
                    data_files[ds].append((root+'/'+base_file[0], root+'/'+added_file[0]))
    return data_files

#base_dir_reproc = "/home/andres/single_top/stpol_pdf/src/step3/output/"

def get_data_files_reproc(iso, channel, qcdmva = False):
    data_files = dict()
    """data_files["ds"] = []
    for root, dir, files in os.walk(base_dir+iso):
        base_files = fnmatch.filter(files, "*.root")
        #added_file = fnmatch.filter(files, "*.root.added")
        #assert len(base_file) <= 1
        #assert len(added_file) <= 1
        #if len(base_file) == 1 and len(added_file) == 1:
        for f in base_files:
            data_files["ds"].append((root+'/'+f, root+'/'+f+".added"))
            #data_files[ds.replace("ToLNu2", "ToLNu")].append((root+'/'+f, root+'/'+f+".added"))
    """
    for ds in datasets_reproc:
        data_files[ds] = []
        #data_files[ds.replace("ToLNu2", "ToLNu")] = []
        
        for root, dir, files in os.walk(base_dir+iso+"/nominal/"+ds):
            base_files = fnmatch.filter(files, "*.root")
            #added_file = fnmatch.filter(files, "*.root.added")
            #assert len(base_file) <= 1
            #assert len(added_file) <= 1
            #if len(base_file) == 1 and len(added_file) == 1:
            for f in base_files:
                data_files[ds].append((root+'/'+f, root+'/'+f+".added"))
                #data_files[ds.replace("ToLNu2", "ToLNu")].append((root+'/'+f, root+'/'+f+".added"))
                
    if not qcdmva:
        for ds in datasets_qcd:
            if channel == "mu" and not ds == "QCDMu": continue
            if channel == "ele" and ds == "QCDMu": continue
            data_files[ds] = []
            for root, dir, files in os.walk(base_dir+iso+"/nominal/"+ds):
                base_files = fnmatch.filter(files, "*.root")
                #added_file = fnmatch.filter(files, "*.root.added")
                #assert len(base_file) <= 1
                #assert len(added_file) <= 1
                for f in base_files:
                    data_files[ds].append((root+'/'+f, root+'/'+f+".added"))
    if not qcdmva or iso == "antiiso":    
        for ds in datasets_data:
            if channel == "mu" and not ds.startswith("SingleMu"): continue
            if channel == "ele" and not ds.startswith("SingleEle"): continue
            data_files[ds] = []
            for root, dir, files in os.walk(base_dir+iso+"/data/"+ds):
                base_files = fnmatch.filter(files, "*.root")
                for f in base_files:
                    data_files[ds].append((root+'/'+f, root+'/'+f+".added"))
    return data_files

def get_data_files_mva(iso):
    data_files = dict()
    for ds in datasets_mva:
        data_files[ds] = []
        for root, dir, files in os.walk(base_dir+iso+"/nominal/"+ds):
            base_files = fnmatch.filter(files, "*.root")
            for f in base_files:
                    data_files[ds].append((root+'/'+f, root+'/'+f+".added"))
    if iso == "antiiso":    
        for ds in datasets_data:
            data_files[ds] = []
            for root, dir, files in os.walk(base_dir+iso+"/data/"+ds):
                base_files = fnmatch.filter(files, "*.root")
                for f in base_files:
                    data_files[ds].append((root+'/'+f, root+'/'+f+".added"))
    return data_files        


def get_data_files_mva_old(iso):
    data_files = dict()
    for ds in datasets_mva:
        data_files[ds] = []
        for root, dir, files in os.walk(base_dir+iso+"/nominal/"+ds):
            base_file = fnmatch.filter(files, "*.root")
            added_file = fnmatch.filter(files, "*.root.added")
            assert len(base_file) <= 1
            assert len(added_file) <= 1
            if len(base_file) == 1 and len(added_file) == 1:
                data_files[ds].append((root+'/'+base_file[0], root+'/'+added_file[0]))
    if iso == "antiiso":    
        for ds in datasets_data:
            data_files[ds] = []
            for root, dir, files in os.walk(base_dir+iso+"/"+ds):
                base_file = fnmatch.filter(files, "*.root")
                added_file = fnmatch.filter(files, "*.root.added")
                assert len(base_file) <= 1
                assert len(added_file) <= 1
                if len(base_file) == 1 and len(added_file) == 1:
                    data_files[ds].append((root+'/'+base_file[0], root+'/'+added_file[0]))
    return data_files        
