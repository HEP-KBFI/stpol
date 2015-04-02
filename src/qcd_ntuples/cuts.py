#ROOT.gSystem.Load("libFWCoreFWLite.so")
#ROOT.AutoLibraryLoader.enable()
from PhysicsTools.PythonAnalysis import *
from DataFormats.FWLite import Events, Handle, Lumis
import math

def passes_cuts(event, channel, iso="iso", iso_var=None):
    if event.njets == 2: 
        if event.ntags > 1: return False
    elif event.njets == 3:
        if event.ntags > 2: return False
        if event.ntags < 1: return False
    else: return False
    

    #if not event.njets == 2: return False
    #if not event.ntags == 1: return False
    
    if event.n_signal_mu == 1 and abs(event.lepton_type) == 13:
        ch = "mu"
    elif event.n_signal_ele == 1 and abs(event.lepton_type) == 11:
        ch = "ele"
    else: return False
    if not ch == channel: return False

    if event.n_veto_mu > 0 or event.n_veto_ele > 0: return False
    
    if event.bjet_pt <= 40 or event.ljet_pt <= 40: return False
    if abs(event.bjet_eta) >= 4.5 or abs(event.ljet_eta) >= 4.5: return False
    
    #if channel == "mu" and event.lepton_pt <= 26: return False  #no effect on top of step3
    #if channel == "ele" and event.lepton_pt <= 30: return False #no effect on top of step3
    if channel == "mu" and event.hlt_mu != 1: return False
    if channel == "ele" and event.hlt_ele != 1: return False
    if event.bjet_dr <= 0.3 or event.ljet_dr <= 0.3: return False
    

    
    run = event.run
    lumi = event.lumi
    eventid = event.event    
    
    if math.isnan(event.lepton_weight__id): return False
    if math.isnan(event.lepton_weight__iso): return False
    if math.isnan(event.lepton_weight__trigger): return False
    if math.isnan(event.b_weight): return False
    
    if iso == "antiiso":
        if iso_var == "down":
            if channel == "mu" and not (event.lepton_iso < 0.3): return False
            if channel == "ele" and not (event.lepton_iso < 0.25): return False
        elif iso_var == "up":
            if channel == "mu" and (event.lepton_iso < 0.3 or event.lepton_iso > 0.5): return False
            if channel == "ele" and (event.lepton_iso < 0.25 or event.lepton_iso > 0.5): return False
        else:
            if event.lepton_iso > 0.5 or event.lepton_iso < 0.15: return False
        #else: break
    return True

def cos_theta_bin(cos_theta, bin):
    if math.isnan(cos_theta):
        return False
    if cos_theta > (-1 + (bin - 1) * (1./3)) and cos_theta <= (-1 + bin * (1./3)):
        return True
    return False
