import ROOT
import logging
import pickle
import copy
import pdb
import string
import sys

try:
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()
    from sqlalchemy import Column, Integer, String
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
except:
    print "SQLAlchemy needed, please install"
    sys.exit(1)
    
import os
import numpy
import copy
from common.cross_sections import xs as sample_xs_map
import fnmatch
import itertools

logging.basicConfig(level=logging.INFO, format="%(asctime)s;%(levelname)s;%(name)s;%(message)s")

class TObjectOpenException(Exception): pass
class HistogramException(Exception): pass

def filter_alnum(s):
    """Filter out everything except ascii letters and digits"""
    return filter(lambda x: x in string.ascii_letters+string.digits + "_", s)

class Cuts:
    class Cut:
        def __init__(self, cut_str):
            self.cut_str = cut_str
        def __mul__(self, other):
            cut_str = '('+self.cut_str+') && ('+other.cut_str+')'
            return Cuts.Cut(cut_str)

    top_mass = Cut("top_mass > 130 && top_mass < 220")
    eta_lj = Cut("eta_lj > 2.5")
    mt_mu = Cut("mt_mu > 50")
    rms_lj = Cut("rms_lj < 0.025")
    top_mass_sig = Cut("top_mass >130 && top_mass<220")

    @staticmethod
    def n_jets(n):
        return Cuts.Cut("n_jets == %.1f" % float(n))
    @staticmethod
    def n_tags(n):
        return Cuts.Cut("n_tags == %.1f" % float(n))



class Histogram(Base):
    __tablename__ = "histograms"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    histogram_entries = Column(Integer)

    var = Column(String)
    cut = Column(String)
    weight = Column(String)
    sample_name = Column(String)
    sample_entries_cut = Column(Integer)
    sample_entries_total = Column(Integer)
    hist_dir = Column(String)
    hist_file = Column(String)

    def __init__(self, *args, **kwargs):
        super(Histogram, self).__init__(*args, **kwargs)
        self.pretty_name = self.name


    def setHist(self, hist, **kwargs):
        self.hist = hist
        self.name = str(self.hist.GetName())
        self.histogram_entries = int(kwargs["histogram_entries"])
        self.var = kwargs["var"]
        self.cut = kwargs["cut"]
        self.weight = kwargs["weight"]
        self.sample_name = kwargs["sample_name"]
        self.sample_entries_cut = kwargs["sample_entries_cut"]
        self.sample_entries_total = kwargs["sample_entries_total"]
        self.integral = None
        self.err = None
        self.is_normalized = False
        self.update()

    def calc_int_err(self):
        err = ROOT.Double()
        integral = self.hist.IntegralAndError(1, self.hist.GetNbinsX(), err)
        self.err = err
        self.integral = integral
        return (self.integral, self.err)

    def normalize(self, target=1.0):
        if self.hist.Integral()>0:
            self.hist.Scale(target/self.hist.Integral())
            self.is_normalized = True
        else:
            logging.warning("Histogram %s integral=0, not scaling." % str(self))

    def normalize_lumi(self, lumi=1.0):
        expected_events = sample_xs_map[self.sample_name] * lumi
        total_events = self.sample_entries_total
        scale_factor = float(expected_events)/float(total_events)
        self.hist.Scale(scale_factor)

    def update(self, file=None, dir=None):
        self.name = str(self.hist.GetName())
        if file and dir:
            self.hist_dir = dir.GetName()
            self.hist_file = file.GetName()
        else:
            try:
                self.hist_dir = self.hist.GetDirectory().GetName()
            except ReferenceError as e:
                self.hist_dir = None
            try:
                self.hist_file = self.hist.GetDirectory().GetFile().GetName()
            except ReferenceError as e:
                self.hist_file = None

    def loadFile(self):
        self.fi = ROOT.TFile(self.hist_file)
        self.hist = self.fi.Get(self.hist_dir).Get(self.name)
        self.update()

    def __repr__(self):
        return "<Histogram(%s, %s, %s)>" % (self.var, self.cut, self.weight)

    @staticmethod
    def unique_name(var, cut, weight):
        cut_str = cut if cut is not None else "NOCUT"
        weight_str = weight if weight is not None else "NOWEIGHT"
        return filter_alnum(var + "_" + cut_str + "_" + weight_str)

