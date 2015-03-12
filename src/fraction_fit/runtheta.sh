#!/bin/sh
echo "running theta wrapper";
#echo $PYTHONPATH
#shopt -s expand_aliases
#source ~/.bashrc
#shopt -s expand_aliases
#echo `which python`
#python -v
#DYLD_LIBRARY_PATH=../../theta/lib:$DYLD_LIBRARY_PATH ../../theta/utils2/theta-auto.py $@;
#echo $LD_LIBRARY_PATH
LD_LIBRARY_PATH=/scratch/andres/theta/lib:$LD_LIBRARY_PATH /scratch/andres/theta/utils2/theta-auto.py $@;
echo "theta wrapper is done";
exit 0;

