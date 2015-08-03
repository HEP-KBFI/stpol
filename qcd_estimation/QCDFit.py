class QCDFit:
    def __init__(self, channel = "mu", jt = "2j1t", cut = "reversecut", var = "qcd_mva"):
        self.channel = channel
        self.jt = jt
        self.cut = cut
        self.var = var
        self.result = None
        self.chi2 = None
        self.extras = {}
   
    def __str__(self):
        #string = self.getTitle()+"\n"
        string = self.getTitle()+"\n"  
        string += "qcd = "+str(self.qcd)+ " +- " +str(self.qcd_uncert)+"\n"
        string += "nonqcd = "+str(self.nonqcd)+ " +- " +str(self.nonqcd_uncert)+"\n"
        string += str(self.result)
        return string

    def geVar(self):
        return self.var.replace("qcd_mva", "QCD BDT")

    def getCut(self):
        region = "full variable range"
        if self.cut == "qcdcut":
            region = "above QCD cut"
        elif self.cut == "reversecut":
            region = "below QCD cut"
        return region

    def getTitle(self):
        return "%s channel, %s, %s, %s" % (self.channel, self.jt, self.cut, self.var)
    """extra_string = ""
    for k,v in extra.items():
        vark = k.replace("varMC_QCDMC",", QCD from MC").replace("varMC_",", MC antiiso").replace("isovar", "Anti-iso range")
        extra_string += "%s %s" % (vark,v)
    """
