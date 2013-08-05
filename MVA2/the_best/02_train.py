import sys

import ROOT

from mvalib.train import MVATrainer

trainoptions = "!H:!V:NTrees=2000:BoostType=Grad:Shrinkage=0.1:!UseBaggedGrad:nCuts=2000:nEventsMin=100:NNodesMax=5:"\
               "UseNvars=4:PruneStrength=5:PruneMethod=CostComplexity:MaxDepth=6"

cuteff = {}
cuteff['ele'] = 0.25983790132790596
cuteff['mu']  = 0.287744526372574

varlist = {}
varlist['ele'] = ['top_mass', 'eta_lj', 'C', 'met', 'mt_el', 'mass_bj', 'mass_lj', 'el_pt', 'pt_bj']
varlist['mu']  = ['top_mass', 'eta_lj', 'C', 'met', 'mt_mu', 'mass_bj', 'mass_lj', 'mu_pt', 'pt_bj']

def train(lept):
	trainer = MVATrainer("trees/prepared_{0}.root".format(lept), ofName = "trees/trained_{0}.root".format(lept), jobname="BDT_AjaM_{0}".format(lept))
	for var in varlist[lept]:
		trainer.add_variable(var)
	trainer.book_method("BDT", "BDT_AjaM", trainoptions)
	trainer.get_factory().TrainAllMethods()
	trainer.evaluate()
	trainer.pack()
	trainer.finish()


def find_score(lept, method_name):
	print "finding score ({0}) for {1}".format(lept, method_name)
	f = ROOT.TFile("trees/trained_{0}_{1}.root".format(lept, method_name))
	roc = f.Get("Method_BDT/{0}/MVA_{0}_rejBvsS".format(method_name)) #type = ROOT::TH1D
	score = roc.GetBinContent(roc.GetXaxis().FindBin(cuteff[lept]))
	f.Close()
	return score

def main(args):
	if len(args) > 1:
		if args[1] != "mu" and args[1] != "ele":
			print "invalid argument, must be [mu|ele]"
			return
		lept = args[1]
		
		train(lept)
	else:
		train("ele")
		train("mu")

if __name__ == "__main__":
	main(sys.argv)


