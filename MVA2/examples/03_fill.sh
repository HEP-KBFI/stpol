#/usr/bin/bash
fillertool=./../tools/filler.py

${fillertool} prepared/exele_mvaprep_ele.root prepared/ele/mc/iso/nominal/Jul15/* prepared/ele/data/iso/Jul15/*
${fillertool} prepared/exmu_mvaprep_mu.root   prepared/mu/mc/iso/nominal/Jul15/*  prepared/mu/data/iso/Jul15/*

#rm -Rf prepared/filled
#mkdir prepared/filled prepared/filled/ele prepared/filled/mu
#${fillertool} prepared/exele_mvaprep_ele.root prepared/ele/mc/iso/nominal/Jul15/* -oprepared/filled/ele
#${fillertool} prepared/exele_mvaprep_ele.root prepared/ele/data/iso/Jul15/* -oprepared/filled/ele
#${fillertool} prepared/exmu_mvaprep_mu.root prepared/mu/mc/iso/nominal/Jul15/* -oprepared/filled/mu
#${fillertool} prepared/exmu_mvaprep_mu.root prepared/mu/data/iso/Jul15/* -oprepared/filled/mu
