
fit_components_regular = {
    "non_qcd": ["Tbar_t_ToLeptons", "T_t_ToLeptons",
        "Tbar_tW", "T_tW", 
        "Tbar_s", "T_s",
        "TTJets_SemiLept", "TTJets_FullLept",
        "DYJets", 
        "WW", "WZ", "ZZ",
        "W1Jets_exclusive", "W2Jets_exclusive", "W3Jets_exclusive", "W4Jets_exclusive",
    ]
}

fit_components_regular_reproc = {
    "non_qcd": ["Tbar_t_ToLeptons", "T_t_ToLeptons",
        "Tbar_tW", "T_tW", 
        "Tbar_s", "T_s",
        "TTJets_SemiLept", "TTJets_FullLept",
        "DYJets", 
        "WW", "WZ", "ZZ",
        #"W1JetsToLNu", "W2JetsToLNu2", "W3JetsToLNu2", "W4JetsToLNu2", 
        "W1Jets_exclusive", "W2Jets_exclusive", "W3Jets_exclusive", "W4Jets_exclusive",
    ]
}

fit_components_just_signal = {
    "signal": ["Tbar_t_ToLeptons", "T_t_ToLeptons",        
    ]
}



fit_components_4 = {
    "top": ["Tbar_t_ToLeptons", "T_t_ToLeptons",
        "Tbar_tW", "T_tW", 
        "Tbar_s", "T_s",
        "TTJets_SemiLept", "TTJets_FullLept"
    ],
    "DY": ["DYJets"
    ],
    "EW": ["WW", "WZ", "ZZ",
        "W1Jets_exclusive", "W2Jets_exclusive", "W3Jets_exclusive", "W4Jets_exclusive",
    ]
}

fit_components = {
    "regular": fit_components_regular, 
    "4comp": fit_components_4
}

fit_components_datasets = {
    "t-channel": ["Tbar_t_ToLeptons", "T_t_ToLeptons"],
    "tW-channel": ["Tbar_tW", "T_tW"],
    "s-channel": ["Tbar_s", "T_s"],
    "ttbar": ["TTJets_SemiLept", "TTJets_FullLept"],
    "DYJets": ["DYJets"],
    "Dibosons": ["WW", "WZ", "ZZ"],
    "WJets": ["W2Jets_exclusive", "W3Jets_exclusive", "W4Jets_exclusive"]
}


fit_components_reproc = {
    "regular": fit_components_regular_reproc, 
    "4comp": fit_components_4,
    "just_signal": fit_components_just_signal,
    "datasets": fit_components_datasets
}

component_uncertainties = {
    "non_qcd": 1.2,
    "top": 1.2,
    "DY": 1.2,
    "EW": 1.3
}

all_datasets = ["Tbar_t_ToLeptons", "T_t_ToLeptons", 
    "Tbar_tW", "T_tW", 
    "Tbar_s", "T_s",
    "TTJets_SemiLept", "TTJets_FullLept",
    "DYJets", 
    "WW", "WZ", "ZZ",
    "W1Jets_exclusive", "W2Jets_exclusive", "W3Jets_exclusive", "W4Jets_exclusive",
    "QCD",
    "data"
    ]

all_datasets_reproc = ["Tbar_t_ToLeptons", "T_t_ToLeptons", 
    "Tbar_tW", "T_tW", 
    "Tbar_s", "T_s",
    "TTJets_SemiLept", "TTJets_FullLept",
    "DYJets", 
    "WW", "WZ", "ZZ",
    #"W1JetsToLNu", "W2JetsToLNu2", "W3JetsToLNu2", "W4JetsToLNu2",
    "W1Jets_exclusive", "W2Jets_exclusive", "W3Jets_exclusive", "W4Jets_exclusive", 
    "QCD",
    "data"
    ]

all_datasets_test = ["Tbar_t_ToLeptons", "T_t_ToLeptons", 
    "TTJets_SemiLept", "TTJets_FullLept",
    "data"
]


legend_names = {"T_t_ToLeptons": "t-channel", 
    "T_tW": "tW-channel", 
    "T_s": "s-channel",
    "TTJets_SemiLept": "ttbar",
    "DYJets": "DY+jets", 
    "WW": "Dibosons",
    "W2Jets_exclusive": "W+Jets",
    "QCD": "QCD",
    "data": "Data"
    }

priors = {"Tbar_t_ToLeptons": 0.1, "T_t_ToLeptons": 0.1,
    "Tbar_tW": 0.1, "T_tW": 0.1, 
    "Tbar_s": 0.1, "T_s": 0.1,
    "TTJets_SemiLept": 0.1, "TTJets_FullLept": 0.1,
    "DYJets": 0.1, 
    "WW": 0.1, "WZ": 0.1, "ZZ": 0.1,
    "W1Jets_exclusive": 0.3, "W2Jets_exclusive": 0.3, "W3Jets_exclusive": 0.3, "W4Jets_exclusive": 0.3,
    "W1JetsToLNu": 0.3, "W2JetsToLNu": 0.3, "W2JetsToLNu2": 0.3, "W3JetsToLNu": 0.3, "W3JetsToLNu2": 0.3, "W4JetsToLNu": 0.3, "W4JetsToLNu2": 0.3
    }

"""datasets_data = [
    "SingleEle1",
    "SingleEle2",
    "SingleEle_miss",
    "SingleMu1",
    "SingleMu2",
    "SingleMu3",
    "SingleMu_miss"
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
]"""
