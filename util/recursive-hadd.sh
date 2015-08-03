#!/bin/bash
set -e
#source ~/local-sl6/root/bin/thisroot.sh

#GNU parallel
PARCMD=~joosep/parallel

#list of input files
SRCFILE=$1

#directory under which to save output, will be created
DSTDIR=$2
mkdir -p $DSTDIR

#first pass, 10 files per hadd
rm -Rf $DSTDIR/step1
mkdir -p $DSTDIR/step1
echo "step1"
cat $SRCFILE | $PARCMD -n5 hadd $DSTDIR/step1/merged_{#}.root {}

#second pass, 5 files per hadd
rm -Rf $DSTDIR/step2
mkdir -p $DSTDIR/step2
echo "step2"
find $DSTDIR/step1 -name "merged_*.root" | $PARCMD -n5 hadd $DSTDIR/step2/merged_{#}.root {}

#third pass, 5 files per hadd
rm -Rf $DSTDIR/step3
mkdir -p $DSTDIR/step3
echo "step3"
find $DSTDIR/step2 -name "merged_*.root" | $PARCMD -n5 hadd $DSTDIR/step3/merged_{#}.root {}


#4th pass, 6 files per hadd
rm -Rf $DSTDIR/step4
mkdir -p $DSTDIR/step4
echo "step4"
find $DSTDIR/step3 -name "merged_*.root" | $PARCMD -n6 hadd $DSTDIR/step4/merged_{#}.root {}

#final pass, hadd all
rm -f $DSTDIR/merged.root
echo "step5"
hadd $DSTDIR/merged.root $DSTDIR/step4/merged_*.root
rm -Rf $DSTDIR/step1
rm -Rf $DSTDIR/step2
rm -Rf $DSTDIR/step3
rm -Rf $DSTDIR/step4

#output is at $DSTDIR/merged.root
du -csh $DSTDIR/merged.root
