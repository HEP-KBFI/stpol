from mva_variables import *
import argparse
from tmva import *
import sys
import os
import ROOT


def roc_plot(args):
    from ROOT import TFile,TH1F,THStack,TLegend,TCanvas,gStyle,kFALSE
    from copy import copy
    
    eff_cut = 0.5
    if args.channel == "mu":
        eff_cut = 0.7

    proc = args.channel

    cur=[]
    base='_with'
    name='roc'
    hist={}
    leg=TLegend(0.1,0.1,0.7,0.5)
    c=TCanvas('c','c')
    col=0
    gStyle.SetOptStat(kFALSE)
    gStyle.SetOptTitle(kFALSE)
    method = "final2"
    fixed = get_fixed(args.channel)
    name = ""
    for v in fixed:
        name += "__"+v
        fn = "TMVA__"+args.channel+name+".root"
        col+=1
        if col == 10: col = 40
        if col == 43: col = 50
        f=TFile('%s' % (fn))
        h=f.Get('Method_BDT/%s_%s/MVA_%s_%s_rejBvsS' % (method, args.channel, method, args.channel))
        hist[name]=copy(h)
        hist[name].SetName(name)
        hist[name].SetLineColor(col)
        hist[name].SetMaximum(1.)
        sm='same'
        print name, h.Interpolate(eff_cut)
        if v==get_fixed(args.channel)[0]:
            sm=''
        hist[name].Draw('l'+sm)
        legtitle = name[2:].replace("__"," + ").replace("met", "MET").replace("top_mass","m_{top}").replace("mu_mtw", "m_{T}").replace("ljet_pt", "p_{T}^{lj}").replace("top_eta",  "\eta_{top}").replace("bjet_pt", "p_{T}^{bj}")
        leg.AddEntry(hist[name],legtitle,'l')

    for v in get_checkvars(args.channel):
        fn = "TMVA__"+args.channel+name+"__"+v+".root"
        col+=1
        if col == 10: col = 40
        if col == 43: col = 50
        print fn
        f=TFile('%s' % (fn))
        h=f.Get('Method_BDT/%s_%s/MVA_%s_%s_rejBvsS' % (method, args.channel, method, args.channel))
        hist[v]=copy(h)
        hist[v].SetName(name+"__"+v)
        hist[v].SetLineColor(col)
        hist[v].SetMaximum(1.)
        print v, h.Interpolate(eff_cut)
        sm='same'
        if len(fixed) == 0 and v == get_checkvars(args.channel)[0]:
            sm=''
        #hist[v].Draw('l'+sm)
        label = v
        if len(get_fixed(args.channel)) > 0:
            label = name[2:]+" + " +v
        #leg.AddEntry(hist[v], label ,'l')
    
    leg.Draw('goff BATCH')
    fixed = get_fixed(args.channel)
    name = ""
    for v in fixed:
        name += "__"+v
    c.SaveAs('ROCs_'+args.channel+'_'+name[2:]+'.png')
    c.SaveAs('ROCs_'+args.channel+'_'+name[2:]+'.pdf')


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
    
    fixed = get_fixed(args.channel)
    name = ""
    for f in fixed:
        name += "__"+f
    
    for v in get_checkvars(args.channel):
        args.var = get_fixed(args.channel)
        args.var.append(v)
        print args.var
        fn = "TMVA__"+args.channel+name+"__"+v+".root"
        doTMVA(args, filename=fn)
    #args.var = get_fixed(args.channel)
    #if len(args.var)>0:
    #    print args.channel+name+".root"
    #    doTMVA(args, filename="TMVA__"+args.channel+name+".root")
    
    roc_plot(args)


