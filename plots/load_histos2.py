import re, glob, sys, os, copy
from collections import deque
from rootpy.io import File
from rootpy.plotting import Hist
import itertools
from plots.common.utils import NestedDict, PatternDict
import ROOT
import logging

logger = logging.getLogger("load_histos2")
logger.setLevel(logging.INFO)

qcd_yield_variations = (2.0, 0.5)
skipped_systs = ["wjets_matching", "wjets_scale", "sig_gen", "sig_anom"]

def load_file(fnames, pats):
    res = {}
    ret = {}
    for patn, pat in pats.items():
        res[patn] = re.compile(pat)
        ret[patn] = PatternDict()

    n = 0
    for fn in fnames:
        fi = File(fn)
        ROOT.gROOT.cd()
        logger.debug("Processing file %s" % fn)
        for root, dirs, items in fi.walk():
            for it in items:
                # if n%10==0:
                #     sys.stdout.write(".")
                #     sys.stdout.flush()
                if n%25000 == 0:
                    logger.info("%d, %s, %s" % (
                            n,
                            str([(k, len(ret[k].keys())) for k in ret.keys()]),
                            fi.GetPath()
                        )
                    )
                    #logger.debug(root)
                for patn, pat in res.items():
                    if pat.match(root):
                        ret[patn][root] = fi.Get(
                            "/".join(
                                [root, it]
                            )
                        ).Clone()
                n += 1
        fi.Close()
    logger.info("Matched %s histograms" % (str([(k, len(ret[k].keys())) for k in ret.keys()])))
    return ret

def _load_pickle(x):
    import cPickle as pickle
    import gzip
    ret = []
    fi = gzip.GzipFile(x, 'rb')
    while True:
        try:
            item = pickle.load(fi)
            ret.append(item)
        except EOFError:
            break
    fi.close()
    return ret

def make_hist(item):
    item.__class__ = Hist
    item._post_init()

def load_pickle(fnames):
    ret = PatternDict()

    from multiprocessing import Pool
    p = Pool(20)

    logger.info("Loading pickles")
    rets = p.map(_load_pickle, fnames)
    logger.info("Combining")
    n = 0
    for r in rets:
        for item in r:
            #if isinstance(item, ROOT.TH1F):
            ret[item.GetName()] = item
        n += 1
    logger.info("Done loading templates from pickles: %d" % len(ret))
    return ret

from SingleTopPolarization.Analysis import sample_types
def get_syst_from_sample_name(sn):
    """
    Gets the sample base name (process name), systematic
    scenario name and variation direction from the name
    of a systematically variated (at production) sample.

    For example:
        'TTJets_FullLept_scaledown' =>
            ('TTJets_FullLept', 'ttbar_scale', 'down')

        'WJetsToLNu_matchingup' =>
            ('WJetsToLNu', 'wjets_matching', 'down')


        'T_t_ToLeptons_mass178_5' =>
            ('T_t_ToLeptons', 'mass', 'up')

    Since there is no standard naming scheme for the
    systematic samples (yet), this mapping must be hardcoded
    at the moment (within reason)

    Args:
        sn: a string with the sample name (the filename with
            the .root suffix removed)

    Returns:
        A 3-tuple with (process_name, systematic_name, systematic_dir)
    """

    si = sample_types.sample_infos[sn]

    #Check if the sample is MC and of the SYST type
    if si.has("mc") and si.has("syst"):

        #All of these can be handled in the same way
        for k in ["mass", ".*scale", ".*matching", "sig_anom", "sig_gen"]:
            m = si.has(k + "__.*", ret=True)
            if len(m)==1:
                m = m[0]
                syst, systdir = m.split("__")
                return (si.subprocess, syst, systdir)

    #If you called this method and got here: problems
    raise Exception("Unhandled systematic: %s" % sn)

def get_updown(syst):
    syst = syst.lower()

    if syst=="unweighted" or syst == "nominal":
        return syst, None
    idx = None
    for d in ["up", "down"]:
        if d in syst:
            idx = syst.index(d)
            break
    if not idx:
        raise ValueError("Unrecognized syst: %s" % syst)

    systtype = syst[0:idx]
    systtype = systtype.strip("_")#.strip("weight__")
    systdir = d
    return systtype, systdir

