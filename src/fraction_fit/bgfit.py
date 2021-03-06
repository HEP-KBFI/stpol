import sys
from glob import glob
import tempfile, shutil, os
import ROOT
import ConfigParser
sys.path.append("/".join([os.environ["STPOL_DIR"], "src", "fraction_fit"]))
from colors import *

Config = ConfigParser.ConfigParser(allow_no_value=True)
Config.read(sys.argv[2])

infiles = Config.get("input", "filenames").split(" ")
try:
    prefixes = Config.get("input", "prefixes", []).split(" ")
except ConfigParser.NoOptionError:
    prefixes = []
if len(prefixes)!=len(infiles):
    prefixes = [""]*len(infiles)
outfile = Config.get("output", "filename")
fit_type = Config.get("fit", "type")

import os
import os.path
dn = os.path.dirname(outfile)
if not os.path.exists(dn):
    os.makedirs(dn)
if not os.path.exists(outfile):
    os.makedirs(outfile)

print("outfile=", outfile)
print("infiles=", infiles)

signal = 'tchan' #name of signal process/histogram

syst = Config.get("systematics", "systematic", "nominal")
direction = Config.get("systematics", "direction", "none")
print "syst=", syst, "dir=", direction

def hfilter(hname):
    if "DEBUG" in hname:
        return False
    spl = hname.split("__")
    #print spl


#    #keep W+jets heavy-light splitting
#    if len(spl)==3 and spl[1] == "wjets":
#        return True

    ##remove combined W+jets
    #if len(spl)==2 and spl[1] == "wjets":
    #    print "remove combined W+jets", spl
    #    return False

    #remove systematic
    if len(spl)!=2:
        #print "remove systematic", spl
        return False


    #remove unmerged data
    if "data_" in hname:
        #print "remove data_", spl
        return False

    #remove systematic
    if '__up' in hname or '__down' in hname:
        #print "remove systematic", spl
        return False

    return True

sr = Config.get("fit", "range", "all")
#def htransform(h):
#    return Histogram(h.get_xmin(), 0.6, h.get_values()[0:24], uncertainties=h.get_uncertainties()[0:24], name=h.get_name())
if sr == "all":
    print "selecting full range"
    def htransform(h):
        return h
elif sr == "sub":
    mx = float(Config.get("fit", "max"))
    mn = float(Config.get("fit", "min"))
    n1 = int(Config.get("fit", "firstbin"))
    n2 = int(Config.get("fit", "lastbin"))
    #print len(h.get_values())
    print "selecting subrange", mn, mx, n1, n2
    def htransform(h):
        #return Histogram(mn, mx, h.get_values()[n1:n2], uncertainties=h.get_uncertainties()[n1:n2], name=h.get_name())
        return Histogram(mn, mx, h.get_values(), uncertainties=h.get_uncertainties(), name=h.get_name())
    def htransform_blind2j1t(h):
        return Histogram(mn, mx, h.get_values()[0:15], uncertainties=h.get_uncertainties()[0:15], name=h.get_name())
    

        
def nameconv(n):
    n = n.replace("wjets__heavy", "wjets_heavy")
    #n = n.replace("wjets__light", "wjets_light")
    return n

def nameconv_mu(n):
    n = nameconv(n)
    n = "mu_"+n
    return n
def nameconv_ele(n):
    n = nameconv(n)
    n = "ele_"+n
    return n

all_hists = []

