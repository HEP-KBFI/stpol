import os
from subprocess import call

indir = '/hdfs/local/joosep/wjetsnlo/'
if __name__ == "__main__":
    for dirname, dirnames, filenames in os.walk(indir):
        for f in filenames:
            sp = f.split(".")
            outfname = "converted_%s.root" % sp[1]
            call(["cmsRun", "hepmc2edm.py", "inputFiles=file:%s/%s" % (dirname, f), "outputFile=file:./converted/%s" % outfname])
