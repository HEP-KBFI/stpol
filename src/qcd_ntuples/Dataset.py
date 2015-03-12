class Dataset:

   #def __init__(self, name, path = "Jul15/", file_name='', xs = 0, MC=True):
   def __init__(self, name, path = "", file_name='', xs = 0, MC=True):
      self._name=name      
      self._file_name=name+".txt"
      self._path = path
      """self._MC=MC
      self._xs = xs
      self._prescale = prescale
      self._files = {}
      self._originalEvents = {}"""

   def GetFillStyle(self):
      if MC:
         return 0   
   
   def getFileName(self):
      return self._path+self._file_name

   def getName(self):
      return self._name

   def isMC(self):
      return self._MC

   def scaleToData(self, dataLumi, syst, iso):
      expected_events = self._xs * dataLumi
      total_events = self.getOriginalEventCount(iso, syst)      
      scale_factor = float(expected_events)/float(total_events)      
      #print "scale: ",self._name,self._file_name,self._xs, dataLumi, self.getOriginalEventCount(iso, syst), scale_factor
      return scale_factor

   def preScale(self):
      return self._prescale

   def addFile(self, syst, iso, f):
      self._files[syst+iso] = f

   def getFile(self, syst, iso):
      #print self._name, syst, iso, self._files, self.isMC
      if not self.isMC(): #for data we don't have systematics
        return self._files["Nominal"+iso]
      else:
        return self._files[syst+iso]

   def setOriginalEventCount(self, count, iso, syst):
      self._originalEvents[iso+syst] = count

   def getOriginalEventCount(self, iso, syst):
      return self._originalEvents[iso+syst] 

   


datasets_signal = []
datasets_signal.append(Dataset("T_t_ToLeptons"))
datasets_signal.append(Dataset("Tbar_t_ToLeptons"))
datasets_signal.append(Dataset("T_t"))
datasets_signal.append(Dataset("Tbar_t"))

datasets_bg = []
datasets_bg.append(Dataset("W1Jets_exclusive"))
datasets_bg.append(Dataset("W2Jets_exclusive"))
datasets_bg.append(Dataset("W3Jets_exclusive"))
datasets_bg.append(Dataset("W4Jets_exclusive"))

datasets_bg.append(Dataset("DYJets"))
datasets_bg.append(Dataset("TTJets_SemiLept"))
datasets_bg.append(Dataset("TTJets_FullLept"))
datasets_bg.append(Dataset("T_s"))
datasets_bg.append(Dataset("Tbar_s"))
datasets_bg.append(Dataset("T_tW"))
datasets_bg.append(Dataset("Tbar_tW"))

datasets_bg.append(Dataset("WW"))
datasets_bg.append(Dataset("WZ"))
datasets_bg.append(Dataset("ZZ"))

datasets_qcdmu = []
datasets_qcdele = []
datasets_qcdele.append(Dataset("GJets1"))
datasets_qcdele.append(Dataset("GJets2"))
datasets_qcdmu.append(Dataset("QCDMu", "Jul15_qcd/"))
datasets_qcdele.append(Dataset("QCD_Pt_20_30_BCtoE", "Jul15_qcd/"))
datasets_qcdele.append(Dataset("QCD_Pt_250_350_EMEnriched", "Jul15_qcd/"))
datasets_qcdele.append(Dataset("QCD_Pt_350_BCtoE", "Jul15_qcd/"))
datasets_qcdele.append(Dataset("QCD_Pt_80_170_EMEnriched", "Jul15_qcd/"))
datasets_qcdele.append(Dataset("QCD_Pt_170_250_BCtoE", "Jul15_qcd/"))
datasets_qcdele.append(Dataset("QCD_Pt_170_250_EMEnriched", "Jul15_qcd/"))
datasets_qcdele.append(Dataset("QCD_Pt_20_30_EMEnriched", "Jul15_qcd/"))
datasets_qcdele.append(Dataset("QCD_Pt_250_350_BCtoE", "Jul15_qcd/"))
datasets_qcdele.append(Dataset("QCD_Pt_30_80_BCtoE", "Jul15_qcd/"))
datasets_qcdele.append(Dataset("QCD_Pt_30_80_EMEnriched", "Jul15_qcd/"))
datasets_qcdele.append(Dataset("QCD_Pt_350_EMEnriched", "Jul15_qcd/"))
datasets_qcdele.append(Dataset("QCD_Pt_80_170_BCtoE", "Jul15_qcd/"))

datasets_inclusive = []
datasets_inclusive.append(Dataset("WJets_inclusive"))
datasets_inclusive.append(Dataset("TTJets_MassiveBinDECAY"))

#dataset_muons
datasets_muons = []
datasets_muons.append(Dataset("SingleMu1"))
datasets_muons.append(Dataset("SingleMu2"))
datasets_muons.append(Dataset("SingleMu3"))
#datasets_muons.append(Dataset("SingleMu_miss", "Aug1/"))
datasets_muons.append(Dataset("SingleMu_miss"))

datasets_electrons = []
datasets_electrons.append(Dataset("SingleEle1"))
datasets_electrons.append(Dataset("SingleEle2"))
datasets_electrons.append(Dataset("SingleEle_miss"))
#datasets_electrons.append(Dataset("SingleEle_miss", "Aug1/"))