def get_all_systs(syst_scenarios):
    allsysts = []
    for sampn, systd in syst_scenarios.items():
        allsysts += systd.keys()
    allsysts = list(sorted(list(set(allsysts))))
    return allsysts

def split_name(name):
    spl = name.split("__")
    var = spl[0]
    sample = spl[1]

    systtype = "nominal"
    systdir = None

    if len(spl)>2:
        systtype = spl[2]
    if len(spl)>3:
        systdir = spl[3]

    return {
        "var":var, "sample":sample,
        "type":systtype, "dir":systdir
    }

def syst_overview(hists):
    from tabulate import tabulate
    diffs = NestedDict()
    table = []
    for k1, v1 in hists:
        spl1 = hname_decode(k1)
        if spl1["type"]=="nominal":
            for k2, v2 in hists:
                spl2 = hname_decode(k2)
                if not spl2["sample"]==spl1["sample"]:
                    continue
                h = v1-v2
                diffs[spl2["sample"]][spl2["type"]][spl2["dir"]] = h
                table.append([
                    "N" if sum(v2.errors())<0.00001 else "Y",
                    "N" if h.Integral()<0.00001 and  h.GetRMS()<0.00001 else "Y",
                    spl1["sample"], spl2["type"], spl2["dir"],
                    "%.2E" % h.Integral(),
                    "%.2E" % h.GetMean(),
                    "%.2E" % h.GetRMS(),
                    "%.2E" % sum(v2.errors()),
                ])
    table.sort(key=lambda x: (x[2], x[3]))
    table = [["available", "non-zero", "sample", "syst", "dir", "int(d)", "mean(d)", "RMS(d)", "sumerr(e)"]] + table
    print tabulate(table, headers="firstrow")

def hname_encode(varname, sampn, systname=None, systdir=None):
    l = [varname, sampn]
    if systname:
        l.append(systname)
    if systdir:
        l.append(systdir)
    return "__".join(l)

def hname_decode(hname):
    spl = hname.split("__")
    var = spl[0]
    sample = spl[1]

    systtype = "nominal"
    systdir = None

    if len(spl)>2:
        systtype = spl[2]
    if len(spl)>3:
        systdir = spl[3]

    return {
        "var":var, "sample":sample,
        "type":systtype, "dir":systdir
    }

def set_missing_hist(hist):
    hist.SetName(hist.GetName()+"__MISSING")
    #for i in range(hist.GetNbinsX()):
    #    hist.SetBinError(i, 0)

def load_theta_format(inf, styles=None):
    from plots.common.sample_style import Styling
    if not styles:
        styles = {}

    hists = SystematicHistCollection()
    fi = File(inf)
    ROOT.gROOT.cd()
    #rate_sfs = load_fit_results("final_fit/results/%s.txt" % fit_results[channel])
    for root, dirs, items in fi.walk():
        for it in items:

            hn = hname_decode(it)
            variable, sample, syst, systdir = hn["var"], hn["sample"], hn["type"], hn["dir"]

            k = os.path.join(root, it)
            try:
                it = fi.Get(k).Clone()
            except:
                raise Exception("Could not copy object %s" % k)
            #Skip anything not a histogram
            if not isinstance(it, ROOT.TH1F):
                continue

            if sample == "DATA":
                sample = sample.lower()

            if sample.lower() != "data":
                sty = styles.get(sample.lower(), sample)
                try:
                    Styling.mc_style(it, sty)
                except:
                    logger.debug("Could not style histogram from sample: %s" % sample)
            else:
                Styling.data_style(it)
            hists[variable][syst][systdir][sample]= it

    #hists = hists.as_dict()
    fi.Close()

    return hists

class SystematicHistCollection(NestedDict):

    def items_flat(self):
        for variable, h1 in super(SystematicHistCollection, self).items():
            for syst, h2 in h1.items():
                for systdir, h3 in h2.items():
                    for sample, h4 in h3.items():
                        yield ((variable, sample, syst, systdir), h4)

