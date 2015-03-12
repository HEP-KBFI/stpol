import fnmatch
import os
import numpy
import pickle
import sys
from parse_input import datasets
from variables import *
import scipy as sp
import scipy.stats
import numpy as np
# weights__cos_theta__mu__3j2t__NNPDF23nloas0122LHgrid__ZZ__1__30.pkl

#weights_dir = "/home/andres/single_top/stpol_pdf/src/pdf_uncertainties/weight_lists/"
weights_dir = "/home/andres/single_top/stpol_pdf/src/pdf_uncertainties/weightlists/"
def mean_confidence_interval(data, confidence=0.67):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), sp.stats.stderr(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return m, m-h, m+h

#""" from numpy doc:
"""
#!/usr/bin/env python
from numpy import *
from scipy.stats.distributions import  t


n = 10 #number of measurements
dof = n - 1 #degrees of freedom
avg_x = 16.1 #average measurement
std_x = 0.01 #standard deviation of measurements

#Find 95% prediction interval for next measurement

alpha = 1.0 - 0.95

pred_interval = t.ppf(1-alpha/2.,dof)*std_x*sqrt(1.+1./n)

print 'We are 95%% confident the next measurement will be between %1.3f and %1.3f' % (avg_x - pred_interval, avg_x + pred_interval)
"""


def calc_cutoffs(dataset, var, jt, files):
    if len(files) == 0:
        return {"min": 0., "max": 2.0}
    full_list = []
    for infile in files:    
        with open(weights_dir+"/"+dataset+"/"+jt+var+"/"+infile, 'rb') as f:
            weights = pickle.load(f)
            full_list.extend(weights)
    mean = numpy.mean(full_list)
    dev = numpy.std(full_list)
    min_val = mean - dev
    max_val = mean + dev
    #count_cutoff_effect(full_list, min_val, max_val)
    (mean, min_val, max_val) = mean_confidence_interval(weights)
    return {"down": min_val, "up": max_val}


def count_cutoff_effect(weights, min_cut, max_cut):
    normal = 0
    small = 0
    big = 0
    weights_normal = []
    for w in weights:
        if w < min_cut:
            small += 1
        elif w > max_cut:
            big += 1
        else:
            normal += 1
            weights_normal.append(w)
    mean = numpy.mean(weights)
    dev = numpy.std(weights)
    mean2 = numpy.mean(weights_normal)
    dev2 = numpy.std(weights_normal)
    print "normal: %d, big: %d, small: %d; %.3f +- %.3f -> %.3f +- %.3f" % (normal, big, small, mean, dev, mean2, dev2)
    print "interval", mean_confidence_interval(weights)
            

if __name__ == "__main__":
    ds = sys.argv[1]
    cutoffs = {}
    cutoffs[ds] = {}
    i = 0
    print weights_dir+"/"+ds
    print "asd", os.walk(weights_dir+"/"+ds)
    #for root, dir, files in os.walk(weights_dir):
    #print root
    #print dir
    #print files
    #print i
    #i += 1
    for var in ["cos_theta", "bdt_sig_bg"]:
        print var
        cutoffs[ds][var] = {}
        for channel in channels:
            cutoffs[ds][var][channel] = {}
            print channel
            for jt in jettag:
                print jt
                cutoffs[ds][var][channel][jt] = {}
                for root, dir, files in os.walk(weights_dir+"/"+ds+"/"+jt+var):
                    for bin in range(ranges[var][0]):
                        selected_files = fnmatch.filter(files, "weights__%s__%s__%s__*__%s__*__*__%s.pkl" % (var, channel, jt, ds, bin))
                        #print "weights__%s__%s__%s__*__%s__*__%s.pkl" % (var, channel, jt, ds, bin)
                        print var, channel, jt, ds, bin, len(selected_files)
                        if len(selected_files) > 0:
                            #print "SELECTED", selected_files
                            #print var, channel, jt, bin
                            cutoffs[ds][var][channel][jt][bin] = calc_cutoffs(ds, var, jt, selected_files)
                            
                            #print cutoffs[ds][var][channel][jt][bin]
    print "cutoffs", cutoffs
    outfilename = weights_dir + "/../cutoffs/cutoffs_%s.pkl" % ds
    outfile = open(outfilename, "wb")
    pickle.dump(cutoffs, outfile)
    outfile.close()
    print "finished"
