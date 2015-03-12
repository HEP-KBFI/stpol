from mva_variables import *
import argparse
from tmva import *
import sys
import os
import ROOT
import copy

def roc_plot_with_remove(args):
    from ROOT import TFile,TH1F,THStack,TLegend,TCanvas,gStyle,kFALSE
    from copy import copy
    
    eff_cut = 0.55
    if args.channel == "mu":
        eff_cut = 0.7

    proc = args.channel

    cur=[]
    base='_with'
    name='roc'
    hist={}
    leg=TLegend(0.1,0.1,0.5,0.7)
    c=TCanvas('c','c')
    col=0
    gStyle.SetOptStat(kFALSE)
    gStyle.SetOptTitle(kFALSE)
    method = "final2"
    removed = get_removed(args.channel)
    name = ""
    full_list = get_varlist_removed(args.channel)

    args.var = full_list
    name = ""
    for f in args.var:
        name += "__"+f
    fn = "TMVA_remove__"+args.channel+name+".root"
    col+=1
    if col == 10: col = 40
    if col == 43: col = 50
    print fn
    print method
    f=TFile('%s' % (fn))
    h=f.Get('Method_BDT/%s_%s_rm/MVA_%s_%s_rm_rejBvsS' % (method, args.channel, method, args.channel))
    print 'Method_BDT/%s_%s_rm/MVA_%s_%s_rm_rejBvsS' % (method, args.channel, method, args.channel)
    print h
    hist[name]=copy(h)
    hist[name].SetName(name)
    hist[name].SetLineColor(col)
    hist[name].SetMaximum(1.)
    sm='same'
    print "baseline", h.Interpolate(eff_cut)
    sm=''
    hist[name].Draw('l'+sm)
    #leg.AddEntry(hist[name],name[2:],'l')
    leg.AddEntry(hist[name],"All variables",'l')
 
    args.var = full_list
    for v in removed:
        args.var.remove(v)
        name = ""
        for f in args.var:
            name += "__"+f
        fn = "TMVA_remove__"+args.channel+name+".root"
        col+=1
        if col == 10: col = 40
        if col == 43: col = 50
        f=TFile('%s' % (fn))
        h=f.Get('Method_BDT/%s_%s_rm/MVA_%s_%s_rm_rejBvsS' % (method, args.channel, method, args.channel))
        hist[name]=copy(h)
        #print fn
        hist[name].SetName(name)
        hist[name].SetLineColor(col)
        hist[name].SetMaximum(1.)
        sm='same'
        print name, h.Interpolate(eff_cut)
        if v==varRank[proc][0]:
            sm=''
        hist[name].Draw('l'+sm)
        leg.AddEntry(hist[name],name[2:],'l')

    full_list = get_varlist_removed(args.channel)
    for v in get_checkvars_remove(args.channel):
        args.var = get_checkvars_remove(args.channel)
        print args.var
        args.var.remove(v)
        name = ""
        #print "removed", v
        for f in args.var:
            name += "__"+f
        fn = "TMVA_remove__"+args.channel+name+".root"
        #print fn
        col+=1
        if col == 10: col = 40
        if col == 43: col = 50
        f=TFile('%s' % (fn))
        h=f.Get('Method_BDT/%s_%s_rm/MVA_%s_%s_rm_rejBvsS' % (method, args.channel, method, args.channel))
        hist[v]=copy(h)
        hist[v].SetName(name+"__"+v)
        hist[v].SetLineColor(col)
        print v, h.Interpolate(eff_cut)
        sm='same'
        if v==varRank[proc][0]:
            sm=''
        hist[v].Draw('l'+sm)
        label = v
        #if len(get_removed(args.channel)) > 0:
        label = name[3:]
        leg.AddEntry(hist[v], str(v) + " removed" ,'l')
    

    leg.Draw('goff BATCH')
    fixed = get_removed(args.channel)
    name = ""
    for v in fixed:
        name += "__"+v
        
    c.SaveAs('ROCs_removed_'+args.channel+'_'+name[2:]+'.png')
    c.SaveAs('ROCs_removed_'+args.channel+'_'+name[2:]+'.pdf')

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Train QCD MVA")
    parser.add_argument(
        "-c",
        "--channel", type=str, required=True, choices=["mu", "ele"], dest="channel", default=None,
        help="the lepton channel to use"
    )
    parser.add_argument(
        "-i",
        "--indir", type=str, required=False, default=(os.environ["STPOL_DIR"] + "/src/qcd_ntuples/mva_input"),
        help="the input directory, which is expected to contain the subdirectories: mu/ele"
    )
    parser.add_argument(
        '-d',
        '--debug', required=False, default=False, action='store_true', dest='debug',
        help='Enable debug printout'
    )
    """parser.add_argument(
        '-l',
        '--lumitag', required=False, default='83a02e9_Jul22', type=str, dest='lumitag',
        help='Luminosity tag for total integrated lumi'
    )"""
    parser.add_argument(
        '-v',
        '--var', required=False, default=[], action='append', type=str, dest="rej_var",
        help='Variable to remove from MVA training'
    )
    parser.add_argument(
        '-r',
        '--rank', required=False, default=[], action='append', type=str, dest="rank_var",
        help='Variable to use in training for rank cumulation'
    )
    args = parser.parse_args()
    
    
    
    for v in get_checkvars_remove(args.channel):
        args.var = get_checkvars_remove(args.channel)
        args.var.remove(v)
        name = ""
        for f in args.var:
            name += "__"+f
        print args.var
        if len(args.var) == 0: continue        
        fn = "TMVA_remove__"+args.channel+name+".root"
        doTMVA(args, filename=fn, rm_extra="_rm")
    
    args.var = get_checkvars_remove(args.channel)
    name = ""
    for f in args.var:
            name += "__"+f
    print args.channel+name+".root"
    doTMVA(args, filename="TMVA_remove__"+args.channel+name+".root", rm_extra="_rm")
    
    roc_plot_with_remove(args)