def get_model(infile, pref):

    (fd, filename) = tempfile.mkstemp()
    filename += "_fit_templates.root"
    #print "temp file", filename
    tf0 = ROOT.TFile.Open(infile, "READ")
    tf = ROOT.TFile.Open(filename, "RECREATE")
    tf.Cd("")

    toskip = []
    kns = [k.GetName() for k in tf0.GetListOfKeys()]

    for k in tf0.GetListOfKeys():
        sys.stdout.flush()
        kn = str(k.GetName())

        if "DEBUG" in kn:
            continue
        #if not hfilter(kn):
        #    continue

        if kn in toskip or "%s__%s__%s"%(kn, syst, direction) in kns:
            continue

        #template is the same systematic scenario we have specified
        #rename the systematic to the nominal
        if (syst != "nominal") and ("%s__%s" % (syst, direction) in kn):
            _kn = "__".join(kn.split("__")[0:2])
            print "renaming", kn, "to", _kn
            toskip.append(_kn)
        else:
            #keep the nominal name
            _kn = kn

        _kn = pref + _kn

        #template passes the histogram filter
        if hfilter(_kn):
            #and is not already present in the output file
            if not tf.Get(_kn):
                x = tf0.Get(kn).Clone(_kn)
                print "cloned", kn, "to", _kn, x.Integral()
                x.SetDirectory(tf)
                x.Write()
            else:
                x = tf.Get(_kn)
                x.Sumw2()
                x1 = x.Integral()
                x.Add(tf0.Get(kn))
                x2 = x.Integral()
                print "added", kn, "to", _kn, x1, x2
                raise Exception("Probably this is an error")
                x.SetDirectory(tf)
                x.Write("", ROOT.TObject.kOverwrite)

    hists = {}
    for h in tf.GetListOfKeys():
        if not hfilter(h.GetName()):
            continue
        hi = h.ReadObj()
        hists[hi.GetName().split("__")[1]] = hi
        #print "hist", hi.GetName(), hi.GetEntries(), hi.Integral()

    """k1 = "ttjets" if "ttjets" in hists.keys() else "other"
    #hists["wzjets"].SetMarkerSize(0)
    hists["tchan"].SetMarkerSize(0)
    hists[k1].SetMarkerSize(0)

    #hists["wzjets"].SetFillStyle(1001)
    hists["tchan"].SetFillStyle(1001)
    hists[k1].SetFillStyle(1001)

    #if "2j1t" in hists["DATA"].GetName():
    #    hists["DATA"].GetXaxis().SetRange(0,24);
    hists["DATA"].SetLineColor(ROOT.kBlack)
    hists["DATA"].SetMarkerStyle(ROOT.kDot)
    hists["tchan"].SetLineColor(ROOT.kRed)
    #hists["wzjets"].SetLineColor(ROOT.kGreen)
    hists[k1].SetLineColor(ROOT.kOrange)
    if "qcd" in hists.keys():
        hists["qcd"].SetLineColor(ROOT.kGray)

    #hists["DATA"].SetFillColor(ROOT.kBlack)
    #hists["tchan"].SetFillColor(ROOT.kRed)
    #hists["wzjets"].SetFillColor(ROOT.kGreen)
    #hists[k1].SetFillColor(ROOT.kOrange)
    if "qcd" in hists.keys():
        hists["qcd"].SetLineColor(ROOT.kGray)
        #hists["qcd"].SetFillColor(ROOT.kGray)
    """
    fn = hists["DATA"].GetName().split("__")[0]
    
    canv = ROOT.TCanvas()
    ROOT.gStyle.SetOptStat(0)
    #hists["DATA"].GetXaxis().SetTitle(hists["DATA"].GetName())
    drawData = ROOT.TH1D(hists["DATA"])
    if "2j1t" in hists["DATA"].GetName() and not fit_type == "data":
        for b in range(drawData.GetNbinsX()):
            if b > 15:
                drawData.SetBinContent(b,0)
                drawData.SetBinError(b,0)
    drawData.Scale(1/drawData.Integral())
    drawData.SetLineWidth(2)
    if "bd_b" in fn:
        drawData.SetAxisRange(0, drawData.GetMaximum()*1.25, "Y")
    else:
        drawData.SetAxisRange(0, drawData.GetMaximum()*2.3, "Y")
    drawData.SetNameTitle("","")
    drawData.GetXaxis().SetTitle(axis_name[fn])
    drawData.GetYaxis().SetTitle("")
    drawData.DrawNormalized("E1")
    for (name, hist) in hists.items():
        #print name, hist
        if name == "DATA": continue
        hist.SetLineColor(colors[name])
        hist.SetLineWidth(2)
        hist.DrawNormalized("hist SAME")
    
    

    leg = ROOT.TLegend(0.4,0.6,0.6,0.90)
    leg.SetBorderSize(0)
    leg.SetLineStyle(0)
    leg.SetTextSize(0.04)
    leg.SetFillColor(0)
    leg.AddEntry(drawData,"Data","pl")
    for (name, hist) in hists.items():
        if name == "DATA": continue
        leg.AddEntry(hist,names[name],"l")

    leg.Draw()
    canv.Print(outfile + "/" + fn + "_shapes.pdf")
    canv.Print(outfile + "/" + fn + "_shapes.png")

    canv = ROOT.TCanvas()
    hs = ROOT.THStack("stack", "stack")
    hists["tchan"].SetFillColor(colors["tchan"])
    hs.Add(hists["tchan"])
    for (name, hist) in hists.items():
        if name == "DATA": continue
        hist.SetFillColor(colors[name])
        hist.SetFillStyle(1001)
        if name == "tchan": continue
        hs.Add(hist)

    hs.Draw("HIST")
    #hs.Draw("BAR HIST")
    hists["DATA"].Draw("E1 SAME")
    leg = ROOT.TLegend(0.1,0.6,0.4,0.90)
    leg.SetBorderSize(0)
    leg.SetLineStyle(0)
    leg.SetTextSize(0.04)
    leg.SetFillColor(0)
    leg.AddEntry(drawData,"Data","pl")
    for (name, hist) in hists.items():
        if name == "DATA": continue
        leg.AddEntry(hist,names[name],"l")
    leg.Draw()

    canv.Print(outfile + "/" + fn + "_unscaled.pdf")
    tf.Close()

    all_hists.append(filename)
    
    #fit with blinded data bdt<0 in 2j1t 
    
    if "mu" in infile:
        name_conv = nameconv_mu
    elif "ele" in infile:
        name_conv = nameconv_ele
    
    if "sig_fixed" in fit_type and "2j_1t" in infile:
        htransform_histo = htransform_blind2j1t
    else:
        htransform_histo = htransform
    
    #end    
    """
    #regular fit
    name_conv = nameconv
    htransform_histo = htransform
    #end regular
    """
    model = build_model_from_rootfile(
        filename,
        #This enables the Barlow-Beeston procedure
        # http://www.pp.rhul.ac.uk/~cowan/stat/mcml.pdf
        # http://atlas.physics.arizona.edu/~kjohns/teaching/phys586/s06/barlow.pdf
        include_mc_uncertainties = True,
        histogram_filter = hfilter,
        transform_histo = htransform_histo,
        root_hname_to_convention = name_conv,
    )                

    #os.remove(filename)
    model.fill_histogram_zerobins()
    model.set_signal_processes(signal)

    for o in model.get_observables():
        for p in model.get_processes(o):
            if p == signal:
                continue
            if p == "qcd":
                continue
            if p == "VV" or p == "diboson":
                continue
            #if p == "wzjets_c":
            #    continue
            #try:
            """add_normal_unc(model,
                p,
                mean=float(Config.get("priors", "%s_mean"%p)),
                unc=float(Config.get("priors", "%s_sigma"%p))
            )"""
            model.add_lognormal_uncertainty('%s' % p, math.log(float(Config.get("priors", "%s_mean"%p)) + float(Config.get("priors", "%s_sigma"%p))), p)
            #except:
            #    print "fixing process ", o, p
    #model.add_lognormal_uncertainty('%s' % p, math.log(float(Config.get("priors", "%s_mean"%p)) + float(Config.get("priors", "%s_sigma"%p))), p)
    """add_normal_unc(model,
        "beta_signal",
        mean=float(Config.get("priors", "signal_mean")),
        unc=float(Config.get("priors", "signal_sigma"))
    )"""

    return model

