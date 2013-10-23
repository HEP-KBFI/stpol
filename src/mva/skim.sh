#!/bin/bash

JULIA=~/local-sl6/julia/julia

for fi in W1Jets_exclusive W2Jets_exclusive W3Jets_exclusive W4Jets_exclusive
do
    $JULIA ../skim/sub.jl skims/csvm/wjets/$fi  ../../filelists/Oct3_nomvacsv_nopuclean_e224b5/step2/mc/iso/nominal/Jul15/$fi.txt
done

for fi in TTJets_FullLept TTJets_SemiLept
do
    $JULIA ../skim/sub.jl skims/csvm/ttjets/$fi  ../../filelists/Oct3_nomvacsv_nopuclean_e224b5/step2/mc/iso/nominal/Jul15/$fi.txt
done

for fi in T_t_ToLeptons Tbar_t_ToLeptons
do
    $JULIA ../skim/sub.jl skims/csvm/tchan/$fi  ../../filelists/Oct3_nomvacsv_nopuclean_e224b5/step2/mc/iso/nominal/Jul15/$fi.txt
done