#!/usr/bin/env python
"""
Uses the unfolding histograms to make a final plot with the systematic band.
"""
from rootpy.io import File
from os.path import join
from plots.common.utils import NestedDict
from SingleTopPolarization.Analysis.systematics import total_syst
from plots.common.hist_plots import plot_hists, plot_hists_dict, plot_data_mc_ratio
from plots.common.stack_plot import plot_hists_stacked
from plots.common.odict import OrderedDict
from plots.common.sample_style import Styling
from plots.common.legend import legend
from plots.common.utils import lumi_textbox
from plots.load_histos2 import load_theta_format, SystematicHistCollection
from plots.common.utils import reorder, PhysicsProcess
from SingleTopPolarization.Analysis import sample_types


import numpy, re, math, logging, copy

logger = logging.getLogger(__name__)
import rootpy
rootpy.log.basic_config_colorized()
logger.setLevel(logging.INFO)

import ROOT
ROOT.gROOT.SetBatch(True)

#Define the styles for the merged histograms
styles = {
    'tchan': 'T_t',
    'ttjets': 'TTJets_FullLept',
    'wjets': 'WJets_inclusive',
    'diboson': 'WW',
    'twchan': 'T_tW',
    'schan': 'T_s',
    'qcd': 'QCD'
}

def rescale_to_fit(sample_name, hist, fitpars, ignore_missing=True):
    """
    Rescales the histogram from a sample by the corresponding scale factors.
    Raises a KeyError when there was no match.

    sample_name - the name of the sample, corresponding to the patterns in fitpars
    hist - the Hist to be scaled
    fitpars - a list with tuple contents
        [
            ([patA1, patA2, ...], sfA, errA),
            ([patB1, patB2, ...], sfB, errB),
        ]

    returns - nothing
    """
    for patterns, sf, err in fitpars:
        for pat in patterns:
            if re.match(pat, sample_name):
                logger.debug("Rescaling sample %s to match rule '%s', sf=%.2f" % (sample_name, pat, sf))
                hist.Scale(sf)
                #We take the first match
                return
    #If we loop through and get here, there was no match
    if not ignore_missing:
        raise KeyError("Couldn't match sample %s to fit parameters!" % sample_name)


def load_fit_results(fn):
    """
    Opens the fit results file and returns the per-sample scale factors.

    Args:
        fn: the file name with the fit results

    Returns:
        A dictionary with (sample_name, scale_factor) elements.
    """
    fi = open(fn)
    rates = {}
    for line in fi.readlines():
        line = line.strip()
        spl = line.split(",")
        spl = map(lambda x: x.strip(), spl)
        assert len(spl)==4

        spl = tuple(spl)
        typ, sample, sf, err = spl
        if not typ=="rate":
            continue
        rates[sample] = float(sf)
    return rates

class PlotDef:
    from plots.vars import varnames

    defaults = dict(
        log=False,
        fit_sf=None,
        systematics=[],
        systematics_shapeonly=False,
        systematics_symmetric=True,
        x_label=r"%(var_name)s %(x_units)s",
        x_units='',
        y_units='',
        lumibox_format='%(channel)s channel%(lb_comments)s',
        legend_pos='top-left',
        lumi_pos='top-right',
        normalize=False,

        #The scale factor for the N(data, anti-iso)/N(QCD, iso) yields,
        process_scale_factor = []
    )

    def __init__(self, **kwargs):

        for k, v in self.defaults.items():
            setattr(self, k, v)

        #Set any keyword arguments as attributes to self
        for k, v in kwargs.items():
            setattr(self, k, v)

        #The default variable pretty name is taken externally
        if not hasattr(self, "var_name"):
            try:
                self.var_name = self.varnames[self.var]
            except KeyError:
                self.var_name = self.var
        #The systematic inclusion list is a list of regex patterns to include
        if isinstance(self.systematics, basestring):
            self.systematics = [self.systematics]

    def get_x_label(self):
        return self.x_label % self.__dict__

    def get_lumibox_comments(self, **kwargs):
        kwargs.update(**self.__dict__)
        return self.lumibox_format % kwargs

    def __repr__(self):
        return self.__dict__

    def __str__(self):
        return str(self.__repr__())

    def update(self, **kwargs):
        self.__dict__.update(**kwargs)

    def copy(self, **kwargs):
        newd = copy.deepcopy(self.__dict__)
        newd.update(**kwargs)
        new = PlotDef(**newd)

        return new