class HistDef:
    defaults = dict(
    )

    def __init__(self, **kwargs):

        for k, v in self.defaults.items():
            setattr(self, k, v)

        #Set any keyword arguments as attributes to self
        for k, v in kwargs.items():
            setattr(self, k, v)

    def update(self, **kwargs):
        self.__dict__.update(**kwargs)

    def copy(self, **kwargs):
        newd = copy.deepcopy(self.__dict__)
        newd.update(**kwargs)
        new = HistDef(**newd)
        return new

    def get_outfile_merged(self):
        return self.outfile_merged % self.__dict__

    def get_outfile_unmerged(self):
        return self.outfile_unmerged % self.__dict__

    def get_cutstr(self):
        return self.cutstr % self.__dict__

    def get_cutstr_antiiso(self, loose=False):
        if loose:
            return self.cutstr_antiiso_loose % self.__dict__
        else:
            return self.cutstr_antiiso % self.__dict__

def make_patterns(conf):
    cutstr = conf.get_cutstr()
    base = conf.basepath

    pat_mc_varsamp = ""
    pat_mc_varsamp += base
    pat_mc_varsamp += "mc_syst/iso/(.*)/Jul15/(.*)/"
    pat_mc_varsamp += conf.get_cutstr()
    pat_mc_varsamp += "(weight__nominal__%(channel)s)/%(varname)s$"

    pat_mc_varproc = ""
    pat_mc_varproc += base
    pat_mc_varproc += "mc/iso/(.*)/Jul15/(.*)/"
    pat_mc_varproc += conf.get_cutstr()
    pat_mc_varproc += "(weight__nominal__%(channel)s)/%(varname)s$"

    pat_data = ""
    pat_data += base
    pat_data += "(data)/iso/.*/(Single.*)/"
    pat_data += conf.get_cutstr()
    pat_data += "(weight__unweighted.*)/%(varname)s$"

    pat_mc_nom = ""
    pat_mc_nom += base
    pat_mc_nom += "mc/iso/(nominal)/Jul15/(.*)/"
    pat_mc_nom += conf.get_cutstr()
    pat_mc_nom += "(weight__.*__%(channel)s)/%(varname)s$"

    #pat_data_antiiso_loose = ""
    #pat_data_antiiso_loose += base
    #pat_data_antiiso_loose += "data/antiiso/.*/(.*)/"
    #pat_data_antiiso_loose += conf.get_cutstr_antiiso(loose=True)
    #pat_data_antiiso_loose += "(weight__unweighted.*)/%(varname)s$"

    pat_data_antiiso = ""
    pat_data_antiiso += base
    pat_data_antiiso += "data/antiiso/.*/(.*)/"
    pat_data_antiiso += conf.get_cutstr_antiiso()
    pat_data_antiiso += "(weight__unweighted.*)/%(varname)s$"


    pat_mc_varsamp = pat_mc_varsamp % conf.__dict__
    pat_mc_varproc = pat_mc_varproc % conf.__dict__
    pat_mc_nom = pat_mc_nom % conf.__dict__
    pat_data = pat_data % conf.__dict__
    pat_data_antiiso = pat_data_antiiso % conf.__dict__

    pats = {
            "mc_varsamp": pat_mc_varsamp,
            "mc_varproc": pat_mc_varproc,
            "mc_nom": pat_mc_nom,
            "data": pat_data,
    #        "data_antiiso_loose": pat_data_antiiso_loose,
            "data_antiiso": pat_data_antiiso,
    }

    return pats

class MatchingException(Exception):
    pass