"""
def add_lognormal_unc(model, par, mean=1.0, unc=1.0):
    model.distribution.set_distribution(
        par, 'gauss', mean = mean,
        width=unc, range=[0.0, float("inf")]
    )
    for o in model.get_observables():
        for p in model.get_processes(o):
            print("p=",p)
            if par == p or (par == "beta_signal" and p == "tchan"):
                print "adding parameters for", o, p
                model.get_coeff(o,p).add_factor('id', parameter=par)

def add_normal_unc(model, par, mean=1.0, unc=1.0):
    model.distribution.set_distribution(
        par, 'gauss', mean = mean,
        width=unc, range=[0.0, float("inf")]
    )
    for o in model.get_observables():
        for p in model.get_processes(o):
            print("p=",p)
            if par == p or (par == "beta_signal" and p == "tchan"):
                print "adding parameters for", o, p
                model.get_coeff(o,p).add_factor('id', parameter=par)"""

def build_model(infiles):
    model = None
    for (inf, pref) in zip(infiles, prefixes):
        print "loading model from ",inf
        m = get_model(inf, pref)
        if model is None:
            model = m
        else:
            model.combine(m)
    if not model:
        raise Exception("no model was built from infiles=%s" % infiles)
    return model

model = build_model(infiles)

print "processes:", sorted(model.processes)
print "observables:", sorted(model.get_observables())
print "parameters(signal):", sorted(model.get_parameters(["tchan"]))
print "nbins=", [model.get_range_nbins(o)[2] for o in model.get_observables()]
print model.get_observables()
nbins = sum([model.get_range_nbins(o)[2] for o in model.get_observables()])
model_summary(model)

