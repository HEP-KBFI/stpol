#!/bin/bash
inf=$1
od=`dirname $inf`

for syst in jes jer tchan_scale wzjets_scale ttjets_scale mass met pu btag_bc btag_l lepton_id lepton_iso lepton_trigger ttjets_matching wzjets_matching wjets_shape top_weight wjets_flavour_heavy wjets_flavour_light qcd_antiiso qcd_yield twchan schan dyjets diboson lepton_weight pdf tchan_qscale_me_weight ttjets_qscale_me_weight wzjets_qscale_me_weight wjets_pt_weight #wjets_light_matching wjets_light_scale
do
    for dir in up down
    do
        FN=$od/${syst}__${dir}.cfg
        cp $inf $FN
        #sed -i '' "s/systematic = nominal/systematic = $syst/" $FN
        #sed -i '' "s/direction = none/direction = $dir/" $FN
        #sed -i '' "s/nominal/${syst}__${dir}/" $FN
        sed -i "s/systematic = nominal/systematic = $syst/" $FN
        sed -i "s/direction = none/direction = $dir/" $FN
        sed -i "s/nominal/${syst}__${dir}/" $FN
    done
done
