import FWCore.ParameterSet.Config as cms

process = cms.Process("OWNPARTICLES")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        "file:/hdfs/cms/store/user/atiko/TToLeptons_t-channel_Pythia8_8TeV-aMCatNLO/mc_atnlo/5a79d760a53c9c1be8d01a2c2cc85600/output_noSkim_1_2_NhR.root"
    )
)

process.genParticleSelectorCompHep = cms.EDProducer('GenParticleSelectorAMCatNLO',
    src=cms.InputTag("genParticles"),
)

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('myOutputFile.root')
)

  
process.p = cms.Path(process.genParticleSelectorCompHep)

process.e = cms.EndPath(process.out)