class Sample:
    def __init__(self, name, file_name):
        self.name = name
        self.file_name = file_name
        self.logger = logging.getLogger(str(self))

        try:
            self.tfile = ROOT.TFile(file_name)
            if not self.tfile:
                raise FileOpenException("Could not open TFile %s: %s" % (self.file_name, self.tfile))
        except Exception as e:
            raise e

        self.tree = self.tfile.Get("trees").Get("Events")
        if not self.tree:
            raise TObjectOpenException("Could not open tree Events from file %s: %s" % (self.tfile.GetName(), self.tree))
        self.tree.SetCacheSize(100*1024*1024)
        #self.tree.AddBranchToCache("*", 1)

        self.event_count = None
        self.event_count = self.getEventCount()
        if self.event_count<=0:
            self.logger.warning("Sample was empty: %s" % self.name)
            #raise Exception("Sample event count was <= 0: %s" % self.name)
        
        self.isMC = not self.file_name.startswith("Single")

        self.logger.info("Opened sample %s with %d final events, %d processed" % (self.name, self.getEventCount(), self.getTotalEventCount()))

    def getEventCount(self):
        if self.event_count is None:
            self.event_count = self.tree.GetEntries()
        return self.event_count

    def getBranches(self):
        return [x.GetName() for x in self.tree.GetListOfBranches()]

    def getTotalEventCount(self):
        count_hist = self.tfile.Get("trees").Get("count_hist")
        if not count_hist:
            raise TObjectOpenException("Failed to open count histogram")
        return count_hist.GetBinContent(1)

    def drawHistogram(self, var, cut, **kwargs):
        name = self.name + "_" + Histogram.unique_name(var, cut, kwargs.get("weight"))
        
        if(var not in self.getBranches()):
            raise KeyError("Plot variable %s not defined in branches" % var)

        plot_range = kwargs["plot_range"]

        weight_str = kwargs.get("weight")

        ROOT.gROOT.cd()
#        ROOT.TH1.AddDirectory(False)
        hist = ROOT.TH1F("htemp", "htemp", plot_range[0], plot_range[1], plot_range[2])
        hist.Sumw2()

#        hist.SetDirectory(ROOT.gROOT)

        draw_cmd = var + ">>htemp"
        
        if weight_str:
            cutweight_cmd = weight_str + " * " + "(" + cut + ")"
        else:
            cutweight_cmd = "(" + cut + ")"
    
        self.logger.debug("Calling TTree.Draw('%s', '%s')" % (draw_cmd, cutweight_cmd))

        n_entries = self.tree.Draw(draw_cmd, cutweight_cmd, "goff")
        self.logger.debug("Histogram drawn with %d entries" % n_entries)

        if n_entries<0:
            raise HistogramException("Could not draw histogram")

        if hist.Integral() != hist.Integral():
            raise HistogramException("Histogram had 'nan' Integral(), probably weight was 'nan'")
        #hist.SetDirectory(0)
        if not hist:
            raise TObjectOpenException("Could not get histogram: %s" % hist)
        if hist.GetEntries() != n_entries:
            raise HistogramException("Histogram drawn with %d entries, but actually has %d" % (n_entries, hist.GetEntries()))
        hist_new = hist.Clone(filter_alnum(name))

        hist = hist_new
        hist.SetTitle(name)
        hist_ = Histogram()
        hist_.setHist(hist, histogram_entries=n_entries, var=var,
            cut=cut, weight=kwargs["weight"] if "weight" in kwargs.keys() else None,
            sample_name=self.name,
            sample_entries_total=self.getTotalEventCount(),
            sample_entries_cut=self.getEventCount(),
            
        )
        return hist_

    def getColumn(self, col, cut):
        N = self.tree.Draw(col, cut, "goff")
        N = int(N)
        if N < 0:
            raise Exception("Could not get column %s: N=%d" % (col, N))
        buf = self.tree.GetV1()
        arr = ROOT.TArrayD(N, buf)
        self.logger.debug("Column retrieved, copying to numpy array")
        out = numpy.copy(numpy.frombuffer(arr.GetArray(), count=arr.GetSize()))
        return out

    def getEntries(self, cut):
        return int(self.tree.GetEntries(cut))

    @staticmethod
    def fromFile(file_name):
        sample_name = (file_name.split(".root")[0]).split("/")[-1]
        sample = Sample(sample_name, file_name)
        return sample

    @staticmethod
    def fromDirectory(directory):
        import glob
        file_names = glob.glob(directory + "/*.root")
        samples = [Sample.fromFile(file_name) for file_name in file_names]
        return samples

    def __repr__(self):
        return "<Sample(%s, %s)>" % (self.name, self.file_name)

    def __str__(self):
        return self.__repr__()