def combine_templates(templates, patterns, conf):
    """
    Args:
    """

    hists = {}
    hsources = []
    for k in ["data", "mc_nom", "mc_varsamp", "mc_varproc"]:
        items = templates[patterns[k]]
        if len(items)==0:
            for _k, _v in dict.items(templates):
                print _k, _v
            raise MatchingException("Nothing matched to %s:%s" % (k, patterns[k]))
        hsources += items

    if len(hsources)==0:
        raise ValueError("No histograms matched")

    hqcd = NestedDict()
    hqcd["nominal"][None] = []
    for syst in ["yield", "iso"]:
        for sdir in ["up", "down"]:
            hqcd[syst][sdir] = []
    templates_qcd = templates[patterns["data_antiiso"]]

    if len(templates_qcd)==0:
        raise MatchingException("Nothing matched to %s:%s" % ("data_antiiso", patterns["data_antiiso"]))

    for keys, hist in templates[patterns["data_antiiso"]]:
        if keys[1].startswith("antiiso"):
            #We have isolation variations
            isodir = keys[1].split("_")[1]
            if isodir=="nominal":
                hqcd["nominal"][None].append(hist)
                hup = hist.Clone()
                hdown = hist.Clone()
                hup.Scale(qcd_yield_variations[0])
                hdown.Scale(qcd_yield_variations[1])
                hqcd["yield"]["up"].append(hup)
                hqcd["yield"]["down"].append(hdown)

            elif isodir in ["up", "down"]:
                hqcd["iso"][isodir].append(hist)
            else:
                raise ValueError("Undefined isolation variation direction: %s" % isodir)

        #We only have the nominal QCD shape
        elif keys[1]=="weight__unweighted":
            hqcd["nominal"][None].append(hist)
            hup = hist.Clone()
            hdown = hist.Clone()
            hup.Scale(qcd_yield_variations[0])
            hdown.Scale(qcd_yield_variations[1])
            hqcd["yield"]["up"].append(hup)
            hqcd["yield"]["down"].append(hdown)

            #Placeholders for the isolation variation
            for isodir in ["up", "down"]:
                h = hist.Clone()
                hqcd["iso"][isodir].append(h)
        else:
            raise Exception("Couldn't parse the QCD pattern: %s" % str(keys))

    def map_leaves(di, f, equate=True):
        for k, v in di.items():
            if isinstance(v, dict):
                map_leaves(v, f)
            else:
                if equate:
                    di[k] = f(v)
                else:
                    f(v)
        return di

    #Sum the anti-iso data subsamples
    map_leaves(hqcd, lambda li: reduce(lambda x,y: x+y, li))

    #Normalize the isolation variations to the nominal
    map_leaves(hqcd["iso"],
        lambda hi:
            hi.Scale(hqcd["nominal"][None].Integral() / hi.Integral()) if hi.Integral()>0 else 0,
        equate=False
    )

    #Add the variated data-driven QCD templates
    hsources += [
        (("data", "qcd", "weight__unweighted"), hqcd["nominal"][None]),
        (("data", "qcd", "weight__qcd_yield_up"), hqcd["yield"]["up"]),
        (("data", "qcd", "weight__qcd_yield_down"), hqcd["yield"]["down"]),
        (("data", "qcd", "weight__qcd_iso_up"), hqcd["iso"]["up"]),
        (("data", "qcd", "weight__qcd_iso_down"), hqcd["iso"]["down"]),
    ]

        #f = open('temp.pickle','wb')
        #pickle.dump(hsources, f)
        #f.close()

    #load the histos from the temporary pickle
    #f = open('temp.pickle','rb')
    #hsources = pickle.load(f)

    syst_scenarios = NestedDict()
    for (sample_var, sample, weight_var), hist in hsources:
        make_hist(hist)
        # if "__ele" in weight_var:
        #     continue

        if ".root" in sample:
            sample = sample[:sample.index(".root")]

        if "__" in weight_var:
            spl = weight_var.split("__")
            wn = spl[1]
        else:
            wn = weight_var
        sample_var = sample_var.lower()
        wtype = None
        wdir = None
        stype = None
        sdir = None

        syst = None

        # if sample=="qcd":
        #     pdb.set_trace()

        #Nominal weight, look for variated samples
        if wn=="nominal":
            syst = sample_var
        elif wn=="unweighted":
            syst="unweighted"
        else:
            #Variated weight, use only nominal sample or data in case of data-driven shapes
            if not (sample_var=="nominal" or sample_var=="data"):
                continue
            syst = wn


        if wn=="nominal" and sample_var=="nominal":
            syst_scenarios[sample]["nominal"][None] = hist

        #A systematic scenario which has a separate systematic sample
        elif sample_var == "syst":
            r = get_syst_from_sample_name(sample)
            if not r:
                continue
            sample, systname, d = r
            #sample = map_syst_sample_to_nominal(sample)
            syst_scenarios[sample][systname][d] = hist

        else:
            systname, d = get_updown(syst)
            syst_scenarios[sample][systname][d] = hist

    ######################################
    ### Save systematics, fill missing ###
    ######################################

    #T_t_ToLeptons mass_up is missing, take the mass down and flip the difference with the nominal
    mnomt = syst_scenarios["T_t_ToLeptons"]["nominal"][None].Clone()
    mdownt = syst_scenarios["T_t_ToLeptons"]["mass"]["down"].Clone()
    mupt = (mnomt+mnomt-mdownt)
    syst_scenarios["T_t_ToLeptons"]["mass"]["up"] = mupt


    #TTbar variations are provided for the inclusive only, fill them for the exclusive
    nom_ttbar = syst_scenarios["TTJets_FullLept"]["nominal"][None] + syst_scenarios["TTJets_SemiLept"]["nominal"][None]
    for syst in ["mass", "ttbar_scale"]:
        for sample in ["TTJets_FullLept", "TTJets_SemiLept"]:
            for sd in ["up", "down"]:
                syst_scenarios[sample][syst][sd] = syst_scenarios[sample]["nominal"][None] * syst_scenarios["TTJets"][syst][sd] / nom_ttbar

    syst_scenarios.pop("TTJets")

    syst_scenarios = syst_scenarios.as_dict()

    #Create the output file
    of = ROOT.TFile(conf.get_outfile_unmerged() , "RECREATE")
    of.cd()

    #Get the list of all possible systematic scenarios that we have available

    allsyts = get_all_systs(syst_scenarios)

    for sampn, h1 in syst_scenarios.items():

        #Consider all the possible systematic scenarios
        for systname in allsyts:

            #If we have it available, fine, use it
            if systname in h1.keys():
                h2 = h1[systname]

            #If not, in case of MC and a non-trivial variation
            elif not sampn.startswith("Single") and systname not in ["unweighted", "nominal"]:

                #Try to get the unvariated template as a placeholder
                h = h1.get("nominal", None)
                if not h:
                    h = h1.get("unweighted", None)
                if not h:
                    raise Exception("Could not get the nominal template for %s:%s" % (sampn, systname))

                #Our convention is that even the unvariated template is a dict with a single
                #key for the direction of variation, which is 'None'
                h = h[None]

                #Add placeholder templates
                for systdir in ["up", "down"]:
                    h = h.Clone(hname_encode(conf.varname, sampn, systname, systdir))
                    print "Missing template for %s:%s" % (sampn, systname)
                    set_missing_hist(h)

                    #Save to file
                    h.SetDirectory(of)
                    h.Write()
                continue
            else:
                continue
            for systdir, h in h2.items():
                if systdir==None and systname=="nominal" or not sample_types.is_mc(sampn):
                    h = h.Clone(hname_encode(conf.varname, sampn))
                elif systdir==None and systname=="unweighted":
                    h = h.Clone(hname_encode(conf.varname, sampn, "unweighted"))
                else:
                    h = h.Clone(hname_encode(conf.varname, sampn, systname, systdir))
                h.SetDirectory(of)
                h.Write()
    nkeys = len(of.GetListOfKeys())
    logger.info("Saved %d histograms to file %s" % (nkeys, of.GetPath()))
    of.Close()

    ########################
    ### Load systematics ###
    ########################
    of = File(conf.get_outfile_unmerged())
    hists = dict()
    ROOT.gROOT.cd()
    for k in of.GetListOfKeys():
        hists[k.GetName()] = of.Get(k.GetName()).Clone()
        #hists[k.GetName()].Rebin(2)
    logger.info("Loaded %d histograms from file %s" % (len(hists), of.GetPath()))
    of.Close()

    ########################
    ###      Merge       ###
    ########################
    from plots.common.utils import merge_hists, PhysicsProcess
    merge_cmds = PhysicsProcess.get_merge_dict(
        PhysicsProcess.get_proc_dict(conf.channel)
    )
    hsysts = NestedDict()
    for k, v in hists.items():
        spl = split_name(k)
        hsysts[spl["type"]][spl["dir"]][spl["sample"]] = v
    hsysts = hsysts.as_dict()
    of = ROOT.TFile(conf.get_outfile_merged(), "RECREATE")
    of.cd()

    for syst, h1 in hsysts.items():
        if syst in skipped_systs:
            continue
        for sdir, h2 in h1.items():
            hmc = merge_hists(h2, merge_cmds)
            for hn, h in hmc.items():
                if syst=="nominal" or syst=="unweighted":
                    h.SetName("__".join([spl["var"], hn]))
                else:
                    h.SetName("__".join([spl["var"], hn, syst, sdir]))
                h.SetDirectory(of)
                h.Write()
    nkeys = len(of.GetListOfKeys())
    logger.info("Saved %d histograms to file %s" % (nkeys, of.GetPath()))
    of.Close()

    hists = load_theta_format(conf.get_outfile_merged())
    processes = []
    systs = []
    for (variable, sample, syst, systdir), v in hists.items_flat():
        processes.append(sample)
        systs.append(syst)
    processes = set(processes)
    systs = set(systs)
    logger.info("Processes: %s" % processes)
    if not processes == set(['diboson', 'schan', 'tWchan', 'TTJets', 'tchan', 'WJets', 'qcd', 'DYJets', 'data']):
        raise Exception("Combined file did not contain the necessary processes: %s" % str(processes))
    logger.info("Systematic scenarios: %s" % systs)


