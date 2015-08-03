include ../analysis/Makefile.options

skim:
	./skim.sh

all: train_bdt_sig_bg_mixed_fullData


ARGSdef="H:VerbosityLevel=Debug:NTrees=2000:BoostType=Grad:Shrinkage=0.1:!UseBaggedGrad:nCuts=2000:nEventsMin=100:NNodesMax=5:UseNvars=4:PruneStrength=5:PruneMethod=CostComplexity:MaxDepth=6"
ARGSmixed="H:VerbosityLevel=Debug:NTrees=200:BoostType=Grad:Shrinkage=0.1:nCuts=50:UseNvars=2:MaxDepth=2"
ARGSmixednew="H:VerbosityLevel=Debug:NTrees=200:BoostType=Grad:Shrinkage=0.4:nCuts=50:UseNvars=2:MaxDepth=2"

train_bdt_sig_bg:
	cp -R input/default input/bdt_sig_bg 
	python train.py input/bdt_sig_bg stpol_bdt_sig_bg $(ARGSdef) &> input/bdt_sig_bg/log

train_bdt_sig_bg_exclusive_only:
	cp -R input/exclusive_only input/bdt_sig_bg_exclusive_only 
	python train.py input/bdt_sig_bg_exclusive_only stpol_bdt_sig_bg_exclusive_only $(ARGSdef) &> input/bdt_sig_bg_exclusive_only/log

train_bdt_sig_bg_mixed:
	cp -R input/default input/bdt_sig_bg_mixed_new 
	python train_mixed.py input/bdt_sig_bg_mixed_new stpol_bdt_sig_bg_mixed_new $(ARGSmixednew) &> input/bdt_sig_bg_mixed_new/log

train_bdt_sig_bg_mixed_old:
	cp -R input/default input/bdt_sig_bg_mixed 
	python train_mixed.py input/bdt_sig_bg_mixed stpol_bdt_sig_bg_mixed $(ARGSmixed) &> input/bdt_sig_bg_mixed/log

train_bdt_sig_bg_mixed_reproc:
	cp -R input/default input/bdt_sig_bg_mixed_reproc 
	python train_mixed.py input/bdt_sig_bg_mixed_reproc stpol_bdt_sig_bg_mixed_reproc $(ARGSmixed) &> input/bdt_sig_bg_mixed_reproc/log
    echo "python train_mixed.py input/bdt_sig_bg_mixed_reproc stpol_bdt_sig_bg_mixed_reproc $(ARGSmixed) &> input/bdt_sig_bg_mixed_reproc/log"

train_bdt_sig_bg_mixed_deltaR:
	python train_mixed.py input/bdt_sig_bg_mixed_deltaR stpol_bdt_sig_bg_mixed_deltaR $(ARGSmixednew) &> input/bdt_sig_bg_mixed_deltaR/log
    echo "python train_mixed.py input/bdt_sig_bg_mixed_deltaR stpol_bdt_sig_bg_mixed_deltaR $(ARGSmixednew) &> input/bdt_sig_bg_mixed_deltaR/log"

train_bdt_sig_bg_mixed_fullData:
	python train_mixed.py input/bdt_sig_bg_mixed_fullData stpol_bdt_sig_bg_mixed_fullData $(ARGSmixednew) &> input/bdt_sig_bg_mixed_fullData/log
    echo "python train_mixed.py input/bdt_sig_bg_mixed_fullData stpol_bdt_sig_bg_mixed_fullData $(ARGSmixednew) &> input/bdt_sig_bg_mixed_fullData/log"

train_bdt_sig_bg_mixed_fullData_withC:
	python train_mixed.py input/bdt_sig_bg_mixed_fullData_withC stpol_bdt_sig_bg_mixed_fullData_withC $(ARGSmixednew) &> input/bdt_sig_bg_mixed_fullData_withC/log
    echo "python train_mixed.py input/bdt_sig_bg_mixed_fullData_withC stpol_bdt_sig_bg_mixed_fullData_withC $(ARGSmixednew) &> input/bdt_sig_bg_mixed_fullData_withC/log"