class HistoDraw:
    def __init__(self, file_name, samples):
        self.tfile = ROOT.TFile(file_name, "RECREATE")
        self.samples = samples

    def drawHistogram(self, var, cut=Cuts.Cut("1"), **kwargs):
        histos = dict()
        self.tfile.cd()
        plot_range = kwargs.get("plot_range")
        skip_weight = kwargs.get("skip_weight", [])

        cut_dir_name = filter_alnum(cut.cut_str)
        if not self.tfile.GetListOfKeys().FindObject(cut_dir_name):
            dirA = self.tfile.mkdir(cut_dir_name)
        else:
            self.tfile.cd(cut_dir_name)
            dirA = self.tfile.Get(cut_dir_name)

        histos = list()

        for sample in self.samples:
            try:
                #histo_name = sample.name + "_" + var + "_" + cut_dir_name + "_" + (kwargs["weight"] if "weight" in kwargs.keys() else "")
                sample_args = copy.deepcopy(kwargs)
                if(
                    ("weight" in sample_args.keys()) and
                    (
                        (not sample.isMC) or
                        (sum([fnmatch.fnmatch(sample.name, match) for match in skip_weight]) > 0)
                    )
                ):
                    logging.debug("Not using weights on sample %s" % str(sample))
                    sample_args.pop("weight")
                
                hist = sample.drawHistogram(
                    var, cut.cut_str,
                    **sample_args
                )

                dirA.cd()
                hist.hist.Write()
                hist.update(file=self.tfile, dir=dirA)
                histos += [hist]
                self.tfile.Write()
            except HistogramException as e:
                logging.error("Caught exception (%s) while drawing histogram for sample %s" % (str(e), str(sample)))
        return histos

class MetaData:
    logger = logging.getLogger("MetaData")
    def __init__(self, fname, create_new=False):
        if create_new:
            try:
                os.remove(fname)
                self.logger.info("Deleted previous metadata file %s" % fname)
            except OSError as e:
                pass

        self.engine = create_engine('sqlite:///%s' % fname)
        Session = sessionmaker(bind = self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)
        self.logger.info("Opened connection to metadata database: %s" % str(self.engine))

    def save(self, obj):
        self.session.add(obj)
        self.session.commit()
        self.session.flush()

    def get_histogram(self, sample_name, var, cut_str=None, weight=None, limit=1):
        hist = None
        for hist_ in self.session.query(Histogram).\
            filter(Histogram.sample_name==sample_name).\
            filter(Histogram.var==var).\
            filter(Histogram.weight==weight).\
            filter(Histogram.cut==cut_str).\
            limit(1):
            
            hist_.loadFile()
            hist = hist_
        if not hist:
            raise KeyError("No match found for sample_name(%s), var(%s), cut_str(%s), weight(%s)" % (sample_name, var, cut_str, weight))
            
        return hist

        

