import ROOT
import os.path
from plots.common.cuts import Cuts
from plots.common.plot_defs import cutlist

cuts_ele = {
	'qcd_2j0t': cutlist['2j0t']*cutlist['presel_ele']*Cuts.deltaR(0.3)*Cuts.antiiso('ele'),
	'qcd_2j1t': cutlist['2j1t']*cutlist['presel_ele']*Cuts.deltaR(0.3)*Cuts.antiiso('ele'),
	'signal': cutlist['2j1t']*cutlist['presel_ele']
}
cuts_mu = {
	'qcd_2j0t': cutlist['2j0t']*cutlist['presel_mu']*Cuts.deltaR(0.3)*Cuts.antiiso('mu'),
	'qcd_2j1t': cutlist['2j1t']*cutlist['presel_mu']*Cuts.deltaR(0.3)*Cuts.antiiso('mu'),
	'signal': cutlist['2j1t']*cutlist['presel_mu']
}

root = 'qcd_step3'
dtp_isomc = 'mc/iso/nominal/Jul15'
dtp_antiisodt = 'data/antiiso/Jul15'

bglist = {}
bglist['ele'] = ['SingleEle1', 'SingleEle2']
bglist['mu']  = ['SingleMu1',  'SingleMu2',  'SingleMu3']
siglist = ['T_t', 'Tbar_t', 'T_t_ToLeptons', 'Tbar_t_ToLeptons']

def showeff(smpls, cut1, cut2):
	print 'Samples:', smpls
	tot_cut1 = tot_cut2 = 0
	for s in smpls:
		tfile = ROOT.TFile(s)
		tree = tfile.Get('trees/Events')
		evs_cut1 = tree.GetEntries(cut1)
		evs_cut2 = tree.GetEntries(cut2)
		
		try: ratio = float(evs_cut2)/float(evs_cut1)
		except ZeroDivisionError: ratio = 'NaN'
		print ' for {0}: {1}, {2} ({3})'.format(s, evs_cut1, evs_cut2, ratio)

		tot_cut1 += evs_cut1; tot_cut2 += evs_cut2
	try: ratio = float(tot_cut2)/float(tot_cut1)
	except ZeroDivisionError: ratio = 'NaN'
	print 'Summary: {0}, {1} ({2})'.format(tot_cut1, tot_cut2, ratio)

showeff(map(lambda x: os.path.join(root,'mu',dtp_isomc,x)+'.root', siglist), str(cuts_mu['signal']),  str(cuts_mu['signal']*Cuts.mt_mu))
showeff(map(lambda x: os.path.join(root,'mu',dtp_antiisodt,x)+'.root', bglist['mu']), str(cuts_mu['qcd_2j1t']),  str(cuts_mu['qcd_2j1t']*Cuts.mt_mu))

showeff(map(lambda x: os.path.join(root,'ele',dtp_isomc,x)+'.root', siglist), str(cuts_ele['signal']),  str(cuts_ele['signal']*Cuts.met))
showeff(map(lambda x: os.path.join(root,'ele',dtp_antiisodt,x)+'.root', bglist['ele']), str(cuts_ele['qcd_2j1t']),  str(cuts_ele['qcd_2j1t']*Cuts.met))

showeff(map(lambda x: os.path.join(root,'mu',dtp_isomc,x)+'.root', siglist), str(cuts_mu['signal']),  str(cuts_mu['signal']*Cuts.met))
showeff(map(lambda x: os.path.join(root,'mu',dtp_antiisodt,x)+'.root', bglist['mu']), str(cuts_mu['qcd_2j1t']),  str(cuts_mu['qcd_2j1t']*Cuts.met))

