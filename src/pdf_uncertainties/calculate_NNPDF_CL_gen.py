# prepare the FWLite autoloading mechanism
from PhysicsTools.PythonAnalysis import *
from DataFormats.FWLite import Events, Handle, Lumis

import ROOT
from ROOT import TH1D, TH2D, TFile
ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

import sys
import os
from array import array
from time import gmtime, strftime
import math
import shutil

from get_weights_nnpdf import *
from utils import sizes, pdfs
from variables import *

print "args", sys.argv
dataset = sys.argv[1]
thispdf = sys.argv[2]
counter = sys.argv[3]
counter2 = sys.argv[4]
channel = sys.argv[5]
filename = sys.argv[6]
base_filename = sys.argv[7]
added_filename = sys.argv[8]

ROOT.TH1.AddDirectory(False)

infile =  TFile.Open(base_filename, "read")
infile2 = TFile.Open(added_filename, "read")

events = infile.Get('dataframe')
events2 = infile2.Get('dataframe')

(pdf_weights, average_weights, pdf_input) = get_weights_nnpdf(dataset, thispdf, channel, counter2, filename, dont_skim = True)

histograms = dict()

c = channel

binned_weights = {}
binned_weights["cos_theta_lj_gen"] = {}
"""
path = os.path.join(os.environ["STPOL_DIR"], "src", "pdf_uncertainties", "eventlists")
picklename = "%s/events_%s_%s_%s.pkl" % (path, channel, dataset, counter)
with open(picklename, 'rb') as f:
    outdata = pickle.load(f)
    outdatai = pickle.load(f)
"""
for var in ["cos_theta_lj_gen"]:
    binned_weights[var] = {}
    for jt in jettag:
        binned_weights[var][jt] = []

        for mybin in range(ranges[var][0]):
            binned_weights[var][jt].append([])

i=-1
k = -1

missing = 0
for event in events:
    i+=1
    #if not i in extra_data: continue

    run = event.run
    lumi = event.lumi
    eventid = event.event    
    """
    if not run in outdata[channel]: continue
    if not lumi in outdata[channel][run]: continue
    if not eventid in outdata[channel][run][lumi]: continue
    if not outdata[channel][run][lumi][eventid] == True: continue
    """
    """jt = "%sj%st" % (event.njets, event.ntags)
    if event.njets > 3: continue
    if event.njets < 2: continue
    if event.ntags > 2: continue
    if event.ntags == 2 and event.njets < 3: continue
    if event.ntags == 0 and event.njets > 2: continue
    bdt = extra_data[i][1]"""
    """if math.isnan(event.lepton_weight__id): continue
    if math.isnan(event.lepton_weight__iso): continue
    if math.isnan(event.lepton_weight__trigger): continue
    """
    if not (run in pdf_weights and lumi in pdf_weights[run] and eventid in pdf_weights[run][lumi]):
        missing += 1
        continue
    pdf_stuff = pdf_weights[run][lumi][eventid]
    

    nr_replicas = {"NNPDF23nloas0116LHgrid": 5, "NNPDF23nloas0117LHgrid": 27, "NNPDF23nloas0118LHgrid": 72, 
        "NNPDF23nloas0119LHgrid": 100, "NNPDF23nloas0120LHgrid": 72, "NNPDF23nloas0121LHgrid": 27, "NNPDF23nloas0122LHgrid": 5}
    for (p, w) in pdf_stuff.items():
        k += 1
        #if not (thispdf == p or (p == 'NNPDF23' and thispdf == "NNPDF23nloas0119LHgrid")): continue
        #if p not in pdfs: continue
        for j in range(nr_replicas[p]):
            for mybin in range(ranges["cos_theta_lj_gen"][0]):
                lowedge = -1 + mybin * (2. / ranges["cos_theta_lj_gen"][0])
                highedge = -1 + (mybin + 1) * (2. / ranges["cos_theta_lj_gen"][0])
                if event.cos_theta_lj >= lowedge and event.cos_theta_lj <= highedge:  
                    binned_weights["cos_theta_lj_gen"][jt][mybin].append(w[j])                



print "writing"
print "missing", missing
local_path = os.path.join(os.environ["STPOL_DIR"], "src", "pdf_uncertainties", "weightlists_gen")

path = os.path.join("/scratch", "andres", "pdf_weightlist")

try: 
    os.makedirs(path)
except OSError:
    if not os.path.isdir(path):
        raise

try: 
    os.makedirs(local_path+"/"+dataset)
except OSError:
    if not os.path.isdir(local_path+"/"+dataset):
        raise



for var in ["cos_theta_lj_gen"]:
    try: 
        os.makedirs(local_path+"/"+dataset+"/"+var)
    except OSError:
        if not os.path.isdir(local_path+"/"+dataset+"/"+var):
            raise
    for bin in range(ranges[var][0]):
        if len(binned_weights[var][jt][bin]) > 0:
            picklename = "weights__%s__%s__%s__%s__%s__%s__%s.pkl" % (var, channel, thispdf, dataset, counter, counter2, bin)
            outfile = open("%s/%s" % (path, picklename), "wb")    
            #print var, jt, bin, binned_weights[var][jt][bin]
            pickle.dump(binned_weights[var][jt][bin], outfile)    
            outfile.close()
            shutil.move("%s/%s" % (path, picklename), "%s/%s" % (local_path+"/"+dataset+"/"+var, picklename))
print i+1, missing
print "finished"             

        