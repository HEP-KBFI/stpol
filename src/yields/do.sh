#!/bin/bash

julia yields.jl data_ele  /home/andres/single_top/stpol_pdf/src/step3/output/May30_deltaRs/iso/data/SingleEle/*.root
julia yields.jl data_mu  /home/andres/single_top/stpol_pdf/src/step3/output/May30_deltaRs/iso/data/SingleMu/output*.root
julia yields.jl tchan  /home/andres/single_top/stpol_pdf/src/step3/output/May30_deltaRs/iso/nominal/T*_t_ToLeptons/output*.root
julia yields.jl ttjets /home/andres/single_top/stpol_pdf/src/step3/output/May30_deltaRs/iso/nominal/TTJets_*Lept/output*.root

julia yields.jl wjets /home/andres/single_top/stpol_pdf/src/step3/output/May30_deltaRs/iso/nominal/W*Jets_exclusive/output*.root
julia yields.jl diboson /home/andres/single_top/stpol_pdf/src/step3/output/May30_deltaRs/iso/nominal/WW/output*.root /home/andres/single_top/stpol_pdf/src/step3/output/May30_deltaRs/iso/nominal/WZ/output*.root /home/andres/single_top/stpol_pdf/src/step3/output/May30_deltaRs/iso/nominal/ZZ/output*.root
julia yields.jl dyjets /home/andres/single_top/stpol_pdf/src/step3/output/May30_deltaRs/iso/nominal/DYJets/output*.root
julia yields.jl twchan /home/andres/single_top/stpol_pdf/src/step3/output/May30_deltaRs/iso/nominal/T*_tW/output*.root
julia yields.jl schan /home/andres/single_top/stpol_pdf/src/step3/output/May30_deltaRs/iso/nominal/T*_s/output*.root
julia yields.jl qcd /home/andres/single_top/stpol_pdf/src/step3/output/May30_deltaRs/antiiso/data/Single*/output*.root

julia yields.jl QCD /home/andres/single_top/stpol_pdf/src/step3/output/May30_deltaRs/iso/nominal/QCD*/output*.root /home/andres/single_top/stpol_pdf/src/step3/output/May30_deltaRs/iso/nominal/GJets*/output*.root

