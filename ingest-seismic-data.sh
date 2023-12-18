#!/bin/bash
shopt -s expand_aliases
. .startenv

ingest-seismic --path Seismic/NA_NA_Blk052-053_ESS-H190-Line-Trace-X-Y-Time-ms_Horizon.dat
ingest-seismic --path Seismic/NA_NA_Blk052-053_Stick-charisma_Fault.dat
ingest-seismic --path Seismic/NA_NA_Blk052-053_BDPOC-sub-cube.sgy
