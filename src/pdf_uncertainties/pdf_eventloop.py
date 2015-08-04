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
#Monkey-patch the system path to import the stpol header
#sys.path.append(os.path.join(os.environ["STPOL_DIR"], "src/headers"))
#from stpol import stpol, list_methods




from get_weights import *
from utils import sizes
from utils import pdfs_minset as pdfs
#from src.qcd_mva.utils import *
#from src.qcd_mva.mva_variables import *
#from Dataset import *


print "args", sys.argv
#system.exit(1)
dataset = sys.argv[1]
thispdf = sys.argv[2]
counter = sys.argv[3]
channel = sys.argv[4]
base_filename = sys.argv[5]
added_filename = sys.argv[6]
select = sys.argv[7]

ROOT.TH1.AddDirectory(False)

variables = ["bdt_sig_bg", "cos_theta", "bdt_qcd", "pdfweight"]
variables.extend(["scale", "id1", "id2", "x1", "x2"])

ranges = {}
#ranges["bdt_sig_bg"] = (30, -1, 1)
#ranges["cos_theta"] = (48, -1, 1)
ranges["bdt_sig_bg"] = (20, -1, 1)
ranges["cos_theta"] = (20, -1, 1)
ranges["bdt_qcd"] = (20, -1, 1)
ranges["pdfweight"] = (100, -200, 200)
ranges["scale"] = (100, 150, 500)
ranges["id1"] = (13, -6.5, 6.5)
ranges["id2"] = (13, -6.5, 6.5)
ranges["x1"] = (25, 0, 1)
ranges["x2"] = (25, 0, 1)

channels = ["mu", "ele"]
jettag = ["2j1t", "2j0t", "3j1t", "3j2t"]
histos = {}

infile =  TFile.Open(base_filename, "read")
infile2 = TFile.Open(added_filename, "read")

events = infile.Get('dataframe')
events2 = infile2.Get('dataframe')

colnames = ["bdt_qcd", "bdt_sig_bg", "xsweight", "wjets_ct_shape_weight", "wjets_fl_yield_weight", "wjets_pt_weight"]
extra_data = {}

(pdf_weights, average_weights, pdf_input) = get_weights(dataset, thispdf, channel, counter, -1)
maxscale = 200
minscale = 170
maxid = 0
minid = 0
maxx = 0.
minx = 0.

histograms = dict()

c = channel
#luminosity  = 19764
luminosity = 19670
if channel == "ele":
    #luminosity = 19820
    luminosity = 19637
    
    


#epath = os.path.join(os.environ["STPOL_DIR"], "src", "pdf_uncertainties", "output_events_new")
#efname = "%s/eventlist_%s_%s_%s_%s.txt" % (epath, channel, dataset, thispdf, counter)
#ef = open(efname, 'w')
bdt_cuts = ["-0.20000",  "-0.10000", "0.00000", "0.06000",  "0.10000", "0.13000", "0.20000", "0.25000", "0.30000", "0.35000", "0.40000", "0.45000", "0.50000", "0.55000", "0.60000", "0.65000", "0.70000", "0.75000", "0.80000"]

binned_weights = {}
binned_weights["cos_theta"] = []
binned_weights["bdt_sig_bg"] = []
binned_weights["bdt_qcd"] = []

