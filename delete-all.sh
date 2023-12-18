#!/bin/bash
shopt -s expand_aliases
. .startenv

delete-welllog-dataset --dataset HT-1X.RAW
delete-welllog-dataset --dataset HT-1X.FINAL-LOGS

delete-welllog-dataset --dataset HT-2X.RAW
delete-welllog-dataset --dataset HT-2X.FINAL-LOGS

sleep 1
delete-wellbore --record_id osdu:master-data--Wellbore:HT-1X
delete-wellbore --record_id osdu:master-data--Wellbore:HT-2X

delete-seismic --horizon_id Blk052-053.ESS-H190-Line-Trace-X-Y-Time-ms
delete-seismic --fault_id Blk052-053.Stick-charisma
delete-seismic --trace_data_id Blk052-053.BDPOC-sub-cube

sleep 2
delete-seismic --bin_grid_id Blk052-053
