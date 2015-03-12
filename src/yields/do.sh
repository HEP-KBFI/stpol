#!/bin/bash

#julia yields.jl data_ele  /home/andres/single_top/stpol_pdf/src/step3/output/Jan27_fullData/iso/data/SingleEle/*.root
#julia yields.jl data_mu  /home/andres/single_top/stpol_pdf/src/step3/output/Jan27_fullData/iso/data/SingleMu/output*.root
#julia yields.jl tchan  /home/andres/single_top/stpol_pdf/src/step3/output/Jan27_fullData/iso/nominal/T*_t_ToLeptons/output*.root
#julia yields.jl ttjets /home/andres/single_top/stpol_pdf/src/step3/output/Jan27_fullData/iso/nominal/TTJets_*Lept/output*.root

julia yields.jl wjets /home/andres/single_top/stpol_pdf/src/step3/output/Jan27_fullData/iso/nominal/W*Jets_exclusive/output*.root
julia yields.jl diboson /home/andres/single_top/stpol_pdf/src/step3/output/Jan27_fullData/iso/nominal/WW/output*.root /home/andres/single_top/stpol_pdf/src/step3/output/Jan27_fullData/iso/nominal/WZ/output*.root /home/andres/single_top/stpol_pdf/src/step3/output/Jan27_fullData/iso/nominal/ZZ/output*.root
julia yields.jl dyjets /home/andres/single_top/stpol_pdf/src/step3/output/Jan27_fullData/iso/nominal/DYJets/output*.root
julia yields.jl twchan /home/andres/single_top/stpol_pdf/src/step3/output/Jan27_fullData/iso/nominal/T*_tW/output*.root
julia yields.jl schan /home/andres/single_top/stpol_pdf/src/step3/output/Jan27_fullData/iso/nominal/T*_s/output*.root
julia yields.jl qcd /home/andres/single_top/stpol_pdf/src/step3/output/Jan27_fullData/antiiso/data/Single*/output*.root

julia yields.jl QCD /home/andres/single_top/stpol_pdf/src/step3/output/Jan27_fullData/iso/nominal/QCD*/output*.root /home/andres/single_top/stpol_pdf/src/step3/output/Jan27_fullData/iso/nominal/GJets*/output*.root

