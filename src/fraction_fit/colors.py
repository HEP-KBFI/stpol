import ROOT

colors = {
    'tchan': ROOT.kRed,
    'T_t': ROOT.kRed,
    'Tbar_t': ROOT.kRed,
    'T_t_ToLeptons': ROOT.kRed,
    'Tbar_t_ToLeptons': ROOT.kRed,
    'T_tW': ROOT.kYellow+4,
    'Tbar_tW': ROOT.kYellow+4,
    'T_s': ROOT.kYellow+2,
    'Tbar_s': ROOT.kYellow+2,

    'DYJets': ROOT.kViolet,

    'WJets': ROOT.kGreen,
    'wzjets': ROOT.kGreen,
    'WJets_inclusive': ROOT.kGreen,
    'W1Jets_exclusive': ROOT.kGreen,
    'W2Jets_exclusive': ROOT.kGreen,
    'W3Jets_exclusive': ROOT.kGreen,
    'W4Jets_exclusive': ROOT.kGreen,
    'WJets_sherpa': ROOT.kCyan,
    'W1JetsToLNu': ROOT.kGreen,
    'W2JetsToLNu': ROOT.kGreen,
    'W2JetsToLNu2': ROOT.kGreen,
    'W3JetsToLNu': ROOT.kGreen,
    'W3JetsToLNu2': ROOT.kGreen,
    'W4JetsToLNu': ROOT.kGreen,
    'W4JetsToLNu2': ROOT.kGreen,
    

    'diboson': ROOT.kBlue,
    'WW': ROOT.kBlue,
    'WZ': ROOT.kBlue,
    'ZZ': ROOT.kBlue,

    'TTJets': ROOT.kOrange,
    'TTJets_MassiveBinDECAY': ROOT.kOrange,
    'TTJets_FullLept': ROOT.kOrange,
    'TTJets_SemiLept': ROOT.kOrange,

    'QCD': ROOT.kGray,
    'QCDMu': ROOT.kGray,
    'GJets': ROOT.kGray,
    'GJets1': ROOT.kGray,
    'GJets2': ROOT.kGray,

    'QCDEle': ROOT.kGray,
    'QCD_Pt_20_30_EMEnriched': ROOT.kGray,
    'QCD_Pt_30_80_EMEnriched': ROOT.kGray,
    'QCD_Pt_80_170_EMEnriched': ROOT.kGray,
    'QCD_Pt_170_250_EMEnriched': ROOT.kGray,
    'QCD_Pt_250_350_EMEnriched': ROOT.kGray,
    'QCD_Pt_350_EMEnriched': ROOT.kGray,


    'QCD_Pt_20_30_BCtoE': ROOT.kGray,
    'QCD_Pt_30_80_BCtoE': ROOT.kGray,
    'QCD_Pt_80_170_BCtoE': ROOT.kGray,
    'QCD_Pt_170_250_BCtoE': ROOT.kGray,
    'QCD_Pt_250_350_BCtoE': ROOT.kGray,
    'QCD_Pt_350_BCtoE': ROOT.kGray,

    'data': ROOT.kBlack,
    'SingleMu': ROOT.kBlack,
    'SingleEle': ROOT.kBlack,

    'ttjets': ROOT.kOrange,
    'wzjets_heavy': ROOT.kGreen+3,
    'wzjets_light': ROOT.kGreen,
    'wzjets_charm': ROOT.kGreen-8,
    'qcd': ROOT.kGray,
    'VV': ROOT.kBlue,
}

names = {   
    'tchan': 't-channel',
    'ttjets': 'top',
    'wzjets': 'EW',
    'wzjets_heavy': 'EW heavy',
    'wzjets_light': 'EW light',
    'wzjets_charm': 'EW charm',
    'qcd': 'QCD',
    'VV': 'VV',
    'diboson': 'VV',
}

axis_name = {
    "2j0t_bjet_bd_b": "CSV of highest b-tag jet, 2j0t",
    "2j1t_bjet_bd_b": "CSV of highest b-tag jet, 2j1t",
    "2j0t_ljet_bd_b": "CSV of lowest b-tag jet, 2j0t",
    "2j1t_ljet_bd_b": "CSV of lowest b-tag jet, 2j1t",
    "2j0t_C": "C parameter, 2j0t",
    "2j1t_C": "C parameter, 2j1t",
    "3j2t_C": "C parameter, 3j2t",
    "2j0t_abs_ljet_eta": "|eta| of lowest b-tag jet, 2j0t",
    "2j1t_abs_ljet_eta": "|eta| of lowest b-tag jet, 2j1t",
    "3j2t_abs_ljet_eta": "|eta| of lowest b-tag jet, 3j2t",
    "2j0t_cos_theta_lj": "cos_theta, 2j0t",
    "2j1t_cos_theta_lj": "cos_theta, 2j1t",
    "3j2t_cos_theta_lj": "cos_theta, 3j2t",
    "2j0t_bdt_sig_bg": "Signal BDT, 2j0t",
    "2j1t_bdt_sig_bg": "Signal BDT, 2j1t",
    "3j2t_bdt_sig_bg": "Signal BDT, 3j2t",
}