def data_mc_plot(pd):
    hists = load_theta_format(pd.infile, styles)

    for (variable, sample, systtype, systdir), hist in hists.items_flat():

        #Scale all MC samples except QCD to the luminosity
        if sample_types.is_mc(sample) and not sample=="qcd":
            hist.Scale(pd.lumi)
        if hasattr(pd, "rebin"):
            hist.Rebin(pd.rebin)
        if sample=="qcd" and hasattr(pd, "qcd_yield"):
            hist.Scale(pd.qcd_yield / hist.Integral())

        rescale_to_fit(sample, hist, pd.process_scale_factor)
        hist.SetTitle(sample)
        hist.SetName(sample)


    #Assuming we only have 1 variable
    hists = hists[pd.var]

    hists_nominal = hists.pop("nominal")[None]
    hists_nom_data = hists_nominal.pop('data')
    hists_nom_mc = hists_nominal.values()
    hists_syst = hists

    hists_nom_data.SetTitle('data')

    #A list of all the systematic up, down variation templates as 2-tuples
    all_systs = [
    ]

    all_systs = hists_syst.keys()
    systs_to_consider = []

    #See which systematics where asked to switch on
    for syst in all_systs:
        for sm in pd.systematics:
            if re.match(sm, syst):
                systs_to_consider.append(syst)

    #The total nominal MC histogram
    nom = sum(hists_nom_mc)

    if pd.normalize:
        ratio = hists_nom_data.Integral() / nom.Integral() 
        hists_nom_data.Scale(1.0/ratio)

    #Get all the variated up/down total templates
    #A list with all the up/down total templates
    all_systs = []

    sumsqs = []
    logger.info("Considering systematics %s" % str(systs_to_consider))
    for syst in systs_to_consider:

        #A list with the up/down variated template for a particular systematic
        totupdown = []

        sumsq = []
        for systdir in ["up", "down"]:

            #Get all the templates corresponding to a systematic scenario and a variation
            _hists = hists_syst[syst][systdir]


            for k, h in _hists.items():

                """
                Consider only the shape variation of the systematic,
                hence the variated template is normalized to the corresponding
                unvariated template.
                """
                if pd.systematics_shapeonly:
                    if h.Integral()>0:
                        h.Scale(hists_nominal[k].Integral() / h.Integral())

            #For the missing variated templates, use the nominal ones, but warn the user
            present = set(_hists.keys())
            all_mc = set(hists_nominal.keys())
            missing = list(all_mc.difference(present))
            for m in missing:
                logger.warning("Missing systematic template for %s:%s" % (syst, systdir))

            #Calculate the total variated template
            tot = sum(_hists.values()) + sum([hists_nominal[m] for m in missing])
            totupdown.append(tot)

            sumsq.append(
                math.sqrt(numpy.sum(numpy.power(numpy.array(list(nom.y())) - numpy.array(list(tot.y())), 2)))
            )
        logger.debug("Systematic %s: sumsq=%.2Eu, %.2Ed" % (syst, sumsq[0], sumsq[1]))
        sumsqs.append((syst, max(sumsq)))
        all_systs.append(
            (syst, tuple(totupdown))
        )

    sumsqs = sorted(sumsqs, key=lambda x: x[1], reverse=True)
    for syst, sumsq in sumsqs[0:7]:
        logger.info("Systematic %s, %.4f" % (syst, sumsq))

    #Calculate the total up/down variated templates by summing in quadrature
    syst_stat_up, syst_stat_down = total_syst(
        nom, all_systs,
    )

    stacks_d = OrderedDict()
    stacks_d['mc'] = reorder(hists_nominal, PhysicsProcess.desired_plot_order_mc)
    stacks_d['data'] = [hists_nom_data]

    #Systematic style
    for s in [syst_stat_up, syst_stat_down]:
        s.SetFillStyle(0)
        s.SetLineWidth(2)
        s.SetMarkerSize(0)
        s.SetLineColor(ROOT.kGray+2)
        s.SetLineStyle('dashed')
        s.SetTitle("stat. + syst.")

    c = ROOT.TCanvas()
    p1 = ROOT.TPad("p1", "p1", 0, 0.3, 1, 1)
    p1.Draw()
    p1.SetTicks(1, 1);
    p1.SetGrid();
    p1.SetFillStyle(0);
    p1.cd()

    stacks = plot_hists_stacked(p1, stacks_d, x_label=pd.get_x_label(), max_bin_mult=1.5 if not pd.log else 100)
    p1.SetLogy(pd.log)

    syst_stat_up.Draw("SAME hist")
    syst_stat_down.Draw("SAME hist")

    ratio_pad, hratio = plot_data_mc_ratio(
        c, hists_nom_data,
        nom, syst_hists=(syst_stat_down, syst_stat_up), min_max=(-1, 1)
    )

    p1.cd()
    leg = legend(
        stacks_d['data'] +
        list(reversed(stacks_d['mc'])) +
        [syst_stat_up],
        legend_pos=pd.legend_pos
    )
    lb = lumi_textbox(pd.lumi,
        line2=pd.get_lumibox_comments(channel=pd.channel_pretty),
        pos=pd.lumi_pos
    )
    c.children = [p1, ratio_pad, stacks, leg, lb]

    tot = 0
    for k, v in hists_nominal.items():
        print k, v.Integral(), v.GetEntries()
        tot += v.Integral()
    tot_data = hists_nom_data.Integral()
    print "MC: %.2f Data: %.2f" % (tot, tot_data)
    #import pdb; pdb.set_trace()
    return c
