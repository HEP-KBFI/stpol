#!/bin/bash
for i in WD*
do
    crab -c $i -clean
done
