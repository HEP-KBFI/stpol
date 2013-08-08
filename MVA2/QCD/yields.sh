#!/bin/bash

#../tools/efffinder.py -l ele -c "Cuts.met"
# returns 51.5%

#../tools/cutfinder.py -l ele -v mva_anti_QCD_MVA -e 0.515
#outputs mva_anti_QCD_MVA > 0.749261170626
CUT="mva_anti_QCD_MVA>0.749261170626"

echo "Iso region: "
for f in ../step3_latest/ele/mc/iso/nominal/Jul15/*.root
do
	echo $f | grep -oh [_a-zA-Z0-9]*\.root
	echo -ne "   MVA cut: " 
	../tools/efffinder.py -l ele -c "Cut('$CUT')" $f | grep -Poh [0-9]*\.[0-9]\%.*?\\\)
	echo -ne "   Cuts.met: "
	../tools/efffinder.py -l ele -c "Cuts.met" $f | grep -Poh [0-9]*\.[0-9]\%.*?\\\)
done

echo "Antiiso region: "
for f in ../step3_latest/ele/data/antiiso/Jul15/*.root
do
	echo $f | grep -oh [_a-zA-Z0-9]*\.root
	echo -ne "   MVA cut: " 
	../tools/efffinder.py -l ele -p "cutlist['2j1t']*cutlist['presel_ele']*Cuts.deltaR(0.3)*Cuts.antiiso('ele')" -c "Cut('$CUT')" $f | grep -Poh [0-9]*\.[0-9]\%.*?\\\)
	echo -ne "   Cuts.met: "
	../tools/efffinder.py -l ele -p "cutlist['2j1t']*cutlist['presel_ele']*Cuts.deltaR(0.3)*Cuts.antiiso('ele')" -c "Cuts.met" $f | grep -Poh [0-9]*\.[0-9]\%.*?\\\)
done

