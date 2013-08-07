#/usr/bin/bash
sbatch="sbatch -pprio -Jmvafill"

filelist_ele=`find qcd_step3/ele/* -name "*root"`
filelist_mu=`find qcd_step3/mu/* -name "*root"`
for f in $filelist_ele; do
	$sbatch ./../tools/fill_same.py trees/trained_ele.root $f
done

filelist_mu=`find qcd_step3/mu/* -name "*root"`
for f in $filelist_mu; do
	$sbatch ./../tools/fill_same.py trees/trained_mu.root $f
done
