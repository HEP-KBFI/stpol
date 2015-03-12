#!/bin/bash
#generated file lists

#SKIM_DIR="/hdfs/local/joosep/stpol/mva/"
SKIM_DIR=/home/andres/single_top/stpol_pdf/src/step3/output/Jan27_fullData/iso/nominal

#TAG=$1
#BDT=$2
BDT=bdt_sig_bg_mixed_fullData

mkdir -p input/$BDT

find $SKIM_DIR/T*_t_ToLeptons -name "*.root" > input/$BDT/sig.txt
find $SKIM_DIR/T*_t -name "*.root" >> input/$BDT/sig.txt
find $SKIM_DIR/TTJets* -name "*.root" > input/$BDT/bg.txt
find $SKIM_DIR/W1Jets_exclusive -name "*.root" >> input/$BDT/bg.txt
find $SKIM_DIR/W2Jets_exclusive -name "*.root" >> input/$BDT/bg.txt
find $SKIM_DIR/W3Jets_exclusive -name "*.root" >> input/$BDT/bg.txt
find $SKIM_DIR/W4Jets_exclusive -name "*.root" >> input/$BDT/bg.txt
find $SKIM_DIR/WJets_inclusive -name "*.root" >> input/$BDT/bg.txt

#separate inclusive files
grep "/T_t/" input/$BDT/sig.txt > input/$BDT/train.txt
grep "/Tbar_t/" input/$BDT/sig.txt >> input/$BDT/train.txt
grep "/TTJets_MassiveBinDECAY/" input/$BDT/bg.txt >> input/$BDT/train.txt
grep "/WJets_inclusive/" input/$BDT/bg.txt >> input/$BDT/train.txt

grep "ToLeptons" input/$BDT/sig.txt > input/$BDT/test.txt
grep "Lept" input/$BDT/bg.txt >> input/$BDT/test.txt
grep "Jets_exclusive" input/$BDT/bg.txt >> input/$BDT/test.txt

