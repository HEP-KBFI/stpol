#!/bin/env python

# Enable logging module
import logging
logging.basicConfig(level=logging.WARNING)

# import modules needed for argument parsing
import sys
import os
import argparse
from copy import copy

# Get list of samples and variables to be used for training
#from sampleList import *

# Import toolkit items for sample reading, scaling, cutting etc
#from plots.common.sample import Sample
#from plots.common.cuts import Weights
#from plots.common.cross_sections import lumi_iso, lumi_antiiso, xs

# Import the important parts from ROOT
from ROOT import TFile,TTree,TMVA,TCut
import ROOT

from utils import *
from mva_variables import *




def doTMVA(args, filename="", rm_extra=""):
    logger = logging.getLogger('tmva.py')

    if args.debug:
        logger.setLevel(logging.DEBUG)
    ROOT.TMVA.Tools.Instance()
    reader = ROOT.TMVA.Reader( "Color:!Silent" )

    varlist = args.var
    #for v in args.var:
    #    varlist.remove(v)
        
    #of.write(":weight_pileup:weight_toppt:weight_xs")

    #xs = read_cross_sections()

    #speclist= ["cos_theta"]

    #// to get access to the GUI and all tmva macros
    tmva_dir = "/opt/software/root/tmva/"
    if ROOT.gSystem.Getenv("TMVASYS"):
        tmva_dir = ROOT.gSystem.Getenv("TMVASYS")
    ROOT.gROOT.SetMacroPath(tmva_dir + "/test/:" + ROOT.gROOT.GetMacroPath() )
    ROOT.gROOT.ProcessLine(".L TMVAGui.C")

    Use = {}

    Use["KNN"] = 0

    Use["MLP"] = 0  # Recommended ANN
    Use["MLPBNN"] = 0 # Recommended ANN with BFGS training method and bayesian regulator

    #-- Support Vector Machine 
    Use["SVM"] = 0

    #--- Boosted Decision Trees
    Use["BDT"]  = 0 # uses Adaptive Boost
    Use["qcdBDT"]  = 0 # uses Adaptive Boost
    Use["qcdBDTGrad"]  = 0 # uses Gradient Boost
    Use["qcdBDTGrad2"]  = 0 # uses Gradient Boost
    Use["qcdBDTGrad3"]  = 0 # uses Gradient Boost
    Use["qcdBDTGrad4"]  = 0 # uses Gradient Boost
    Use["qcdBDTGrad5"]  = 0 # uses Gradient Boost
    Use["qcdBDTGrad0"]  = 1 # uses Gradient Boost
    Use["qcdBDTGradMixed"]  = 0 # uses Gradient Boost
    Use["BDTold"] = 0


    print "==> Start TMVAClassification"

    # Set the weight expression
    #weightString = str(Weights.total(args.channel) *
    #    Weights.wjets_madgraph_shape_weight() *
    #    Weights.wjets_madgraph_flat_weight())

    extra = "_with"
    for v in varlist:
        extra += '_' + v

    if len(filename) > 0:
        outfileName = filename
    else:
        #outfileName = "TMVA_%s%s_27Jan.root" % (args.channel, "")#extra)
        outfileName = "TMVA_%s%s_27Jan_allvars.root" % (args.channel, "")#extra)
    of = TFile( outfileName, "RECREATE" )

    #factory = TMVA.Factory( "anti_QCD_MVA_28Nov", of, "V:!Silent:Color:DrawProgressBar:Transformations=I;N;D:AnalysisType=Classification" );
    #factory = TMVA.Factory( "anti_QCD_MVA_27Jan_fullData", of, "V:!Silent:Color:DrawProgressBar:Transformations=I;N;D:AnalysisType=Classification" );
    factory = TMVA.Factory( "test", of, "V:!Silent:Color:DrawProgressBar:Transformations=I;N;D:AnalysisType=Classification" );        

    # define variables that we'll use for training
    for v in varlist:
        factory.AddVariable(v,'D')
    #for v in speclist:
    #    factory.AddSpectator(v,'D')

    signalWeight = 1. #samples[s].lumiScaleFactor(lumi),
    backgroundWeight = 1.# * 200
    lumi = 19700
    print args.indir
    for root,dirs,files in os.walk(args.indir):
        #print root
        #print dirs
        #print files
        for filename in files:
            #print filename
            fn = args.indir + "/" + filename
            parts = filename.split("_")
            dsname = "_".join(parts[:-3])
            if ("T_t_ToLeptons" in fn or "Tbar_t_ToLeptons" in fn) and args.channel in fn and "2j1t" in fn and not "antiiso" in fn:
                #print dsname        
                factory.AddSignalTree(fn, signalWeight, TMVA.Types.kTesting)
            elif ("T_t" in fn or "Tbar_t" in fn) and ("tW" not in fn) and args.channel in fn and "2j1t" in fn and not "antiiso" in fn:
                factory.AddSignalTree(fn, signalWeight, TMVA.Types.kTraining);
            #elif "Single" in fn and args.channel in fn and args.channel.capitalize() in fn and "2j0t" in fn:
            #    factory.AddBackgroundTree(fn, backgroundWeight, TMVA.Types.kTraining)
            elif "Single" in fn and args.channel in fn and args.channel.capitalize() in fn and "2j1t" in fn:
                factory.AddBackgroundTree(fn, backgroundWeight)#, TMVA.Types.kTesting)
            elif Use["qcdBDTGradMixed"] == 1 and "Single" in fn and args.channel in fn and args.channel.capitalize() in fn and ("2j0t_21" in fn or "2j0t_11" in fn or "2j0t_31" in fn  or "2j0t_41" in fn):
                factory.AddBackgroundTree(fn, backgroundWeight)#, TMVA.Types.kTraining)
       

    #Apply additional cuts on the signal and background samples (can be different)
    #cuts = "int_lightJetCount__STPOLSEL2==1 && int_bjetCount__STPOLSEL2==1 && int_electronCount__STPOLSEL2==0 && int_muonCount__STPOLSEL2==1";
    mycuts = TCut("bjet_dr > 0.3 && ljet_dr > 0.3")#bjet_dr > 0.3 && ljet_dr > 0.3")#cuts; // for example: TCut mycuts = "abs(var1)<0.5 && abs(var2-0.5)<1";
    mycutb = TCut("bjet_dr > 0.3 && ljet_dr > 0.3")#cuts; // for example: TCut mycutb = "abs(var1)<0.5";

    #wstring = "1"
    
    factory.SetWeightExpression("1")

    factory.PrepareTrainingAndTestTree(mycuts, mycutb,
            #"SplitMode=Block:NormMode=EqualNumEvents::V:SplitSeed=99"
            "SplitMode=Random:NormMode=EqualNumEvents::V"
        )

    # Book MVA methods

    if Use["qcdBDTGrad0"]:  # Gradient Boost
            print outfileName, args.channel
            factory.BookMethod( TMVA.Types.kBDT, "qcdBDT"+"_"+args.channel+rm_extra, "!H:V:NTrees=50:nEventsMin=250:MaxDepth=2:BoostType=Grad:Shrinkage=0.1:!UseBaggedGrad:SeparationType=CrossEntropy:nCuts=200:PruneStrength=7:PruneMethod=CostComplexity")
            """shrinkage = 0.39
            if args.channel == "mu":
                shrinkage = 0.18
            params = "!H:V:NTrees=50:nEventsMin=250:MaxDepth=2:BoostType=Grad:Shrinkage=%f:!UseBaggedGrad:SeparationType=CrossEntropy:nCuts=200" % shrinkage
            factory.BookMethod( TMVA.Types.kBDT, "qcdBDT"+"_"+args.channel+rm_extra, params)"""
            print "booked"

    if Use["qcdBDTGradMixed"]:  # Gradient Boost
        shrinkage = 0.45
        if args.channel == "mu":
            shrinkage = 0.6
        params = "!H:V:NTrees=50:nEventsMin=250:MaxDepth=2:BoostType=Grad:Shrinkage=%f:!UseBaggedGrad:SeparationType=CrossEntropy:nCuts=200" % shrinkage
        factory.BookMethod( TMVA.Types.kBDT, "qcdBDT_mixed_"+"_"+args.channel+rm_extra, params)

    #Boosted Decision Trees
    if Use["qcdBDT"]:  # Adaptive Boost
          factory.BookMethod( TMVA.Types.kBDT, "qcdBDT"+"_"+args.channel, "!H:V:NTrees=850:nEventsMin=250:MaxDepth=2:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=CrossEntropy:nCuts=200:PruneStrength=7:PruneMethod=CostComplexity")

    if Use["qcdBDTGrad"]:  # Gradient Boost
        factory.BookMethod( TMVA.Types.kBDT, "qcdBDTGrad"+"_"+args.channel, "!H:V:NTrees=850:nEventsMin=250:MaxDepth=2:BoostType=Grad:Shrinkage=0.1:!UseBaggedGrad:SeparationType=CrossEntropy:nCuts=200:PruneStrength=7:PruneMethod=CostComplexity")

    if Use["qcdBDTGrad2"]:  # Gradient Boost
        factory.BookMethod( TMVA.Types.kBDT, "qcdBDTGrad2"+"_"+args.channel, "!H:V:NTrees=850:nEventsMin=250:MaxDepth=2:BoostType=Grad:Shrinkage=0.1:!UseBaggedGrad:SeparationType=CrossEntropy:nCuts=200:PruneStrength=7:PruneMethod=CostComplexity")

    if Use["qcdBDTGrad3"]:  # Gradient Boost
        factory.BookMethod( TMVA.Types.kBDT, "qcdBDTGrad3"+"_"+args.channel, "!H:V:NTrees=850:nEventsMin=250:MaxDepth=2:BoostType=Grad:Shrinkage=0.1:UseBaggedGrad:SeparationType=CrossEntropy:nCuts=200:PruneStrength=3:PruneMethod=CostComplexity")

    if Use["qcdBDTGrad4"]:  # Gradient Boost
        factory.BookMethod( TMVA.Types.kBDT, "qcdBDTGrad4"+"_"+args.channel, "!H:V:NTrees=850:nEventsMin=250:MaxDepth=2:BoostType=Grad:Shrinkage=0.1:!UseBaggedGrad:SeparationType=CrossEntropy:nCuts=200:PruneStrength=5:PruneMethod=CostComplexity")

    if Use["qcdBDTGrad5"]:  # Gradient Boost
        factory.BookMethod( TMVA.Types.kBDT, "qcdBDTGrad5"+"_"+args.channel, "!H:V:NTrees=850:nEventsMin=250:MaxDepth=2:BoostType=Grad:Shrinkage=0.1:!UseBaggedGrad:SeparationType=CrossEntropy:nCuts=200:PruneStrength=7:PruneMethod=CostComplexity:DoBoostMonitor")

    
    

    if Use["BDTold"]:
        factory.BookMethod(
            TMVA.Types.kBDT,
            "BDT_from_AN_noDR"+"_"+args.channel, \
            "!H:!V:"\
            "NTrees=2000:"\
            "BoostType=Grad:"\
            "Shrinkage=0.1:"\
            "!UseBaggedGrad:"\
            "nCuts=2000:"\
            "nEventsMin=100:"\
            "NNodesMax=5:"\
            "UseNvars=4:"\
            "PruneStrength=5:"\
            "PruneMethod=CostComplexity:"\
            "MaxDepth=6"
        )

    # For an example of the category classifier usage, see: TMVAClassificationCategory

    #   // ---- Now you can optimize the setting (configuration) of the MVAs using the set of training events
    #   // factory->OptimizeAllMethods("SigEffAt001","Scan");
    #   // factory->OptimizeAllMethods("ROCIntegral","GA");

    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()

    #Save the output
    of.Close()

    print "==> Wrote root file: " + of.GetName()
    print "==> TMVAClassification is done!"

    # Launch the GUI for the root macros
    #if not ROOT.gROOT.IsBatch():
    #    TMVAGui( of )

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Train QCD MVA")
    parser.add_argument(
        "-c",
        "--channel", type=str, required=True, choices=["mu", "ele"], dest="channel", default=None,
        help="the lepton channel to use"
    )
    parser.add_argument(
        "-i",
        "--indir", type=str, required=False, default=(os.environ["STPOL_DIR"] + "/src/qcd_ntuples/mva_input_step3"),
        help="the input directory, which is expected to contain the subdirectories: mu/ele"
    )
    parser.add_argument(
        '-d',
        '--debug', required=False, default=False, action='store_true', dest='debug',
        help='Enable debug printout'
    )
    """parser.add_argument(
        '-l',
        '--lumitag', required=False, default='83a02e9_Jul22', type=str, dest='lumitag',
        help='Luminosity tag for total integrated lumi'
    )"""
    parser.add_argument(
        '-v',
        '--var', required=False, default=[], action='append', type=str, dest="rej_var",
        help='Variable to remove from MVA training'
    )
    parser.add_argument(
        '-r',
        '--rank', required=False, default=[], action='append', type=str, dest="rank_var",
        help='Variable to use in training for rank cumulation'
    )
    args = parser.parse_args()
    
    #args.var = get_fixed(args.channel)
    args.var = get_varlist(args.channel)

    doTMVA(args)
