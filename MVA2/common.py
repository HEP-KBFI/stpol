import pickle
import ROOT
from plots.common import cross_sections
from plots.common import cuts


rootfilepath = "step3_latest/"


vartypes = {
	"bdiscr_bj" : "F",
	"bdiscr_lj" : "F",
	"cos_theta" : "F",
	"deltaR_bj" : "F",
	"deltaR_lj" : "F",
	"el_mva" : "F",
	"el_pt" : "F",
	"el_reliso" : "F",
	"eta_bj" : "F",
	"eta_lj" : "F",
	"met" : "F",
	"mt_mu" : "F",
	"mu_eta" : "F",
	"mu_iso" : "F",
	"mu_pt" : "F",
	"pt_bj" : "F",
	"pt_lj" : "F",
	"rms_lj" : "F",
	"top_mass" : "F",
	"el_charge" : "I",
	"el_mother_id" : "I",
	"n_eles" : "I",
	"n_jets" : "I",
	"n_muons" : "I",
	"n_tags" : "I",
	"n_vertices" : "I",
	"n_veto_ele" : "I",
	"n_veto_mu" : "I",
	"event_id" : "I",
	"lumi_id" : "I",
	"run_id" : "I"
}


class MVA_meta:
	varlist = []
	xmlstring = ""
	method_tag = "" 
	cutstring = ""


class MVA_trainer:
	
	def __init__(self, jobname="jobname"):
		self.jobname = jobname
		self.signals = []
		self.backgrounds = []
		self.variables = []
		self.methods = []
		self.cutstring = str(cuts.Cuts.rms_lj*cuts.Cuts.mt_mu*cuts.Cuts.n_jets(2)*cuts.Cuts.n_tags(1))
		self.channel = "mu"
		self.files = {}
		self.trees = {}
		self.tempfile = ROOT.TFile("%s-TMVA.root"%jobname, "RECREATE")
		self.factory = ROOT.TMVA.Factory(jobname, self.tempfile)
	
	def set_channel(self, ch):
		if ch != "mu" and ch != "ele":
			print "MVA_trainer: Invalid channel: " + ch + ", please use \"ele\" or \"mu\"."
		else:
			channel = ch
	
	def add_signal(self, sg):
		if not sg in self.signals:
			self.signals.append(sg)
	
	def add_background(self, bg):
		if not bg in self.backgrounds:
			self.backgrounds.append(bg)
	
	def add_variable(self, var):
		if not var in self.variables:
			self.variables.append(var)
	
	def set_cutstring(self, cutstring):
		self.cutstring = cutstring
	
	def get_factory(self):
		return self.factory
	
	def prepare(self):	
		for sg in self.signals:
			self.files[sg] = ROOT.TFile(rootfilepath + self.channel + "/iso/nominal/" + sg + ".root")
			tree = self.files[sg].Get("trees/Events")
			self.trees[sg] = tree.CopyTree(self.cutstring)
			count_uncut = self.files[sg].Get("trees/count_hist").GetBinContent(1)
			weight = cross_sections.xs[sg]*cross_sections.lumi_iso[self.channel]/count_uncut
			self.factory.AddSignalTree(self.trees[sg], weight)
		for bg in self.backgrounds:
			self.files[bg] = ROOT.TFile(rootfilepath + self.channel + "/iso/nominal/" + bg + ".root")
			tree = self.files[bg].Get("trees/Events")
			self.trees[bg] = tree.CopyTree(self.cutstring)
			count_uncut = self.files[bg].Get("trees/count_hist").GetBinContent(1)
			weight = cross_sections.xs[bg]*cross_sections.lumi_iso[self.channel]/count_uncut
			self.factory.AddBackgroundTree(self.trees[bg], weight)
		for var in self.variables:
			self.factory.AddVariable(var, vartypes[var])
		return self.factory
	
	def book_method(self, method_type, tag, options):
		if tag in self.methods:
			print "MVA_trainer: Method tagged " + tag + " already booked. Skipping."
		self.methods.append(tag)
		self.factory.BookMethod(method_type, tag, options)
	
	def pack_and_finish(self):
		for meth in self.methods:
			meta = MVA_meta()
			meta.varlist = self.variables
			xmlfile = open("weights/%s_"%self.jobname+meth+".weights.xml")
			meta.xmlstring = xmlfile.read()
			meta.method_tag = meth
			meta.cutstring = self.cutstring
			pklfile = open("weights/%s_"%self.jobname+meth+".pkl", "wb")
			pickle.dump(meta, pklfile)
			pklfile.close()
		self.tempfile.Close()