options = Options()
#options.set("minimizer","strategy","robust")
#options.set("minimizer","strategy","newton_vanilla")
#options.set("minimizer","strategy","minuit_vanilla")
options.set("global", "debug", "true")

#print "options=", options
#dist = "gauss:1.0,0.01"
if fit_type == "mconly" or fit_type== "data":
    dist = "flat"#:[0.,2.]:1.0"
    #dist = "log_normal:%s,%s" % (Config.get("priors", "signal_mean"), Config.get("priors", "signal_sigma"))
    #dist = "gauss:1.0,0.1"
elif fit_type == "sig_fixed":
    dist = "fix:1.0"
result = mle(model,
    input = 'data', n=1, with_covariance=True, options=options, chi2=True, ks=True,
    #input = 'toys-asimov:1.0', n=1, with_covariance=True, options=options, chi2=True, ks=True,
    #signal_prior="flat:[0,1.01]"
    signal_prior=dist
)
model_summary(model)
print "result=", result
values = {}
for name, value in result["tchan"].items():
    if name not in ["__chi2", "__ks", "__nll", "__cov"]:
        val, var = value[0]
        values[name] = val
    #if name == "beta_signal":
    #    beta_signal = val
pred = evaluate_prediction(model, values)
#for name, it in pred["mu_2j1t_bdt_sig_bg"].items():
#    print name, it.get_value_sum()
write_histograms_to_rootfile(pred, "fit_histos.root")


fitresults = {}
values = {}
errors = {}
for process in result[signal]:
    if '__' not in process:
        fitresults[process] = result[signal][process][0]
        if not ("beta_signal" in process):
            values[process] = math.e**(fitresults[process][0] * math.log((float(Config.get("priors", "%s_sigma" %process)) + float(Config.get("priors", "%s_mean" %process)))))
            errors[process] = math.e**((fitresults[process][0] + abs(fitresults[process][1])) * math.log(float(Config.get("priors", "%s_mean" %process)) + float(Config.get("priors", "%s_sigma" %process)))) - values[process]
        else:
            values[process] = fitresults[process][0]
            errors[process] = fitresults[process][1]


pars = sorted(model.get_parameters([signal]))
outpars = copy.copy(pars)

for p in ["qcd"]:
    outpars.append("qcd")
    if p not in values.keys():
        values[p] = 1.0
    if p not in errors.keys():
        errors[p] = 0.0
if "wzjets" not in values.keys():
    for p in ["diboson"]:
        outpars.append("diboson")
        if p not in values.keys():
            values[p] = 1.0
        if p not in errors.keys():
            errors[p] = 0.0

