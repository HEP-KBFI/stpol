#!/bin/bash
timestamp=`eval date +%m_%d_%H_%M`
OFDIR=out_step3_$timestamp
FLDIR=filelist_step2_latest
mkdir -p $OFDIR/presel

$STPOL_DIR/analysis_step3/suball_presel.sh "--lepton=mu" $OFDIR/presel $FLDIR/presel/*