train_bdt_sig_bg_reproc:
	cp -R input/default/* input/bdt_sig_bg_reproc 
	python train.py input/bdt_sig_bg_reproc stpol_bdt_sig_bg_reproc $(ARGSdef) &> input/bdt_sig_bg_reproc/log
	echo "python train.py input/bdt_sig_bg_reproc stpol_bdt_sig_bg_reproc $(ARGSdef) &> input/bdt_sig_bg_reproc/log"

train_bdt_sig_bg_nomet:
	python train.py input/bdt_sig_bg_new stpol_bdt_sig_bg_nomet $(ARGSdef) &> input/bdt_sig_bg_new/log
	echo "python train.py input/bdt_sig_bg_new stpol_bdt_sig_bg_nomet $(ARGSdef) &> input/bdt_sig_bg_new/log"

train_bdt_sig_bg_dr_nomet:
	python train.py input/bdt_sig_bg_new_dr_lpt stpol_bdt_sig_bg_dr_nomet_lpt $(ARGSdef) &> input/bdt_sig_bg_new_dr_lpt/log
	echo "python train.py input/bdt_sig_bg_new_dr_lpt stpol_bdt_sig_bg_dr_nomet_lpt $(ARGSdef) &> input/bdt_sig_bg_new_dr_lpt/log"

train_bdt_sig_bg_dr_met:
	python train.py input/bdt_sig_bg_new_dr_met_lpt stpol_bdt_sig_bg_dr_met_lpt $(ARGSdef) &> input/bdt_sig_bg_new_dr_met_lpt/log
	echo "python train.py input/bdt_sig_bg_new_dr_met_lpt stpol_bdt_sig_bg_dr_met_lpt $(ARGSdef) &> input/bdt_sig_bg_new_dr_met_lpt/log"

train_bdt_sig_bg_dr_nomet_nolpt:
	python train.py input/bdt_sig_bg_new_dr stpol_bdt_sig_bg_dr_nomet_nolpt $(ARGSdef) &> input/bdt_sig_bg_new_dr/log
	echo "python train.py input/bdt_sig_bg_new_dr stpol_bdt_sig_bg_dr_nomet_nolpt $(ARGSdef) &> input/bdt_sig_bg_new_dr/log"

train_bdt_sig_bg_dr_met_nolpt:
	python train.py input/bdt_sig_bg_new_dr_met stpol_bdt_sig_bg_dr_met_nolpt $(ARGSdef) &> input/bdt_sig_bg_new_dr_met/log
	echo "python train.py input/bdt_sig_bg_new_dr_met stpol_bdt_sig_bg_dr_met_nolpt $(ARGSdef) &> input/bdt_sig_bg_new_dr_met/log"

evaluate:
	find ~/singletop/ntuples/nominal/ -name "*.root" | ~/parallel python adder.py bdt_sig_bg weights/stpol_bdt_sig_bg_lepton_flavour.weights.xml {}
	find ~/singletop/ntuples/nominal/ -name "*.root" | ~/parallel python adder.py bdt_sig_bg_A3 weights/stpol_bdt_sig_bg_ARGS3_lepton_flavour.weights.xml {}
	find ~/singletop/ntuples/nominal/ -name "*.root" | ~/parallel python adder.py bdt_sig_bg_mixed_A3 weights/stpol_bdt_sig_bg_mixed_ARGS3_lepton_flavour.weights.xml {}

print_statistics:
	echo "TTJets_SemiLept"
	cat input/default/bg.txt | grep "TTJets_SemiLept" | python list_entries.py
	echo "TTJets_FullLept"
	cat input/default/bg.txt | grep "TTJets_FullLept" | python list_entries.py
	echo "TTJets_MassiveBinDECAY"
	cat input/default/bg.txt | grep "TTJets_MassiveBinDECAY" | python list_entries.py
