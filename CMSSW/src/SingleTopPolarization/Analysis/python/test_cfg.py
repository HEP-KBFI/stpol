import FWCore.ParameterSet.Config as cms
from SingleTopPolarization.Analysis.selection_step2_cfg import SingleTopStep2, Config

Config.doMETSystShift = True
#Config.isAMCatNLO = True
Config.bTagDiscriminant = Config.Jets.BTagDiscriminant.CSV
Config.bTagWorkingPoint = Config.Jets.BTagWorkingPoint.CSVT
#Config.subChannel = "TToLeptons_t-channel_Pythia8_8TeV-aMCatNLO"
Config.subChannel = "W3Jets_exclusive"
process = SingleTopStep2()

process.maxEvents.input = 1000

"""process.MessageLogger = cms.Service("MessageLogger",
       destinations = cms.untracked.vstring('cout'),
       #debugModules = cms.untracked.vstring('bTagWeightProducer'),
       #cout = cms.untracked.PSet(threshold = cms.untracked.string('DEBUG')),
)"""

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #"file:/hdfs/cms/store/user/jpata/TTJets_SemiLeptMGDecays_8TeV-madgraph/Sep8_newjec_metsystshift_hermeticproj/b5f3018263c1ef499fcfff38dc3a7740/output_noSkim_234_2_WuB.root",
        "file:/hdfs/cms/store/user/atiko/W3JetsToLNu_TuneZ2Star_8TeV-madgraph/wjets_nominals_clear/bef8661838e52e144800069e7fe2aa7b/output_Skim_345_1_Vaa.root",        
        #"file:/hdfs/cms/store/user/atiko/TToLeptons_t-channel_Tune4C_8TeV-aMCatNLO/mc_atnlo_4c_withlhe/5a79d760a53c9c1be8d01a2c2cc85600/output_noSkim_1_1_HKO.root"
        
    )
)