histograms[c] = dict()
pdfs = [thispdf]
for p in pdfs:
        histograms[c][p] = dict()
        if not (thispdf == p or (p == 'NNPDF23' and thispdf == "NNPDF23nloas0119LHgrid")): continue
        for var in variables:
            histograms[c][p][var] = dict()
            histograms[c][p]["id1id2"] = dict()
            for jt in jettag:
                histograms[c][p][var][jt] = dict()
                histograms[c][p]["id1id2"][jt] = dict()
                name = "pdf__%s_%s__%s__%s" % (jt, var, dataset, p)
                if not var in ["scale", "id1", "id2", "x1", "x2"]:
                    if var == "cos_theta":
                        for bdtcut in bdt_cuts:
                            histograms[c][p][var][jt]["nominal_cut_%s" %bdtcut] = TH1D(name+"_nominal_cut_%s" %bdtcut, name+"_nominal_cut_%s" %bdtcut, ranges[var][0], ranges[var][1], ranges[var][2])
                            histograms[c][p][var][jt]["nominal_cut_%s" % bdtcut].SetDirectory(0)
                            histograms[c][p][var][jt]["nominal_cut_%s" % bdtcut].Sumw2()
                            histograms[c][p][var][jt]["weighted_cut_%s" % bdtcut] = []
                    else:
                        for selection in ["preqcd", "preselection"]:
                            histograms[c][p][var][jt]["nominal_%s" % selection] = TH1D(name+"_nominal_%s" % selection, name+"_nominal_%s" % selection, ranges[var][0], ranges[var][1], ranges[var][2])
                            histograms[c][p][var][jt]["nominal_%s" % selection].SetDirectory(0)
                            histograms[c][p][var][jt]["nominal_%s" % selection].Sumw2()
                            histograms[c][p][var][jt]["weighted_%s" % selection] = []

                for i in range(sizes[p]):
                    if var == "pdfweight": continue
                    if var in ["scale", "id1", "id2", "x1", "x2"]: continue
                    thisname = name + "_weighted_" + str(i)
                    if var == "cos_theta":
                        for bdtcut in bdt_cuts:
                            histograms[c][p][var][jt]["weighted_cut_%s" % bdtcut].append(TH1D(thisname+"_cut_%s" % bdtcut, thisname+"_cut_%s" % bdtcut, ranges[var][0], ranges[var][1], ranges[var][2]))
                            histograms[c][p][var][jt]["weighted_cut_%s" % bdtcut][i].SetDirectory(0)
                            histograms[c][p][var][jt]["weighted_cut_%s" % bdtcut][i].Sumw2()
                    else:
                        for selection in ["preqcd", "preselection"]:
                            thisname = "%s_weighted_%s_%d" % (name, selection, i)
                            histograms[c][p][var][jt]["weighted_%s" % selection].append(TH1D(thisname, thisname, ranges[var][0], ranges[var][1], ranges[var][2]))
                            #print c, p, var, jt, i, len(histograms[c][p][var][jt]["weighted"]), histograms[c][p][var][jt]["weighted"][i]
                            #print histograms[c][p][var][jt]["weighted"][i].GetEntries()
                            histograms[c][p][var][jt]["weighted_%s" % selection][i].SetDirectory(0)
                            histograms[c][p][var][jt]["weighted_%s" % selection][i].Sumw2()
                if var in ["scale", "id1", "id2", "x1", "x2"]:
                    histograms[c][p][var][jt]["nobdtcut"] = TH1D(name, name, ranges[var][0], ranges[var][1], ranges[var][2])
                    histograms[c][p][var][jt]["final"] = TH1D(name+"_final", name+"_final", ranges[var][0], ranges[var][1], ranges[var][2]) 
                    

path = os.path.join(os.environ["STPOL_DIR"], "src", "pdf_uncertainties", "eventlists")
picklename = "%s/events_%s_%s.pkl" % (path, dataset, counter)
with open(picklename, 'rb') as f:
    outdata = pickle.load(f)
    outdatai = pickle.load(f)


"""cpath = os.path.join(os.environ["STPOL_DIR"], "src", "pdf_uncertainties", "cutoffs")
picklename = "%s/cutoffs_%s.pkl" % (cpath, dataset)
with open(picklename, 'rb') as f:
    cutoffs = pickle.load(f)
"""
       
i=-1
for event in events2:
    i+=1
    #if event.bdt_qcd <= -0.15: continue
    extra_data[i] = [event.bdt_qcd, event.bdt_sig_bg, event.xsweight, event.wjets_ct_shape_weight, event.wjets_fl_yield_weight, event.wjets_pt_weight]

i=-1
missing = 0
asd = 0
qw = 0

