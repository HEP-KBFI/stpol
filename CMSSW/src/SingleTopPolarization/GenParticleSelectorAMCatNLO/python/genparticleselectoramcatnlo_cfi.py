import FWCore.ParameterSet.Config as cms

process = cms.Process("OWNPARTICLES")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'file:myfile.root'
    )
)

process.genParticleSelectorCompHep = cms.EDProducer('GenParticleSelectorAMCatNLO',
    src=cms.InputTag("genParticles"),
)

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('myOutputFile.root')
)

  
process.p = cms.Path(process.genParticleSelectorAMCatNLO)

process.e = cms.EndPath(process.out)
