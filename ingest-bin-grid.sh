#!/bin/bash
shopt -s expand_aliases
. .startenv

ingest-seismic --path Seismic/NA_NA_Blk052-053.zip
sleep 3
