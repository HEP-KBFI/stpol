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

from get_weights import *
from utils import sizes, pdfs


print "args", sys.argv
#system.exit(1)
dataset = sys.argv[1]
thispdf = sys.argv[2]
counter = sys.argv[3]
channel = sys.argv[4]
base_filename = sys.argv[5]
added_filename = sys.argv[6]
select = sys.argv[7]
counter_w = int(sys.argv[8])

ROOT.TH1.AddDirectory(False)

#variables = ["bdt_sig_bg", "cos_theta", "pdfweight"]
variables = ["cos_theta_lj_gen"]
var = variables[0]
ranges = {}
ranges["cos_theta_lj"] = (48, -1, 1)
ranges["cos_theta_lj_gen"] = (24, -1, 1)

channels = ["mu", "ele"]
jettag = ["2j1t"]

infile =  TFile.Open(base_filename, "read")
infile2 = TFile.Open(added_filename, "read")

events = infile.Get('dataframe')
#events2 = infile2.Get('dataframe')

(pdf_weights, average_weights, pdf_input) = get_weights(dataset, thispdf, channel, counter, counter_w, dont_skim= True)

histograms = dict()

c = channel
luminosity = 19670
if channel == "ele":
    luminosity = 19637
    
#bdt_cuts = ["-0.20000",  "-0.10000", "0.00000", "0.06000",  "0.10000", "0.13000", "0.20000", "0.25000", "0.30000", "0.35000", "0.40000", "0.45000", "0.50000", "0.55000", "0.60000", "0.65000", "0.70000", "0.75000", "0.80000"]

histograms[c] = dict()
for p in pdfs:
    if not (thispdf == p or (p == 'NNPDF23' and thispdf == "NNPDF23nloas0119LHgrid")): continue
    histograms[c][p] = dict()
    name = "cos_theta_lj_gen__%s__%s" % (dataset, p)
    histograms[c][p]["nominal"] = TH1D(name+"__nominal", name+"_nominal", ranges[var][0], ranges[var][1], ranges[var][2])
    histograms[c][p]["nominal"].SetDirectory(0)
    histograms[c][p]["nominal"].Sumw2()
    histograms[c][p]["weighted"] = []
    for i in range(sizes[p]):
        thisname = name + "__weighted_" + str(i)
        histograms[c][p]["weighted"].append(TH1D(thisname, thisname, ranges[var][0], ranges[var][1], ranges[var][2]))
        histograms[c][p]["weighted"][i].SetDirectory(0)
        histograms[c][p]["weighted"][i].Sumw2()
                        
"""
i=-1
for event in events2:
    i+=1
    if event.bdt_qcd <= -0.15: continue
    extra_data[i] = [event.bdt_qcd, event.bdt_sig_bg, event.xsweight, event.wjets_ct_shape_weight, event.wjets_fl_yield_weight]
"""
i=-1

for event in events:
    i+=1
    #if i>100000: break
    #print "Event:", i
    run = event.run
    lumi = event.lumi
    eventid = event.event    

    jt = "%sj%st" % (event.njets, event.ntags)
    genid = event.gen_lepton_id
    if channel == "mu" and not abs(genid) == 13: continue
    if channel == "ele" and not abs(genid) == 11: continue

    if select == "top":
        if not genid == -abs(genid): continue
    elif select == "antitop":
        if not genid == abs(genid): continue
    #xsweight = extra_data[i][2]
    #wjets_shape = extra_data[i][3]
    #wjets_yield = extra_data[i][4]
    #total_weight = event.pu_weight * event.lepton_weight__id * event.lepton_weight__iso * event.lepton_weight__trigger \
    #         * wjets_shape * wjets_pt * xsweight

    #if math.isnan(event.lepton_weight__id): continue
    #if math.isnan(event.lepton_weight__iso): continue
    #if math.isnan(event.lepton_weight__trigger): continue
    #if not math.isnan(event.b_weight):
    #total_weight *= event.b_weight
    #total_weight *= luminosity

    try:
        pdf_stuff = pdf_weights[run][lumi][eventid]
        other_stuff = pdf_input[run][lumi][eventid]
    except KeyError:
        #print "event missing"
        continue
    for (p, w) in pdf_stuff.items():
        if not (thispdf == p or (p == 'NNPDF23' and thispdf == "NNPDF23nloas0119LHgrid")): continue
        if p not in pdfs: continue
            
        #histograms[channel][p]["nominal"].Fill(bdt, total_weight)
        histograms[channel][p]["nominal"].Fill(event.cos_theta_lj_gen, 1)#bdt, total_weight)
        #histograms[channel][p]["cos_theta"][jt]["nominal_cut_%s" % cut_val].Fill(event.cos_theta_lj, total_weight)
        #print event.cos_theta_lj, event.cos_theta_lj_gen, 1
        if not "NNPDF" in p:
            for j in range(len(w)):
                #this_weight = total_weight * w[j]
                this_weight = w[j]
                #if (dataset.startswith("T_t") and not dataset.startswith("T_tW")) or (dataset.startswith("Tbar_t") and not dataset.startswith("Tbar_tW")):
                this_weight /= average_weights[p][j]
                histograms[channel][p]["weighted"][j].Fill(event.cos_theta_lj_gen, this_weight)
                #print j, event.cos_theta_lj_gen, w[j]
                

print "writing"
#path = os.path.join(os.environ["STPOL_DIR"], "src", "pdf_uncertainties", "output_removestrange")
path = os.path.join(os.environ["STPOL_DIR"], "src", "pdf_uncertainties", "gen_output")
if select == "top":
	path = os.path.join(os.environ["STPOL_DIR"], "src", "pdf_uncertainties", "gen_output_top2")
elif select == "antitop":
    path = os.path.join(os.environ["STPOL_DIR"], "src", "pdf_uncertainties", "gen_output_antitop2")

    #path = os.path.join(os.environ["STPOL_DIR"], "src", "pdf_uncertainties", "output_skip")
#path = os.path.join(os.environ["STPOL_DIR"], "src", "pdf_uncertainties", "output_events")
outfilename = "%s/gen_%s_%s_%s_%s_%d.root" % (path, channel, dataset, thispdf, counter, counter_w)
outfile = TFile(outfilename, "RECREATE")
for p in histograms[channel]:
    print histograms[channel][p]["nominal"].GetEntries(), histograms[channel][p]["nominal"].Integral()
    histograms[channel][p]["nominal"].Write()
    for h in histograms[channel][p]["weighted"]:
        print h.Integral()
        h.Write()
        
outfile.Write()
outfile.Close()
print "finished"             

        