def getBTaggingEff(sample, flavour, cut):
    if flavour not in ["b", "c", "l"]:
        raise ValueError("Flavour must be b, c or l")

    N_tagged = numpy.sum(sample.getColumn("true_%s_tagged_count" % flavour, cut))
    N = numpy.sum(sample.getColumn("true_%s_count" % flavour, cut))
    return N_tagged/N

if __name__=="__main__":

    metadata = MetaData("histos.db", create_new=True)
    samples = list()
    samples = Sample.fromDirectory("/Users/joosep/Documents/stpol/data/")
    samplesDict = dict()
    for sample in samples:
        samplesDict[sample.name] = sample
    #samples = [Sample.fromFile("/Users/joosep/Documents/stpol/TTJets_FullLept_sf.root")]

    histos = dict()
    hdraw = HistoDraw("histos.root", samples)

    histos = []
    b_weight_range = [100, 0.7, 1.5]

    class Cleanup:
        def __init__(self, metadata, hdraw, histos):
            self.metadata = metadata
            self.hdraw = hdraw
            self.histos = histos
        def __enter__(self):
            pass
        def __exit__(self, type, value, traceback):
            self.metadata.session.close_all()
            self.hdraw.tfile.Write()
            self.hdraw.tfile.Close()
            #del self.hdraw
            print "Done cleanup"

    with Cleanup(metadata, hdraw, histos):
        try:
            histos += hdraw.drawHistogram("n_tags", cut=Cuts.mt_mu*Cuts.n_jets(2), plot_range=[5, 0, 5])
            histos += hdraw.drawHistogram("top_mass", cut=Cuts.mt_mu*Cuts.n_jets(2)*Cuts.n_tags(1)*Cuts.eta_lj, plot_range=[40, 100, 350])
            histos += hdraw.drawHistogram("cos_theta", cut=Cuts.mt_mu*Cuts.n_jets(2)*Cuts.n_tags(1)*Cuts.eta_lj*Cuts.top_mass_sig, plot_range=[40, -1, 1])

            histos += hdraw.drawHistogram("cos_theta", cut=Cuts.mt_mu*Cuts.n_jets(2)*Cuts.n_tags(1)*Cuts.eta_lj*Cuts.top_mass_sig,
                plot_range=[40, -1, 1], weight="pu_weight", skip_weights=["SingleMu*"]
            )

            n_jets = [2,3]
            n_tags = [0,1,2]
            weights = [None, "pu_weight"]
            for nj, nt, weight in itertools.product(n_jets, n_tags, weights):
                histos += hdraw.drawHistogram("eta_lj", cut=Cuts.mt_mu*Cuts.n_jets(nj)*Cuts.n_tags(nt), plot_range=[40, -5, 5],
                    weight=weight,
                    skip_weight=["QCD*", "SingleMu*"]
                )
            
            for h in histos:
                metadata.save(h)
            logging.info("Done saving %d histograms to histos.db" % len(histos))
        except HistogramException as e:
            pass
            #raise e

    do_b_effs = False
    if do_b_effs:
        logging.info("Doing b-tagging efficiency calculations")
        cuts = []
        cuts.append("n_jets==2 && top_mass>130 && top_mass<220 && mt_mu>50")
    #    cuts.append("n_jets==3 && top_mass>130 && top_mass<220 && mt_mu>50")
    #    cuts.append("n_jets==2 && !(top_mass>130 && top_mass<220) && mt_mu>50")
    #    cuts.append("n_jets==3 && !(top_mass>130 && top_mass<220) && mt_mu>50")
        for cut in cuts:
            print cut
            #for sample in ["TTJets_FullLept", "TTJets_SemiLept", "TTJets_MassiveBinDECAY", "T_t", "WJets_inclusive"]:
            for sample in ["TTJets_MassiveBinDECAY", "T_t", "WJets_inclusive"]:
                for flavour in ["b", "c", "l"]:
                    entries = samplesDict[sample].getEntries(cut)
                    total = samplesDict[sample].getTotalEventCount()
                    eff = getBTaggingEff(samplesDict[sample], flavour, cut)
                    print "%s | %s | %.3E/%.3E | %.3E" % (sample, flavour, entries, total, eff)