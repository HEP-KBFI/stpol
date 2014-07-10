import sys, imp
from glob import glob
import tempfile, shutil, os
import ROOT
import ConfigParser
Config = ConfigParser.ConfigParser(allow_no_value=True)
Config.read(sys.argv[2])

infiles = Config.get("input", "filenames").split(" ")
outfile = Config.get("output", "filename")
print("outfile=", outfile)
print("infiles=", infiles)

signal = 'tchan' #name of signal process/histogram

syst = Config.get("systematics", "systematic", "nominal")
dir = Config.get("systematics", "direction", "none")

def hfilter(hname):
    spl = hname.split("__")
    #print spl

    #keep W+jets heavy-light splitting
    if len(spl)==3 and spl[1] == "wjets":
        return True
    #remove combined W+jets
    if len(spl)==2 and spl[1] == "wjets":
        return False

    if len(spl)!=2:
        return False


    if "data_" in hname:
        return False
    #if "qcd" in hname:
    #    return False

    if '__up' in hname or '__down' in hname:
        return False
    return True

def nameconv(n):
    n = n.replace("wjets__heavy", "wjets_heavy")
    n = n.replace("wjets__light", "wjets_light")
    return n

def get_model(infile):

    (fd, filename) = tempfile.mkstemp()
    filename += "_fit_templates.root"
    print("temp file", filename)
    #shutil.copy(infile, filename)
    tf0 = ROOT.TFile.Open(infile, "READ")
    tf = ROOT.TFile.Open(filename, "RECREATE")
    tf.Cd("")
    for k in tf0.GetListOfKeys():
        kn = k.GetName()

        #template is the same systematic scenario we have specified
        #rename the systematic to the nominal
        if syst!="nominal" and "%s__%s"%(syst, dir) in kn:
            _kn = "__".join(kn.split("__")[0:2])
            print "renaming", kn, "to", _kn
        #keep the nominal name
        else:
            _kn = kn
        _kn = nameconv(kn)

        #template passes the histogram filter
        if hfilter(_kn):

            sample = _kn.split("__")[1]
            try:
                gr = Config.get("grouping", sample, None)
            except:
                gr = None

            if gr is None:
                gr = sample
            _kn_new = _kn.split("__")[0] + "__" + gr
            print "grouping",_kn, _kn_new
            _kn = _kn_new
            #and is not already present in the output file
            if not tf.Get(_kn):
                x = tf0.Get(kn).Clone(_kn)
                print("cloned", kn, "to", _kn, x.Integral())
                x.SetDirectory(tf)
                x.Write()
            else:
                x = tf.Get(_kn)
                x.Sumw2()
                x1 = x.Integral()
                x.Add(tf0.Get(kn))
                x2 = x.Integral()
                print("added", kn, "to", _kn, x1, x2)
                x.SetDirectory(tf)
                x.Write("", ROOT.TObject.kOverwrite)

    #tf.Write()
    tf.Close()

    model = build_model_from_rootfile(
        filename,

        #This enables the Barlow-Beeston procedure
        # http://www.pp.rhul.ac.uk/~cowan/stat/mcml.pdf
        # http://atlas.physics.arizona.edu/~kjohns/teaching/phys586/s06/barlow.pdf
        include_mc_uncertainties = True,
        histogram_filter = hfilter,
        root_hname_to_convention = nameconv
    )
    #os.remove(filename)
    model.fill_histogram_zerobins()
    model.set_signal_processes(signal)

    for o in model.get_observables():
        for p in model.get_processes(o):
            if p == signal:
                continue
            try:
                add_normal_unc(model,
                    p,
                    mean=float(Config.get("priors", "%s_mean"%p)),
                    unc=float(Config.get("priors", "%s_sigma"%p))
                )
            except:
                print "fixing process ", o, p
    return model

def add_normal_unc(model, par, mean=1.0, unc=1.0):
    model.distribution.set_distribution(
        par, 'gauss', mean = mean,
        width=unc, range=[0.0, float("inf")]
    )
    for o in model.get_observables():
        for p in model.get_processes(o):
            if par != p:
                continue
            print "adding parameters for", o, p
            model.get_coeff(o,p).add_factor('id', parameter=par)

def build_model(infiles):
    model = None
    #infiles = glob("%s/*.root*" % indir)
    for inf in infiles:
        print "loading model from ",inf
        m = get_model(inf)
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
nbins = sum([model.get_range_nbins(o)[2] for o in model.get_observables()])
model_summary(model)

options = Options()
options.set("minimizer","strategy","robust")
#options.set("minimizer","strategy","minuit_vanilla")
options.set("global", "debug", "true")

#print "options=", options

result = mle(model, input = 'data', n=1, with_covariance=True, options=options, chi2=True, ks=True)
print "result=", result
fitresults = {}
values = {}
errors = {}
for process in result[signal]:
    if '__' not in process:
        fitresults[process] = result[signal][process][0]
        values[process] = fitresults[process][0]
        errors[process] = fitresults[process][1]

for p in ["qcd"]:
    if p not in values.keys():
        values[p] = 1.0
    if p not in errors.keys():
        errors[p] = 0.0

pars = sorted(model.get_parameters([signal]))
n = len(pars)

cov = result[signal]['__cov'][0]

corr = numpy.zeros((n, n), dtype=numpy.float32)

import os
import os.path
dn = os.path.dirname(outfile)
if not os.path.exists(dn):
    os.makedirs(dn)

print("writing covariance file")
covfi = ROOT.TFile(outfile+"_cov.root", "RECREATE")
covmat = ROOT.TH2D("covariance", "covariance", n, 0, n - 1, n, 0, n - 1)
covmat.SetDirectory(covfi)
for i in range(n):
   for j in range(n):
       corr[i][j] = cov[i][j] / (errors[pars[i]] * errors[pars[j]])
       covmat.SetBinContent(i, j, cov[i][j])
       covmat.SetBinError(i, j, 0.0)
       # if i==j:
       #     print("diag corr = ", corr[i][j])
covfi.Write()
covfi.Close()

of = open(outfile+"_cov.txt", "w")
of.write(str(corr[0][1]) + "\n")
of.write(str(corr[0][2]) + "\n")
of.write(str(corr[1][2]) + "\n")
of.close()

out = {
    "names": [p for p in pars],
    "means": [values[p] for p in pars],
    "errors": [errors[p] for p in pars],
    "cov": cov.tolist(),
    "corr": corr.tolist(),
    "chi2": result[signal]["__chi2"],
    "nbins": nbins
}
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
