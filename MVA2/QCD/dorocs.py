#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os.path
import mvalib.plot
import mvalib.utils
import plots.common.sample
import plots.common.cross_sections
import plots.common.plot_defs

from plots.common.cuts import Cuts
from plots.common.plot_defs import cutlist
cut_iso = {}
cut_iso['ele'] = str(cutlist['2j1t']*cutlist['presel_ele'])
cut_iso['mu'] = str(cutlist['2j1t']*cutlist['presel_mu'])
cut_test_antiiso = {}
cut_test_antiiso['ele'] = str(cutlist['2j1t']*cutlist['presel_ele']*Cuts.deltaR(0.3)*Cuts.antiiso('ele'))
cut_test_antiiso['mu'] = str(cutlist['2j1t']*cutlist['presel_mu']*Cuts.deltaR(0.3)*Cuts.antiiso('mu'))

signals = ['T_t_ToLeptons', 'Tbar_t_ToLeptons']
bgs = {
	'TTbar_inclusive': ['TTJets_MassiveBinDECAY'],
	'WJets_inclusive': ['WJets_inclusive'],
	'WJets': ['W1Jets_exclusive', 'W2Jets_exclusive', 'W3Jets_exclusive', 'W4Jets_exclusive'],
	'TTbar': ['TTJets_FullLept', 'TTJets_SemiLept'],
	'signal': ['T_t_ToLeptons', 'Tbar_t_ToLeptons'],
	'signal_inclusive': ['T_t', 'Tbar_t'],
	'diboson': ['WW', 'WZ', 'ZZ'],
	's_channel': ['T_s', 'Tbar_s'],
	'tW': ['T_tW', 'Tbar_tW'],
}
allbgs = bgs['WJets']+bgs['TTbar']+bgs['diboson']+bgs['s_channel']+bgs['tW']
qcd_bgs = {
	'mu':  ['SingleMu1','SingleMu2','SingleMu3'],
	'ele': ['SingleEle1', 'SingleEle2']
}

cutvar = {'mu': 'mt_mu', 'ele': 'met'}

class MCSample(plots.common.sample.Sample):
	def __init__(self, ch, s):
		self._ch = ch
		plots.common.sample.Sample.__init__(self, s, os.path.join('qcd_filled', ch, 'mc/iso/nominal/Jul15', s+'.root'))

		elist_name = 'elist_{0}'.format(s)
		self.tree.Draw('>>{0}'.format(elist_name), cut_iso[ch], 'entrylist')
		elist=ROOT.gDirectory.Get(elist_name);
		self.tree.SetEntryList(elist)

	def lumiScaleFactor(self):
		lumi = plots.common.cross_sections.lumi_iso[self._ch]
		return plots.common.sample.Sample.lumiScaleFactor(self, lumi)


class QCDSample(plots.common.sample.Sample):
	def __init__(self, ch, s):
		self._ch = ch
		plots.common.sample.Sample.__init__(self, s, os.path.join('qcd_filled', ch, 'data/antiiso/Jul15', s+'.root'))

		elist_name = 'elist_{0}'.format(s)
		self.tree.Draw('>>{0}'.format(elist_name), cut_test_antiiso[ch], 'entrylist')
		elist=ROOT.gDirectory.Get(elist_name);
		self.tree.SetEntryList(elist)

	def lumiScaleFactor(self):
		return 1.0


def fn_openTree(ch, SampleClass):
	return lambda s: SampleClass(ch, s)

for ch in ['ele', 'mu']:
	#variables = ['mva_anti_QCD_MVA', cutvar[ch], plots.common.plot_defs.mva_var[ch]]
	variables = ['mva_anti_QCD_MVA', cutvar[ch]]
	smpls_sig = map(fn_openTree(ch, MCSample), signals)
	for bg,bgss in bgs.items():
		smpls_bgs = map(fn_openTree(ch, MCSample), bgss)
		mvalib.plot.plot_ROC(smpls_sig, smpls_bgs, variables, name='{0}_{1}'.format(ch,bg), title='ROC: antiQCD MVA vs {1} (channel: {0})'.format(ch,bg), nbins=500)
	smpls_qcd = map(fn_openTree(ch, QCDSample), qcd_bgs[ch])
	mvalib.plot.plot_ROC(smpls_sig, smpls_qcd, variables, name='{0}_QCD'.format(ch), title='ROC: antiQCD MVA vs QCD (channel: {0})'.format(ch), nbins=500)

	smpls_all = map(fn_openTree(ch, MCSample), allbgs) + map(fn_openTree(ch, QCDSample), qcd_bgs[ch])
	mvalib.plot.plot_ROC(smpls_sig, smpls_all, variables, name='{0}_all'.format(ch), title='ROC: antiQCD MVA vs all (channel: {0})'.format(ch), nbins=500)
