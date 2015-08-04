import os

rootdir = "/home/andres/single_top/stpol_pdf/src/step3/output/May30_deltaRs"
rootdir = "/home/andres/single_top/stpol_pdf/src/step4/output_plots"

count = 0
count_above0 = 0
for subdir, dirs, files in os.walk(rootdir):
    for f in files:
        if f.endswith(".root"):
            print subdir + "/" +f
            count += 1
            if os.path.getsize(subdir + "/" +f):
                count_above0 += 1
#print count, count_above0
