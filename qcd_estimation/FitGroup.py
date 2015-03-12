from odict import *

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

metmtwFit = FitGroup("metmtw")
metmtwFit.header = "Region & Lepton & Variable & Scale factors & Event yields & Event yields& Chi^2/NDF \\\\ \n"
metmtwFit.header += " & & & & before QCD cut	& after QCD cut & \\\\ \n"
metmtwFit.caption = "QCD fit results with $\mTW$ (for muons) and $\MET$ (for electrons) variables, which were used in the PAS. NB! Event yields after cut are not directly comparable to the nominal fit, as the cut is on a different variable"

groupings = {
    "nominal": nominalFit,
    "isovar": isovarFit,
    "nocut": nocutFit,
    "metmtw": metmtwFit,
    "varMC": varMCFit
}
"""
region = "full variable range"
    if cuttype == "qcdcut":
        region = "above QCD cut"
    elif cuttype == "reversecut":
        region = "below QCD cut"""
