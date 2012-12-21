
class C(object):
    @classmethod
    def _toStr(cls):
        s = "Config: " + cls.__name__ + " {"
        for k in dir(cls):
            if k[0].islower():
                s += "\n\t%s = %s" % (k, getattr(cls, k))
        # for c in cls.__bases__:
        #     if hasattr(c, "toStr"):
        #         s += c.toStr()
        s += "\n}"
        return s

"""
This is the single global static (singleton type) configuration class, that is read by the SingleTopStep2 code.
"""
class Config(C):

    """
    An enum for choosing the channel.
    signal - run over T_t or Tbar_t
    background - run over anything else (or data)
    """
    class Channel:
        signal = "signal"
        background = "background"

    channel = Channel.background

    #Whether to run the muon channel
    doMuon = True

    #Whether to run the electron channel
    doElectron = True

    #Whether to filter the HLT
    filterHLT = True

    #Whether to use the cross-strigger or the single lepton trigger
    useXTrigger = False

    #Either running over MC or Data
    isMC = True

    #Enable debugging modules
    doDebug = False

    #Whether to output CMSSW-specific trees
    skipPatTupleOutput = True

    #Whether to run over grid (without command-line arguments)
    onGrid = False

    """
    Specifies the jet configuration.
    """
    class Jets(C):
        cutJets = False
        nJets = 2
        nBTags = 1
        ptCut = 40
        etaCut = 4.7

        source = "selectedPatJets"

        class BTagDiscriminant:
            TCHP = "trackCountingHighPurBJetTags"
            CSV_MVA = "combinedSecondaryVertexMVABJetTags"
        class BTagWorkingPoint:
            TCHPT = "TCHPT"
            CSVT = "CSVT"
            CSVM = "CSVM"

            WP = {"TCHPT":3.41, "CSVT":0.898, "CSVM":0.679}

        bTagDiscriminant = BTagDiscriminant.TCHP
        bTagWorkingPoint = BTagWorkingPoint.TCHPT

        @classmethod
        def BTagWorkingPointVal(c):
            return c.BTagWorkingPoint.WP[c.bTagWorkingPoint]

    class Leptons(C):
        class WTransverseMassType:
            MtW = "MtW"
            MET = "MET"

        class RelativeIsolation:
            rhoCorrRelIso = "rhoCorrRelIso"
            deltaBetaCorrRelIso = "deltaBetaCorrRelIso"

        reverseIsoCut = False
        cutOnIso = True
        cutOnTransverseMass = False
        transverseMassType = "MtW"
        transverseMassCut = 40
        relIsoType = RelativeIsolation.rhoCorrRelIso

        relIsoCutRangeIsolatedRegion = [0.0, 0.2]
        relIsoCutRangeAntiIsolatedRegion = [0.2, 0.5]
        looseVetoRelIsoCut = 0.2


    class Muons(Leptons):
        relIsoCutRangeIsolatedRegion = [0.0, 0.12]
        relIsoCutRangeAntiIsolatedRegion = [0.3, 0.5]
        looseVetoRelIsoCut = 0.2

    class Electrons(Leptons):
        pt = "ecalDrivenMomentum.Pt()"
        mvaCut = 0.98
        cutOnMVA = True
        relIsoCutRangeIsolatedRegion = [0.0, 0.1]
        relIsoCutRangeAntiIsolatedRegion = [0.1, 0.5]
        looseVetoRelIsoCut = 0.3


    Electrons.relIsoType = Leptons.RelativeIsolation.rhoCorrRelIso
    Muons.relIsoType = Leptons.RelativeIsolation.deltaBetaCorrRelIso

    # @classmethod
    # def toStr(c):
    #     s = "channel = %s" % Config.channel
    #     s += "\n" + Config.Jets.toStr()
    #     return s