for event in events:
    i+=1
    if not i in extra_data: continue
    
    run = event.run
    lumi = event.lumi
    eventid = event.event    

    if not run in outdata["preqcd"][channel]: continue
    if not lumi in outdata["preqcd"][channel][run]: continue
    if not eventid in outdata["preqcd"][channel][run][lumi]: continue
    if not outdata["preqcd"][channel][run][lumi][eventid] == True: continue

    jt = "%sj%st" % (event.njets, event.ntags)
    if select == "top":
        if not event.lepton_charge == 1: continue
    elif select == "antitop":
        if not event.lepton_charge == -1: continue
    #if channel == "mu" and not (abs(event.lepton_id) == 13): continue
    #if channel == "ele" and not (abs(event.lepton_id) == 11): continue
    qw += 1
    
    
    asd += 1
    
    qcd_bdt = extra_data[i][0]
    #if qcd_bdt < qcd_mva_cut: continue    
    bdt = extra_data[i][1]
    xsweight = extra_data[i][2]
    wjets_shape = extra_data[i][3]
    #wjets_yield = extra_data[i][4]
    wjets_pt = extra_data[i][5]
    #if math.isnan(event.b_weight): 
    #    event.b_weight = 1
    total_weight = event.pu_weight * event.lepton_weight__id * event.lepton_weight__iso * event.lepton_weight__trigger \
             * wjets_shape * wjets_pt * xsweight

    #if eventid in missing_events:
    #missing += 1
    #print "info", eventid, event.pu_weight, event.lepton_weight__id, event.lepton_weight__iso, event.lepton_weight__trigger, event.b_weight, wjets_shape,  wjets_yield, xsweight

    #if event.top_weight > 0:
    #    total_weight *= event.top_weight
    if math.isnan(event.lepton_weight__id): continue
    if math.isnan(event.lepton_weight__iso): continue
    if math.isnan(event.lepton_weight__trigger): continue
    #if not math.isnan(event.b_weight):
    total_weight *= event.b_weight
    
    total_weight *= luminosity

    #print "weights: ",event.pu_weight, event.lepton_weight__id, event.lepton_weight__iso, event.lepton_weight__trigger, \
    #       event.top_weight, event.b_weight, wjets_shape, wjets_yield, xsweight
    #print run, lumi, eventid
    #print pdf_weights
    if not (run in pdf_weights and lumi in pdf_weights[run] and eventid in pdf_weights[run][lumi]):
        missing+=1
        print "MISSING", run, lumi, eventid, "BDT", bdt
        continue
    pdf_stuff = pdf_weights[run][lumi][eventid]
    other_stuff = pdf_input[run][lumi][eventid]
    #print other_stuff
    for (p, w) in pdf_stuff.items():
        #print "thispdf", thispdf, p
        if not (thispdf == p or (p == 'NNPDF23' and thispdf == "NNPDF23nloas0119LHgrid")): continue
        if p not in pdfs: continue
        #print "here"
            
        if math.isnan(histograms[channel][p]["bdt_sig_bg"][jt]["nominal_preqcd"].Integral()): ghts
        
        histograms[channel][p]["bdt_qcd"][jt]["nominal_preqcd"].Fill(qcd_bdt, total_weight)
        histograms[channel][p]["bdt_sig_bg"][jt]["nominal_preqcd"].Fill(bdt, total_weight)

        if not "NNPDF" in p:
            for j in range(len(w)):
                this_weight = total_weight * w[j]
                if (dataset.startswith("T_t") and not dataset.startswith("T_tW")) or (dataset.startswith("Tbar_t") and not dataset.startswith("Tbar_tW")):
                    this_weight /= average_weights[p][j]
                histograms[channel][p]["bdt_qcd"][jt]["weighted_preqcd"][j].Fill(qcd_bdt, this_weight)
                histograms[channel][p]["bdt_sig_bg"][jt]["weighted_preqcd"][j].Fill(bdt, this_weight)
        

        if not run in outdata["preselection"][channel]: continue
        if not lumi in outdata["preselection"][channel][run]: continue
        if not eventid in outdata["preselection"][channel][run][lumi]: continue
        if not outdata["preselection"][channel][run][lumi][eventid] == True: continue

        histograms[channel][p]["bdt_sig_bg"][jt]["nominal_preselection"].Fill(bdt, total_weight)
        #histograms[channel][p]["cos_theta_lj"][jt]["nominal_preselection"].Fill(bdt, total_weight)
        
        if not "NNPDF" in p:
            for j in range(len(w)):
                this_weight = total_weight * w[j]
                if (dataset.startswith("T_t") and not dataset.startswith("T_tW")) or (dataset.startswith("Tbar_t") and not dataset.startswith("Tbar_tW")):
                    this_weight /= average_weights[p][j]
                histograms[channel][p]["bdt_sig_bg"][jt]["weighted_preselection"][j].Fill(bdt, this_weight)
                #histograms[channel][p]["pdfweight"][jt]["nominal"].Fill(w[j])
                
        for cut_val in bdt_cuts:
            if bdt < float(cut_val): continue
            
            histograms[channel][p]["cos_theta"][jt]["nominal_cut_%s" % cut_val].Fill(event.cos_theta_lj, total_weight)
            
            if not "NNPDF" in p:
                for j in range(len(w)):
                    this_weight = total_weight * w[j]
                    if (dataset.startswith("T_t") and not dataset.startswith("T_tW")) or (dataset.startswith("Tbar_t") and not dataset.startswith("Tbar_tW")):
                        this_weight /= average_weights[p][j]
                    histograms[channel][p]["cos_theta"][jt]["weighted_cut_%s" % cut_val][j].Fill(event.cos_theta_lj, this_weight)
                            

