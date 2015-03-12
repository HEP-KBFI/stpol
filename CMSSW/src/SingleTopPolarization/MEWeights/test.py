import FWCore.ParameterSet.Config as cms

process = cms.Process("OWNPARTICLES")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        #'root://xrootd.unl.edu//store/mc/Summer12_DR53X/TToLeptons_t-channel_scaleup_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/022CADC1-A0D9-E111-9916-0030487FA4CB.root'
        'file:/hdfs/cms/store/user/jpata/TToLeptons_t-channel_8TeV-powheg-tauola/Sep8_newjec_metsystshift_hermeticproj/b5f3018263c1ef499fcfff38dc3a7740/output_noSkim_100_1_5j9.root'
        
    )
)

process.meweights = cms.EDProducer('MEWeightProducer'
)

process.out = cms.OutputModule("PoolOutputModule",
    #pdfsetFile=cms.string("cteq10.LHpdf") # this changes the pdfset file - default is 'cteq6m.LHpdf'
    fileName = cms.untracked.string('myOutputFile.root')
)

  
process.p = cms.Path(process.meweights)

process.e = cms.EndPath(process.out)
