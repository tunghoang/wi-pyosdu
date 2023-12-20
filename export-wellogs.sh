#!/bin/bash
shopt -s expand_aliases
. .startenv

_BASE=/home/jovyan/workspace/data/mntwin/welllogs
#_BASE=output/welllogs

export-welllog-dataset --dataset HT-1X.RAW --out_file $_BASE/HT-1X.RAW.las
export-welllog-dataset --dataset HT-1X.FINAL-LOGS --out_file $_BASE/HT-1X.FINAL-LOGS.las

export-welllog-dataset --dataset HT-2X.RAW --out_file $_BASE/HT-2X.RAW.las
export-welllog-dataset --dataset HT-2X.FINAL-LOGS --out_file $_BASE/HT-2X.FINAL-LOGS.las
