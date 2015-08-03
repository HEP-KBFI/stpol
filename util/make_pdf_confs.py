import sys
import os
from subprocess import call

paths = {
    "DYJets": "/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/jpata-Sep8_newjec_metsystshift_hermeticproj-ddf5cfe2d986d6f8e7493e5e618fc544/USER",
    "TTJets_FullLept": "/TTJets_FullLeptMGDecays_8TeV-madgraph/jpata-Sep8_newjec_metsystshift_hermeticproj-b5f3018263c1ef499fcfff38dc3a7740/USER",
    "TTJets_SemiLept": "/TTJets_SemiLeptMGDecays_8TeV-madgraph/jpata-Sep8_newjec_metsystshift_hermeticproj-b5f3018263c1ef499fcfff38dc3a7740/USER",
    "T_s": "/T_s-channel_TuneZ2star_8TeV-powheg-tauola/jpata-Sep8_newjec_metsystshift_hermeticproj-ddf5cfe2d986d6f8e7493e5e618fc544/USER",
    "T_tW": "/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/jpata-Sep8_newjec_metsystshift_hermeticproj-ddf5cfe2d986d6f8e7493e5e618fc544/USER",
    "T_t_ToLeptons": "/TToLeptons_t-channel_8TeV-powheg-tauola/jpata-Sep8_newjec_metsystshift_hermeticproj-b5f3018263c1ef499fcfff38dc3a7740/USER",
    "Tbar_t_ToLeptons": "/TBarToLeptons_t-channel_8TeV-powheg-tauola/jpata-Sep8_newjec_metsystshift_hermeticproj-b5f3018263c1ef499fcfff38dc3a7740/USER",
    "Tbar_s": "/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/jpata-Sep8_newjec_metsystshift_hermeticproj-ddf5cfe2d986d6f8e7493e5e618fc544/USER",
    "Tbar_tW": "/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/jpata-Sep8_newjec_metsystshift_hermeticproj-ddf5cfe2d986d6f8e7493e5e618fc544/USER",
    "W1Jets_exclusive": "/W1JetsToLNu_TuneZ2Star_8TeV-madgraph/atiko-wjets_nominals_clear-bef8661838e52e144800069e7fe2aa7b/USER",
    "W2Jets_exclusive": "/W2JetsToLNu_TuneZ2Star_8TeV-madgraph/atiko-wjets_nominals_clear-bef8661838e52e144800069e7fe2aa7b/USER",
    "W3Jets_exclusive": "/W3JetsToLNu_TuneZ2Star_8TeV-madgraph/atiko-wjets_nominals_clear-bef8661838e52e144800069e7fe2aa7b/USER",
    "W4Jets_exclusive": "/W4JetsToLNu_TuneZ2Star_8TeV-madgraph/atiko-wjets_nominals_clear-bef8661838e52e144800069e7fe2aa7b/USER",
    "WW": "/WW_TuneZ2star_8TeV_pythia6_tauola/jpata-Sep8_newjec_metsystshift_hermeticproj-ddf5cfe2d986d6f8e7493e5e618fc544/USER",
    "WZ": "/WZ_TuneZ2star_8TeV_pythia6_tauola/jpata-Sep8_newjec_metsystshift_hermeticproj-ddf5cfe2d986d6f8e7493e5e618fc544/USER",
    "ZZ": "/ZZ_TuneZ2star_8TeV_pythia6_tauola/jpata-Sep8_newjec_metsystshift_hermeticproj-ddf5cfe2d986d6f8e7493e5e618fc544/USER"
}

pdfs = [
    "CT10",
    "mstw2008CPdeut",
    "nnpdf23_bestfit"
]

for pdf in pdfs:
    mydir = "/home/andres/single_top/stpol_pdf/crabs/pdf_final/pdfs_final_20_06_%s_slurm/" % pdf
    call(["mkdir", "-p", mydir])
    for dataset, dspath in paths.items():
        if "powheg" in dspath:
            massFix = "True"
        else:
            massFix = "False"

        bf_name = "%s/crab_%s.cfg" % (mydir, dataset)
        batch_outfile = open(bf_name, "w")
        batch_outfile.write("""[CMSSW]
lumis_per_job=200
total_number_of_lumis=-1
dbs_url=phys03
pset=/home/andres/single_top/stpol_pdf/src/step2/pdfweights_%s_cfg.py
pycfg_params=PowhegTopMassFix=%s
allow_nonproductioncmssw=1
get_edm_output=1
datasetpath=%s

[USER]
ui_working_dir=WD_%s
copy_data=1
user_remote_dir=stpol/pdfs_%s_20_06_final_slurm/%s
storage_element=T2_EE_Estonia
email=andres.tiko@cern.ch

[CRAB]
jobtype = cmssw
scheduler = slurm
use_server = 0

[PBSV2WITHSRM]
#forceTransferFiles = 1
workernodebase = /scratch/$USER
use_proxy = 1
queue=main""" % (pdf, massFix, dspath, dataset, pdf, dataset))
        batch_outfile.close()
                    



