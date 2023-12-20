#!/bin/bash
shopt -s expand_aliases
. .startenv

ingest-welllog --path "Welllogs/NA_05-2_HAI THACH_HT-1X_RAW_RAW.las"
sleep 20
ingest-welllog --path "Welllogs/NA_05-2_HAI THACH_HT-1X_FINAL LOGS_INTERPRETATION.las"
sleep 20

ingest-welllog --path "Welllogs/NA_05-2_HAI THACH_HT-2X_RAW_RAW.las"
sleep 20
ingest-welllog --path "Welllogs/NA_05-2_HAI THACH_HT-2X_FINAL LOGS_INTERPRETATION.las"
sleep 20