if __name__=="__main__":
    from plots.common.tdrstyle import tdrstyle
    tdrstyle()

    from plots.fit_scale_factors import fitpars_process
    from plots.common.cross_sections import lumis

    channels_pretty = {
        "mu": "Muon",
        "ele": "Electron",
    }

    sfs = {
        "mu": [
            (["tchan"], 1.031894, -1),
            (["ttjets", "twchan", "schan"], 0.914750, -1),
            (["qcd"], 0.914750 * 7, -1),
            (["wjets", "diboson", "dyjets"], 1.604641, -1),
        ],
        "ele": [
            (["tchan"], 0.956595, -1),
            (["ttjets", "twchan", "schan"], 0.982722, -1),
            (["qcd"], 0.982722 * 0.0, -1),
            (["wjets", "diboson", "dyjets"], 1.382914, -1),
        ]
    }

    # qcd_yields = {
    #     "mu": 700,
    #     "ele": 133.020387,
    # }

    for channel in ["mu", "ele"]:
        for var in ["top_mass_sr", "abs_eta_lj_4", "mtw_50_150", "cos_theta"]:
            h = PlotDef(
                infile="out/hists/hists_merged__%s_%s.root" % (var, channel),
                lumi=lumis["Aug4_0eb863_full"]["iso"][channel],
                var=var,
                channel_pretty=channels_pretty[channel],
                leg_pos='top-right',
                systematics='.*',
                log=False,
                systematics_shapeonly=True,
                save_name='2j1t_mva__%s__all_syst_%s.png' % (var, channel),
                #normalize=False,
                lb_comments=', all syst.',
                process_scale_factor = sfs[channel],
                #qcd_yield=qcd_yields[channel],
                rebin=2
            )
            # h1 = h.copy(
            #     systematics='en|res',
            #     save_name='2j1t_mva__%s__jes_jer_%s.png' % (var, channel),
            #     lb_comments=', JES+JER',
            #     process_scale_factor = sfs[channel]
            # )

            for p in [h]:
                c = data_mc_plot(p)
                c.SaveAs(p.save_name)
                p.res = c
                c.Close()