for fn in all_hists:

    tf = ROOT.TFile(fn)

    hists = {}
    for h in tf.GetListOfKeys():
        if not hfilter(h.GetName()):
            continue
        hi = h.ReadObj()
        hists[hi.GetName().split("__")[1]] = hi
        print "hist", hi.GetName(), hi.GetEntries(), hi.Integral()
    hn = hists["DATA"].GetName().split("__")[0]
    canv = ROOT.TCanvas()

    hs = ROOT.THStack("stack", "stack")

    hists["tchan"].SetFillColor(colors["tchan"])
    hists["tchan"].Scale(values["beta_signal"])
    print "scaled hist", hists["tchan"].GetName(), hists["tchan"].GetEntries(), hists["tchan"].Integral()
    hs.Add(hists["tchan"])
    for (name, hist) in hists.items():
        if name == "DATA":
            print "scaled hist", hist.GetName(), hist.GetEntries(), hist.Integral()
            continue
        hist.SetFillColor(colors[name])
        hist.SetLineColor(colors[name])
        hist.SetFillStyle(1001)
        if name == "tchan": continue
        if not name in ["VV"]: 
            hist.Scale(values[name])
        print "scaled hist", hist.GetName(), hist.GetEntries(), hist.Integral()
        hs.Add(hist)

    hs.SetTitle("Stack scaled to fit results")
    hs.SetMaximum(hs.GetMaximum()*1.25)
    hs.Draw("BAR HIST")
    hs.GetXaxis().SetTitle(axis_name[hn])
    #hs.Draw("BAR HIST")
    hists["DATA"].Draw("E1 SAME")
    leg = ROOT.TLegend(0.6,0.6,0.9,0.90)
    #leg = ROOT.TLegend(0.1,0.6,0.4,0.90)
    leg.SetBorderSize(0)
    leg.SetLineStyle(0)
    leg.SetTextSize(0.04)
    leg.SetFillColor(0)
    leg.AddEntry(hists["DATA"],"Data","pl")
    for (name, hist) in hists.items():
        if name == "DATA": continue
        leg.AddEntry(hist,names[name],"lf")
    leg.Draw()

    canv.Print(outfile + "/" + hn + "_scaled.pdf")
    canv.Print(outfile + "/" + hn + "_scaled.png")

for p in ["wzjets_heavy"]:
    if p in values:
        values[p] = 2.0 * values[p]
        errors[p] = 2.0 * errors[p]

#print("pars:", pars)
#print("outpars:", outpars)
n = len(outpars)

cov = result[signal]['__cov'][0]

corr = numpy.zeros((n, n), dtype=numpy.float32)


print("writing covariance file")
covfi = ROOT.TFile(outfile+"_cov.root", "RECREATE")
covmat = ROOT.TH2D("covariance", "covariance", n, 0, n - 1, n, 0, n - 1)
covmat.SetDirectory(covfi)
for i in range(n):
    covmat.GetXaxis().SetBinLabel(i+1, outpars[i])
    for j in range(n):
        covmat.GetYaxis().SetBinLabel(j+1, outpars[j])
        try:
            ci = pars.index(outpars[i])
            cj = pars.index(outpars[j])
            #corr[i][j] = cov[ci][cj] / (errors[outpars[i]] * errors[outpars[j]])
            corr[i][j] = cov[ci][cj] / math.sqrt(cov[ci][ci] * cov[cj][cj])
            covmat.SetBinContent(i + 1, j + 1, cov[ci][cj])
        except Exception as err:
            corr[i][j] = 0#1.0 / (errors[outpars[i]] * errors[outpars[j]])
            covmat.SetBinContent(i + 1, j + 1, 1.0)
        if math.isnan(corr[i][j]): #if NaN because of fixed prior
            corr[i][j] = 0#1.0 / (errors[outpars[i]] * errors[outpars[j]])
            covmat.SetBinContent(i + 1, j + 1, 1.0)
        covmat.SetBinError(i, j, 0.0)
covfi.Write()
covfi.Close()

out = {
    "names": [p for p in outpars],
    "means": [values[p] for p in outpars],
    "errors": [errors[p] for p in outpars],
    "cov": cov.tolist(),
    "corr": corr.tolist(),
    "chi2": result[signal]["__chi2"],
    "nbins": nbins
}

#print corr

print("writing json file")
import json
of = open(outfile+".json", "w")
of.write(json.dumps(out) + "\n")
of.close()

print("writing txt file")
of2 = open(outfile+".txt", "w")
for p in sorted(values.keys()):
    print("%s %f %f" % (p, values[p], errors[p]))
    of2.write("%s %f %f\n" % (p, values[p], errors[p]))
of2.close()

print("all done!")
