#!/bin/bash
shopt -s expand_aliases
. .startenv

_BASE=/home/jovyan/workspace/data/mntwin/seismic

export-seismic --bin_grid_id Blk052-053 --outdir $_BASE
export-seismic --trace_data_id Blk052-053.BDPOC-sub-cube --outdir $_BASE

export-seismic --fault_id Blk052-053.Stick-charisma --outdir $_BASE
export-seismic --horizon_id Blk052-053.ESS-H190-Line-Trace-X-Y-Time-ms --outdir $_BASE
