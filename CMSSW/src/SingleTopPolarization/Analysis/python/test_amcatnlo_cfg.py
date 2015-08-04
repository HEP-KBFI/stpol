import FWCore.ParameterSet.Config as cms
from SingleTopPolarization.Analysis.selection_step2_cfg import SingleTopStep2, Config

Config.doMETSystShift = True
Config.isAMCatNLO = True
Config.bTagDiscriminant = Config.Jets.BTagDiscriminant.CSV
Config.bTagWorkingPoint = Config.Jets.BTagWorkingPoint.CSVT
Config.subChannel = "TToLeptons_t-channel_Pythia8_8TeV-aMCatNLO"
process = SingleTopStep2()

process.maxEvents.input = 10000

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring("file:/hdfs/cms/store/user/atiko/TToLeptons_t-channel_Tune4C_8TeV-aMCatNLO/mc_atnlo_4c/5a79d760a53c9c1be8d01a2c2cc85600/output_noSkim_2_1_ZMm.root"
    )
)

