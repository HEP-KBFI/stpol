import json
from pprint import pprint
import os
import fnmatch

datasets = [
    "DYJets", 
    "T_t", 
    "Tbar_tW", 
    "W4Jets_exclusive", 
    #"W4JetsToLNu",
    #"W4JetsToLNu2",
    "ZZ", 
    "TTJets_FullLept", 
    "T_tW", 
    "Tbar_t_ToLeptons", 
    "WJets_inclusive", 
    "TTJets_MassiveBinDECAY", 
    "T_t_ToLeptons", 
    "W1Jets_exclusive", 
    #"W1JetsToLNu",
    "TTJets_SemiLept", 
    "Tbar_s", 
    "W2Jets_exclusive", 
    #"W2JetsToLNu",
    #"W2JetsToLNu2",
    "WW", 
    "T_s", 
    "Tbar_t", 
    "W3Jets_exclusive", 
    #"W3JetsToLNu",
    #"W3JetsToLNu2",
    "WZ"
]

#datasets = ["W4JetsToLNu2"]

datasets_mva = [
    "T_t", 
    "Tbar_t_ToLeptons", 
    "T_t_ToLeptons", 
    "Tbar_t",     
]

"""datasets_data = [
    "SingleEle1",
    "SingleEle2",
    "SingleEle_miss",
    "SingleMu1",
    "SingleMu2",
    "SingleMu3",
    "SingleMu_miss"
]"""

datasets_data = [
    "SingleEle",
    "SingleMu",    
]

datasets_qcd = [
    "QCD_Pt_170_250_BCtoE",
    "QCD_Pt_250_350_BCtoE",
    "QCD_Pt_350_BCtoE",
    "GJets1",
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

datasets_syst = [
    "Tbar_t_ToLeptons_mass169_5",
    "Tbar_t_ToLeptons_mass175_5",
    #"Tbar_t_ToLeptons_mass178_5,
    "Tbar_t_ToLeptons_scaledown",
    "Tbar_t_ToLeptons_scaleup",
    "T_t_ToLeptons_mass169_5",
    "T_t_ToLeptons_mass175_5",
    "T_t_ToLeptons_scaledown",
    "T_t_ToLeptons_scaleup",
    #"TTJets_mass169_5",
    #"TTJets_mass175_5",
    #"TTJets_matchingdown",
    #"TTJets_matchingup",
    #"TTJets_scaledown",
    #"TTJets_scaleup",
    #TTJets_MS_mass166_5,
    "TTJets_MS_mass169_5",
    "TTJets_MS_mass175_5",
    "TTJets_MS_matchingdown",
    "TTJets_MS_matchingup",
    "TTJets_MS_scaledown",
    "TTJets_MS_scaleup",
    "TToBENu_anomWtb-0010_LVLT_t-channel",
    "TToBENu_anomWtb-0100_t-channel",
    "TToBENu_anomWtb-Lv1Rt3_LVRT_t-channel",
    "TToBENu_anomWtb-Lv2Rt2_LVRT_t-channel",
    "TToBENu_anomWtb-Lv3Rt1_LVRT_t-channel",
    "TToBENu_anomWtb-Rt4_LVRT_t-channel",
    "TToBENu_anomWtb-unphys_LVLT_t-channel",
    "TToBENu_anomWtb-unphys_t-channel",
    "TToBENu_t-channel",
    "TToBMuNu_anomWtb-0010_LVLT_t-channel",
    "TToBMuNu_anomWtb-0100_t-channel",
    "TToBMuNu_anomWtb-Lv1Rt3_LVRT_t-channel",
    "TToBMuNu_anomWtb-Lv2Rt2_LVRT_t-channel",
    "TToBMuNu_anomWtb-Lv3Rt1_LVRT_t-channel",
    "TToBMuNu_anomWtb-Rt4_LVRT_t-channel",
    "TToBMuNu_anomWtb-unphys_LVLT_t-channel",
    "TToBMuNu_anomWtb-unphys_t-channel",
    "TToBMuNu_t-channel",
    "TToBTauNu_anomWtb-0010_LVLT_t-channel",
    "TToBTauNu_anomWtb-0100_t-channel",
    "TToBTauNu_anomWtb-Lv1Rt3_LVRT_t-channel",
    "TToBTauNu_anomWtb-Lv2Rt2_LVRT_t-channel",
    "TToBTauNu_anomWtb-Lv3Rt1_LVRT_t-channel",
    "TToBTauNu_anomWtb-Rt4_LVRT_t-channel",
    "TToBTauNu_anomWtb-unphys_LVLT_t-channel",
    "TToBTauNu_anomWtb-unphys_t-channel",
    "TToBTauNu_t-channel",
    "W1JetsToLNu_matchingup",
    "W1JetsToLNu_matchingdown",
    "W1JetsToLNu_scaledown",
    "W1JetsToLNu_scaleup",
    "W2JetsToLNu_matchingdown",
    "W2JetsToLNu_matchingup",
    "W2JetsToLNu_scaledown",
    "W2JetsToLNu_scaleup",
    "W3JetsToLNu_matchingdown",
    "W3JetsToLNu_matchingup",
    "W3JetsToLNu_scaledown",
    "W3JetsToLNu_scaleup",
    "W4JetsToLNu_matchingdown",
    "W4JetsToLNu_matchingup",
    "W4JetsToLNu_scaledown",
    "W4JetsToLNu_scaleup",
    #"WJets_matchingdown",
    #"WJets_matchingup",
    #"WJets_scaledown",
    #"WJets_scaleup",
    "W1Jets_exclusive_FSIM",
    "W2Jets_exclusive_FSIM",
    "W3Jets_exclusive_FSIM",
    "W4Jets_exclusive_FSIM",
    "WJets_sherpa", 
    "TToLeptons_tchannel_aMCatNLO",
    "TToLeptons_tchannel_aMCatNLO_scaledown",
    "TToLeptons_tchannel_aMCatNLO_scaleup"    
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

#base_dir = "/hdfs/local/joosep/stpol/skims/step3/tchpt/Aug8_tchpt/"
#base_dir = "/hdfs/local/joosep/stpol/skims/step3/csvt/Jul4_newsyst_newvars_metshift/"

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


def get_data_files_mva(iso):
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
