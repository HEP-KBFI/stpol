import sys

import ROOT

from mvalib.train import MVATrainer

trainoptions = "!H:!V:NTrees=2000:BoostType=Grad:Shrinkage=0.1:!UseBaggedGrad:nCuts=2000:nEventsMin=100:NNodesMax=5:"\
               "UseNvars=4:PruneStrength=5:PruneMethod=CostComplexity:MaxDepth=6"

varlist = {}
varlist['ele'] = ['top_mass', 'eta_lj', 'C', 'met', 'mt_el', 'mass_bj', 'mass_lj', 'el_pt', 'pt_bj']
varlist['mu']  = ['top_mass', 'eta_lj', 'C', 'met', 'mt_mu', 'mass_bj', 'mass_lj', 'mu_pt', 'pt_bj']

for lept in ['ele', 'mu']:
	trainer = MVATrainer("trees/prepared_{0}.root".format(lept), ofName = "trees/trained_{0}.root".format(lept), jobname="anti_QCD_MVA_{0}".format(lept))
	for var in varlist[lept]:
		trainer.add_variable(var)
	trainer.book_method("BDT", "anti_QCD_MVA", trainoptions)
	trainer.get_factory().TrainAllMethods()
	trainer.evaluate()
	trainer.pack()
	trainer.finish()


