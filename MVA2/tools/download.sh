#!/bin/bash

function cmkdir { if [ ! -d $1 ]; then mkdir $1; fi }

REMOTE=cms.hep.kbfi.ee:/hdfs/local/stpol/step3/Jul26_MVA_multivar_withQCDMVA
LOCAL=../../../Jul26_MVA_multivar_withQCDMVA

cmkdir $LOCAL
cmkdir $LOCAL/mu
cmkdir $LOCAL/mu/data
cmkdir $LOCAL/mu/data/iso
cmkdir $LOCAL/mu/data/iso/Jul15
cmkdir $LOCAL/mu/data/antiiso
cmkdir $LOCAL/mu/data/antiiso/Jul15
cmkdir $LOCAL/mu/mc
cmkdir $LOCAL/mu/mc/iso
cmkdir $LOCAL/mu/mc/iso/nominal
cmkdir $LOCAL/mu/mc/iso/nominal/Jul15
cmkdir $LOCAL/mu/mc/antiiso
cmkdir $LOCAL/mu/mc/antiiso/nominal
cmkdir $LOCAL/mu/mc/antiiso/nominal/Jul15
cmkdir $LOCAL/ele
cmkdir $LOCAL/ele/data
cmkdir $LOCAL/ele/data/iso
cmkdir $LOCAL/ele/data/iso/Jul15
cmkdir $LOCAL/ele/data/antiiso
cmkdir $LOCAL/ele/data/antiiso/Jul15
cmkdir $LOCAL/ele/mc
cmkdir $LOCAL/ele/mc/iso
cmkdir $LOCAL/ele/mc/iso/nominal
cmkdir $LOCAL/ele/mc/iso/nominal/Jul15
cmkdir $LOCAL/ele/mc/antiiso
cmkdir $LOCAL/ele/mc/antiiso/nominal
cmkdir $LOCAL/ele/mc/antiiso/nominal/Jul15

rsync --progress $REMOTE/mu/data/iso/Jul15/* $LOCAL/mu/data/iso/Jul15
rsync --progress $REMOTE/mu/mc/iso/nominal/Jul15/* $LOCAL/mu/mc/iso/nominal/Jul15
rsync --progress $REMOTE/ele/data/iso/Jul15/* $LOCAL/ele/data/iso/Jul15
rsync --progress $REMOTE/ele/mc/iso/nominal/Jul15/* $LOCAL/ele/mc/iso/nominal/Jul15

rsync --progress $REMOTE/mu/data/antiiso/Jul15/* $LOCAL/mu/data/antiiso/Jul15
rsync --progress $REMOTE/mu/mc/antiiso/nominal/Jul15/* $LOCAL/mu/mc/antiiso/nominal/Jul15
rsync --progress $REMOTE/ele/data/antiiso/Jul15/* $LOCAL/ele/data/antiiso/Jul15
rsync --progress $REMOTE/ele/mc/antiiso/nominal/Jul15/* $LOCAL/ele/mc/antiiso/nominal/Jul15

