import shutil
import os

import ROOT

from mvalib.prepare import MVAPreparer
from plots.common.cuts import Cuts
from plots.common.plot_defs import cutlist

cut_test_antiiso = {}
cut_train_antiiso = {}
cut_iso = {}
cut_train_antiiso['ele'] = str(cutlist['2j0t']*cutlist['presel_ele']*Cuts.deltaR(0.3)*Cuts.antiiso('ele'))
cut_train_antiiso['mu']  = str(cutlist['2j0t']*cutlist['presel_mu']*Cuts.deltaR(0.3)*Cuts.antiiso('mu'))
cut_test_antiiso['ele']  = str(cutlist['2j1t']*cutlist['presel_ele']*Cuts.deltaR(0.3)*Cuts.antiiso('ele'))
cut_test_antiiso['mu']   = str(cutlist['2j1t']*cutlist['presel_mu']*Cuts.deltaR(0.3)*Cuts.antiiso('mu'))
cut_iso['ele']           = str(cutlist['2j1t']*cutlist['presel_ele'])
cut_iso['mu']            = str(cutlist['2j1t']*cutlist['presel_mu'])

bglist = {}
bglist['ele'] = ['SingleEle1', 'SingleEle2']
bglist['mu']  = ['SingleMu1',  'SingleMu2',  'SingleMu3']

shutil.rmtree('trees', ignore_errors=True); os.mkdir('trees')

for lepton_channel in ['ele', 'mu']:

	prep = MVAPreparer("../step3_latest")

	#signal
	prep.add_train('signal', 'T_t', 'iso',              cut_iso[lepton_channel])
	prep.add_train('signal', 'Tbar_t', 'iso',           cut_iso[lepton_channel])
	prep.add_test ('signal', 'T_t_ToLeptons', 'iso',    cut_iso[lepton_channel])
	prep.add_test ('signal', 'Tbar_t_ToLeptons', 'iso', cut_iso[lepton_channel])

	
	#QCD
	for bg in bglist[lepton_channel]:
		prep.add_train('background', bg, 'antiiso', cut_train_antiiso[lepton_channel])
		prep.add_test ('background', bg, 'antiiso', cut_test_antiiso[lepton_channel])

	prep.write(lepton_channel, "trees/prepared_{0}.root".format(lepton_channel), step3_ofdir="trees")
