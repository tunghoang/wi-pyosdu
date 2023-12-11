# -*- coding: utf-8 -*-
import json
from os import environ
from config import *
from client.Search import *

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--kind')
parser.add_argument('--query')
parser.add_argument('--returnedFields')
args = parser.parse_args()

if args.kind and args.query:
  returnedFields = args.returnedFields.split(',') if args.returnedFields else None
  print(json.dumps(search_query(args.kind, args.query, returnedFields=returnedFields)))
elif args.kind:
  returnedFields = args.returnedFields.split(',') if args.returnedFields else None
  search_kind(args.kind, returnedFields=returnedFields)
