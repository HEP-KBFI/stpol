import FWCore.ParameterSet.Config as cms

# Give the process a name
process = cms.Process("PickEvent")

# Tell the process which files to use as the sourdce
process.source = cms.Source ("PoolSource",
          #fileNames = cms.untracked.vstring ("/store/mc/Summer12DR53X/TToLeptons_t-channel_Tune4C_8TeV-aMCatNLO/AODSIM/PU_S10_START53_V19-v1/00000/0077F240-2667-E411-9997-0025905A48C0.root")
          fileNames = cms.untracked.vstring ("/store/mc/Summer12_DR53X/TToLeptons_t-channel_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/0034258A-D7DE-E111-BEE3-00261834B529.root")
)

# tell the process to only run over 100 events (-1 would mean run over
#  everything
process.maxEvents = cms.untracked.PSet(
            input = cms.untracked.int32 (1000)

)

# Tell the process what filename to use to save the output
process.Out = cms.OutputModule("PoolOutputModule",
         fileName = cms.untracked.string ("MyOutputFile_powheg.root")
)

process.Out.outputCommands = cms.untracked.vstring([
                    'drop *',

                    'keep GenEventInfoProduct_generator__*',
                    'keep LHEEventProduct_source__*',
                                          
                    
            ])

# make sure everything is hooked up
process.end = cms.EndPath(process.Out)