print "writing"
#path = os.path.join(os.environ["STPOL_DIR"], "src", "pdf_uncertainties", "output_removestrange")
path = os.path.join(os.environ["STPOL_DIR"], "src", "pdf_uncertainties", "output")
if select == "top":
    path = os.path.join(os.environ["STPOL_DIR"], "src", "pdf_uncertainties", "output_top")    
elif select == "antitop":
    path = os.path.join(os.environ["STPOL_DIR"], "src", "pdf_uncertainties", "output_antitop")

#path = os.path.join(os.environ["STPOL_DIR"], "src", "pdf_uncertainties", "output_skip")
#path = os.path.join(os.environ["STPOL_DIR"], "src", "pdf_uncertainties", "output_events")
outfilename = "%s/pdftest_%s_%s_%s_%s.root" % (path, channel, dataset, thispdf, counter)
outfile = TFile(outfilename, "RECREATE")
for p in histograms[channel]:
        for var in variables:
            if var in ["scale", "id1", "id2", "x1", "x2", "pdfweight"]: continue
            for jt in jettag:
                print p, var, jt
                if var == "cos_theta":
                    for bdtcut in bdt_cuts:
                        print histograms[channel][p][var][jt]["nominal_cut_%s" % bdtcut].GetEntries(), histograms[channel][p][var][jt]["nominal_cut_%s" % bdtcut].Integral()
                        histograms[channel][p][var][jt]["nominal_cut_%s" % bdtcut].Write()
                        for h in histograms[channel][p][var][jt]["weighted_cut_%s" % bdtcut]:
                            print h.Integral()
                            h.Write()
                else:
                    for selection in ["preqcd", "preselection"]:
                        print histograms[channel][p][var][jt]["nominal_%s" % selection].GetEntries(), histograms[channel][p][var][jt]["nominal_%s" % selection].Integral()
                        histograms[channel][p][var][jt]["nominal_%s" % selection].Write()
                        for h in histograms[channel][p][var][jt]["weighted_%s" % selection]:
                            print h.Integral()
                            h.Write()


#ef.close()
outfile.Write()
outfile.Close()
print "missing", missing>0, missing
print qw, asd
#print "minmax", maxscale, minscale, maxid, minid, maxx, minx
print "finished"             

        
