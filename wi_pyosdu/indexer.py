# -*- coding: utf-8 -*-
import json
from os import environ
from .config import *
from .client.Indexer import *

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--info', action="store_true")
parser.add_argument('--reindex', action="store_true")
parser.add_argument('--kind')
parser.add_argument('--cursor')
args = parser.parse_args()

if args.info:
  indexer_info()
elif args.reindex and args.kind:
  indexer_reindex_kind(args.kind)
