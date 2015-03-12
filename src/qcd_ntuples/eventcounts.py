import sys
import os
from array import array

#Monkey-patch the system path to import the stpol header
sys.path.append(os.path.join(os.environ["STPOL_DIR"], "src/headers"))
from stpol import stpol, list_methods

import ROOT
from ROOT import TH1D, TFile
#import TMVA
# prepare the FWLite autoloading mechanism
ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()
from PhysicsTools.PythonAnalysis import *
from DataFormats.FWLite import Events, Handle, Lumis



print "args", sys.argv[0], sys.argv[1]
#system.exit(1)
channel = sys.argv[1]
dataset = sys.argv[2]
counter = sys.argv[3]
iso = sys.argv[4]
infile_list = sys.argv[7:]


if True:
    #print file_list_file
    events = Events(infile_list)

    ffile = stpol.stable.file
    
    total_events = 0
    for f in infile_list:
        print f, ffile.total_processed(f)
        total_events += ffile.total_processed(f)
        
    print "Event count", dataset, total_events
              

        
