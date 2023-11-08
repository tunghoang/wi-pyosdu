# -*- coding: utf-8 -*-
import json
from os import environ
from config import *
from client.Search import *

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--kind')
parser.add_argument('--query')
args = parser.parse_args()

if args.kind:
  search_kind(args.kind)

elif args.query:
  search_query(args.query)