if __name__=="__main__":
    import sys
    inf = sys.argv[1] + '/hists-*.pickle'

    templates = load_pickle(glob.glob(inf))

    for channel in ["mu", "ele"]:
        for cut in ["baseline", "mva_loose", "cutbased_final"]:
            fpat_unmerged = 'out/hists/hists__2j1t_' + cut + '__%(varname)s_%(channel)s.root'
            fpat_merged = 'out/hists/hists_merged__2j1t_' + cut + '__%(varname)s_%(channel)s.root'

            cutstr = '%(channel)s_2j1t_' + cut + '/'
            cos_theta = HistDef(
                varname='cos_theta',
                channel=channel,
                basepath='.*/%(channel)s/',
                cutstr=cutstr,
                cutstr_antiiso='%(channel)s_2j1t_baseline/(antiiso_.*)/',
                outfile_unmerged=fpat_unmerged,
                outfile_merged=fpat_merged
            )

            mtw = cos_theta.copy(
                varname='mtw_50_150',
            )

            abs_eta_lj = cos_theta.copy(
                varname='abs_eta_lj',
            )

            top_mass_sr = cos_theta.copy(
                varname='top_mass_sr',
            )


           # for var in [top_mass_sr, cos_theta, abs_eta_lj, mtw]:
           #     patterns = make_patterns(var)
           #     combine_templates(templates, patterns, var)

        bdt = cos_theta.copy(
            varname='bdt_discr',
            channel=channel,
            #For the BDT plot we don't want to apply the MVA cut
            cutstr='%(channel)s_2j1t_baseline/',
            cutstr_antiiso='%(channel)s_2j1t_baseline/(antiiso_.*)/',
            outfile_unmerged = 'out/hists/hists__2j1t_baseline__%(varname)s_%(channel)s.root',
            outfile_merged = 'out/hists/hists_merged__2j1t_baseline__%(varname)s_%(channel)s.root'
        )
        met = cos_theta.copy(
            varname='met',
            channel=channel,
            #To show the MET distribution, don't apply the MET cut
            cutstr='%(channel)s_2j1t_nomet/',
            cutstr_antiiso='%(channel)s_2j1t_nomet/(antiiso_.*)/',
            outfile_unmerged = 'out/hists/hists__2j1t_baseline_nomet__%(varname)s_%(channel)s.root',
            outfile_merged = 'out/hists/hists_merged__2j1t_baseline_nomet__%(varname)s_%(channel)s.root'
        )
        for v in [bdt, met]:
            patterns = make_patterns(v)
            combine_templates(templates, patterns, v)
