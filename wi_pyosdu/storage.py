# -*- coding: utf-8 -*-
import json
from os import environ
from .config import *
from .models.FileGeneric import FileGeneric
from .client.Storage import *


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--info', action="store_true")
parser.add_argument('--get_kinds', action="store_true")

parser.add_argument('--query', action="store_true")
parser.add_argument('--record_id')
parser.add_argument('--kind')

parser.add_argument('--delete', action="store_true")

# put json file
parser.add_argument('--put', action="store_true")
parser.add_argument('--path')
args = parser.parse_args()

if args.info:
  print(json.dumps(storage_info()))
elif args.get_kinds:
  print(json.dumps(get_kinds()))
elif args.query and args.record_id:
  print(json.dumps(storage_get_record(args.record_id)))
elif args.query and args.kind:
  print(json.dumps(storage_query_records(args.kind)))
elif args.delete and args.record_id:
  print(json.dumps(storage_delete_record(args.record_id)))
elif args.put and args.path:
  with open(args.path, 'r') as f:
    print(storage_put_json(f))
