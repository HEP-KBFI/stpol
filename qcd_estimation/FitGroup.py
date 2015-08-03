from odict import *
from copy import copy

class FitGroup():
    def __init__(self, name):
        self.name = name
        #self.cut
        #self.order = None
        self.columns = "|l|l|l|c|c|c|c|"



jt_order = ["2j1t", "2j0t", "3j1t", "3j2t"]
channel_order = ["mu", "ele"]

nominalFit = FitGroup("nominal")
#nominal.cut
#nominal.order = OrderedDict({"jt": jt_order, "channel": channel_order})
nominalFit.columns = "|l|l|c|c|c|c|"
nominalFit.header = "Region & Lepton & Scale factors & Event yields & Event yields& Chi^2/NDF \\\\ \n"
nominalFit.header += " & & & before QCD cut	& after QCD cut & \\\\ \n"
nominalFit.caption = "QCD fit results"

mvaNometFit = FitGroup("qcd_mva_nomet")
mvaNometFit.columns = "|l|l|c|c|c|c|"
mvaNometFit.header = "Region & Lepton & Scale factors & Event yields & Event yields& Chi^2/NDF \\\\ \n"
mvaNometFit.header += " & & & before QCD cut	& after QCD cut & \\\\ \n"
mvaNometFit.caption = "QCD fit results, QCD MVA without MET"

mvaNometFit_qcdcut = copy(mvaNometFit)
mvaNometFit_qcdcut.name = "qcd_mva_nomet_qcdcut"
mvaNometFit_qcdcut.caption = "QCD fit results, QCD MVA without MET, loose cut"

dPhisNoMetFit = FitGroup("bdt_qcd_dphis_nomet") 
dPhisNoMetFit.columns = "|l|l|c|c|c|c|"
dPhisNoMetFit.header = "Region & Lepton & Scale factors & Event yields & Event yields& Chi^2/NDF \\\\ \n"
dPhisNoMetFit.header += " & & & before QCD cut	& after QCD cut & \\\\ \n"
dPhisNoMetFit.caption = "QCD fit results, QCD MVA with dPhi variables, without MET"

dPhisNoMetFit_qcdcut = copy(dPhisNoMetFit)
dPhisNoMetFit_qcdcut.name = "bdt_qcd_dphis_nomet_qcdcut"
dPhisNoMetFit_qcdcut.caption = "QCD fit results, QCD MVA with dPhi variables, without MET, loose cut on QCD MVA"

dPhisMetFit = FitGroup("bdt_qcd_dphis_withmet")
dPhisMetFit.columns = "|l|l|c|c|c|c|"
dPhisMetFit.header = "Region & Lepton & Scale factors & Event yields & Event yields& Chi^2/NDF \\\\ \n"
dPhisMetFit.header += " & & & before QCD cut	& after QCD cut & \\\\ \n"
dPhisMetFit.caption = "QCD fit results, QCD MVA with dPhi variables and MET"

dPhisMetFit_qcdcut = copy(dPhisMetFit)
dPhisMetFit_qcdcut.name = "bdt_qcd_dphis_withmet_qcdcut"
dPhisMetFit_qcdcut.caption = "QCD fit results, QCD MVA with dPhi variables and MET, loose cut on QCD MVA"


isovarFit = FitGroup("isovar")
isovarFit.header = "Region & Lepton & Anti-Iso & Scale factors & Event yields & Event yields& Chi^2/NDF \\\\ \n"
isovarFit.header += " & & & & before QCD cut	& after QCD cut & \\\\ \n"
isovarFit.caption = "QCD fit results with variated boundaries of anti-isolated region."

varMCFit = FitGroup("varMC")
varMCFit.header = "Region & Lepton & MC & Scale factors & Event yields & Event yields& Chi^2/NDF \\\\ \n"
varMCFit.header += " & &subtraction& & before QCD cut	& after QCD cut & \\\\ \n"
varMCFit.caption = "QCD fit with variated MC subtraction\label{tab:qcd_MC_sub_var}."

nocutFit = FitGroup("nocut")
nocutFit.columns = "|l|l|c|c|c|c|"
nocutFit.header = "Region & Lepton & Scale factors & Event yields & Event yields& Chi^2/NDF \\\\ \n"
nocutFit.header += " & & & before QCD cut	& after QCD cut & \\\\ \n"
nocutFit.caption = "QCD fit results, fitted on full BDT region"

qcdcutFit = copy(nocutFit)
qcdcutFit.name = "qcdcut"
qcdcutFit.caption = "QCD fit results, fitted on BDT distribution with loose cut"

metmtwFit = FitGroup("metmtw")
metmtwFit.header = "Region & Lepton & Variable & Scale factors & Event yields & Event yields& Chi^2/NDF \\\\ \n"
metmtwFit.header += " & & & & before QCD cut	& after QCD cut & \\\\ \n"
metmtwFit.caption = "QCD fit results with $\mTW$ (for muons) and $\MET$ (for electrons) variables, which were used in the PAS. NB! Event yields after cut are not directly comparable to the nominal fit, as the cut is on a different variable"

metmtwFit_qcdcut = copy(metmtwFit)
metmtwFit_qcdcut.name = "metmtw_qcdcut"
metmtwFit_qcdcut.caption = "QCD fit results with $\mTW$ (for muons) and $\MET$ (for electrons) variables, loosely cut. NB! Event yields after cut are not directly comparable to the nominal fit, as the cut is on a different variable"


groupings = {
    "nominal": nominalFit,
    "isovar": isovarFit,
    "nocut": nocutFit,
    "metmtw": metmtwFit,
    "varMC": varMCFit,
    "qcd_mva_nomet": mvaNometFit,
    "bdt_qcd_dphis_nomet": dPhisNoMetFit,
    "bdt_qcd_dphis_withmet": dPhisMetFit,
    "qcdcut": qcdcutFit,
    "metmtw_qcdcut": metmtwFit_qcdcut,
    "qcd_mva_nomet_qcdcut": mvaNometFit_qcdcut,
    "bdt_qcd_dphis_nomet_qcdcut": dPhisNoMetFit_qcdcut,
    "bdt_qcd_dphis_withmet_qcdcut": dPhisMetFit_qcdcut
    
    
}
"""
region = "full variable range"
    if cuttype == "qcdcut":
        region = "above QCD cut"
    elif cuttype == "reversecut":
        region = "below QCD cut"""
