class FitConfig():
    """
    Constructor for FitConfig
    Default values valid for fitting in final muon selection are provided
    If you want to change just a few values, using setters is a good idea
    """
    def __init__(self,
            name = "final_selection",    #name will go into output file names 
            trigger = "(HLT_IsoMu24_eta2p1_v11==1 || HLT_IsoMu24_eta2p1_v12==1 || HLT_IsoMu24_eta2p1_v13==1 || HLT_IsoMu24_eta2p1_v14==1 || HLT_IsoMu24_eta2p1_v15==1 || HLT_IsoMu24_eta2p1_v16==1 || HLT_IsoMu24_eta2p1_v17==1)",
            weightMC = "b_weight_nominal*pu_weight*muon_IDWeight*muon_IsoWeight*muon_TriggerWeight",
            baseCuts = "pt_lj>40 && pt_bj>40 && abs(eta_lj)>2.5 && top_mass < 220 && top_mass > 130 && n_jets == 2 && n_tags == 1 && rms_lj<0.025",
            isolationCut = "mu_iso<0.12",
            antiIsolationCut = "mu_iso>0.3 && mu_iso<0.5", 
            antiIsolationCutDown = "mu_iso>0.27 && mu_iso<0.45", 
            antiIsolationCutUp = "mu_iso>0.33 && mu_iso<0.55",
            extraAntiIsoCuts = "deltaR_lj > 0.3 && deltaR_bj > 0.3",
            weightQCD = "pu_weight*muon_IDWeight*muon_IsoWeight*muon_TriggerWeight" #Only needed if taking QCD template from MC           
        ):
        self.name = name
        self.setTrigger(trigger)
        self.setWeightMC(weightMC)
        self.setWeightQCD(weightQCD)
    
        self.setBaseCuts(baseCuts)
        self.setIsolationCut(isolationCut)
        self.setAntiIsolationCut(antiIsolationCut)
        self.setAntiIsolationCutUp(antiIsolationCutUp)
        self.setAntiIsolationCutDown(antiIsolationCutDown)
        self.setExtraAntiIsoCuts(extraAntiIsoCuts)

        self.calcCuts()
    
    """
    Setters for different cuts.
    Remember to call calcCuts after finishing with the setters.
    (Unless you have a special reason not to -  then you have to compose the final cuts yourself)
    """  
    def setTrigger(self, trigger):
        self._trigger = trigger

    def setWeightMC(self, weight):
        self._weightMC = weight

    def setWeightQCD(self, weight):
        self._weightQCD = weight

    def setBaseCuts(self, cut):
        self._baseCuts = cut

    def setIsolationCut(self, cut):
        self._isolationCut = cut

    def setAntiIsolationCut(self, cut):
        self._antiIsolationCut = cut
    
    def setAntiIsolationCutUp(self, cut):
        self._antiIsolationCutUp = cut

    def setAntiIsolationCutDown(self, cut):
        self._antiIsolationCutDown = cut    
    
    def setExtraAntiIsoCuts(self, cut):
        self._extraAntiIsoCuts = cut

    """
    Calculates all necessary cuts from the base values
    In case you need some special configuration, you can change the values manually afterwards
    """
    def calcCuts(self):
        isoCuts = self._trigger + "*(" + self._baseCuts + " && " + self._isolationCut +")"
        self.isoCutsMC = self._weightMC + "*(" + isoCuts +")"
        self.isoCutsData = isoCuts

        antiIsoCuts = self._trigger + "*(" + self._baseCuts + " && " + self._extraAntiIsoCuts + " && " + self._antiIsolationCut +")"
        antiIsoCutsDown = self._trigger + "*(" + self._baseCuts + " && " + self._extraAntiIsoCuts + " && " + self._antiIsolationCutDown +")"
        antiIsoCutsUp = self._trigger + "*(" + self._baseCuts + " && " + self._extraAntiIsoCuts + " && " + self._antiIsolationCutUp +")"
        self.antiIsoCutsMC = self._weightMC + "*(" + antiIsoCuts +")"
        self.antiIsoCutsMCIsoDown = self._weightMC + "*(" + antiIsoCutsDown +")"
        self.antiIsoCutsMCIsoUp = self._weightMC + "*(" + antiIsoCutsUp +")"
        self.antiIsoCutsData = antiIsoCuts
        self.antiIsoCutsDataIsoDown = antiIsoCutsDown
        self.antiIsoCutsDataIsoUp = antiIsoCutsUp
        
        self.antiIsoCutsQCD = self._weightQCD + "*(" + antiIsoCuts +")"
        self.antiIsoCutsQCDIsoDown = self._weightQCD + "*(" + antiIsoCutsDown +")"
        self.antiIsoCutsQCDIsoUp = self._weightQCD + "*(" + antiIsoCutsUp +")"
        

