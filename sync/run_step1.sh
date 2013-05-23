#!/bin/bash
echo "step1 sync"
echo "Inclusive sample"
cmsRun $STPOL_DIR/runconfs/step1_newCmdLine_cfg.py doSkimming=False inputFiles_load=$STPOL_DIR/sync/inclusive/files.txt outputFile=$STPOL_DIR/sync/inclusive/step1.root &> $STPOL_DIR/sync/inclusive/log_step1.txt
echo "Exclusive sample"
cmsRun $STPOL_DIR/runconfs/step1_newCmdLine_cfg.py doSkimming=False inputFiles_load=$STPOL_DIR/sync/exclusive/files.txt outputFile=$STPOL_DIR/sync/exclusive/step1.root &> $STPOL_DIR/sync/exclusive/log_step1.txt
echo "step1 done"
