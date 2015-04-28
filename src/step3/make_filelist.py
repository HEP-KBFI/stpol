import os

#rootdir ='/hdfs/local/andres/stpol/step2/Oct28_reproc'
rootdir = "/home/andres/single_top/stpol_pdf/src/step3/output/Oct28_reproc"
#rootdir = "/home/andres/single_top/stpol_pdf/src/step3/output/Apr21_btags"
rootdir = "/home/andres/single_top/stpol_pdf/src/step4/output/"

count = 0
count_above0 = 0
#print "[/Jan11_deltaR]"
for subdir, dirs, files in os.walk(rootdir):
    #print subdir
    #print dirs
    #print files    
    for f in files:
        if f.endswith(".root"):
            print subdir + "/" +f
            count += 1
            if os.path.getsize(subdir + "/" +f):
                count_above0 += 1
#print count, count_above0
