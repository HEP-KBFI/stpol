#!/usr/bin/env cmsRun
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

# Usage: cmsRun OPTIONS
#   or   ./hepmc2edm.py OPTIONS
#
# Description: converts an HEP2MC2 ascii file into an EDM file.
#
# OPTIONS:
#   inputFiles=INPUT_FILE  specifies the input file using CMSSW standard format for the path (file:, /store...).
#                          Add one option per file to read. (default: file:sample.hepmc2).
#   outputFile=OUTPUT_FILE specifies the output file using CMSSW standard format for the path. 
#                          (default: file:sampl.root)
#   maxEvents=MAX_EVENTS   Maximum number of events to process. (default: -1)

process = cms.Process("GEN")

# setup 'analysis'  options
options = VarParsing.VarParsing ('analysis')

#default options:
options.inputFiles= ["file:/hdfs/local/joosep/wjetsnlo/WJets_MENLOPS.hepmc_100_120_140_160.hepmc2g",
    "file:/hdfs/local/joosep/wjetsnlo/WJets_MENLOPS.hepmc_55_66_77_88.hepmc2g",
    "file:/hdfs/local/joosep/wjetsnlo/WJets_MENLOPS.hepmc_10_12_14_16.hepmc2g",
    "file:/hdfs/local/joosep/wjetsnlo/WJets_MENLOPS.hepmc_5_6_7_8.hepmc2g",
    "file:/hdfs/local/joosep/wjetsnlo/WJets_MENLOPS.hepmc_15_18_21_24.hepmc2g",
    "file:/hdfs/local/joosep/wjetsnlo/WJets_MENLOPS.hepmc_60_72_84_96.hepmc2g",
    "file:/hdfs/local/joosep/wjetsnlo/WJets_MENLOPS.hepmc_20_24_28_32.hepmc2g",
    "file:/hdfs/local/joosep/wjetsnlo/WJets_MENLOPS.hepmc_65_78_91_104.hepmc2g",
    "file:/hdfs/local/joosep/wjetsnlo/WJets_MENLOPS.hepmc_25_30_35_40.hepmc2g",
    "file:/hdfs/local/joosep/wjetsnlo/WJets_MENLOPS.hepmc_70_84_98_112.hepmc2g",
    "file:/hdfs/local/joosep/wjetsnlo/WJets_MENLOPS.hepmc_30_36_42_48.hepmc2g",
    "file:/hdfs/local/joosep/wjetsnlo/WJets_MENLOPS.hepmc_75_90_105_120.hepmc2g",
    "file:/hdfs/local/joosep/wjetsnlo/WJets_MENLOPS.hepmc_35_42_49_56.hepmc2g",
    "file:/hdfs/local/joosep/wjetsnlo/WJets_MENLOPS.hepmc_80_96_112_128.hepmc2g",
    "file:/hdfs/local/joosep/wjetsnlo/WJets_MENLOPS.hepmc_40_48_56_64.hepmc2g",
    "file:/hdfs/local/joosep/wjetsnlo/WJets_MENLOPS.hepmc_85_102_119_136.hepmc2g",
    "file:/hdfs/local/joosep/wjetsnlo/WJets_MENLOPS.hepmc_45_54_63_72.hepmc2g",
    "file:/hdfs/local/joosep/wjetsnlo/WJets_MENLOPS.hepmc_90_108_126_144.hepmc2g",
    "file:/hdfs/local/joosep/wjetsnlo/WJets_MENLOPS.hepmc_50_60_70_80.hepmc2g",
    "file:/hdfs/local/joosep/wjetsnlo/WJets_MENLOPS.hepmc_95_114_133_152.hepmc2g" 
]
options.outputFile = 'file:sample.root'
options.maxEvents = -1 # -1 means all events

options.parseArguments()

print options.inputFiles
print options.outputFile
print options.maxEvents

# Standard sequences and services:
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')

# Input:
process.source = cms.Source(
    "MCFileSource",
    fileNames = cms.untracked.vstring (options.inputFiles)
    )

# Number of events to process:
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))

# Logs:
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'

# Vertex smearing:
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic8TeV2012Collision_cfi')

# Producer of generator objects  is "source" instead of usual "generator":
process.VtxSmeared.src   = cms.InputTag("source")
process.genParticles.src = cms.InputTag("source")

# Use default condition tag:
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:mc', '')

#Output:
process.output = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string (options.outputFile),
    outputCommands = cms.untracked.vstring('keep *')
    )

# Path and EndPath definitions
process.generation_step       = cms.Path(process.pgen)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step           = cms.EndPath(process.endOfProcess)
process.output_step           = cms.EndPath(process.output)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,
                                process.genfiltersummary_step,
                                process.endjob_step,
                                process.output_step)
