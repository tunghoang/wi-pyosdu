# -*- coding: utf-8 -*-
import json
from os import environ
from config import *
from models.FileGeneric import FileGeneric
from client.Storage import *


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--info', action="store_true")
parser.add_argument('--get_kinds', action="store_true")

parser.add_argument('--query', action="store_true")
parser.add_argument('--record_id')

parser.add_argument('--delete', action="store_true")

args = parser.parse_args()

if args.info:
  print(json.dumps(storage_info()))
elif args.get_kinds:
  print(json.dumps(get_kinds()))
elif args.query and args.record_id:
  print(json.dumps(storage_get_record(args.record_id)))
elif args.delete and args.record_id:
  print(json.dumps(storage_delete_record(args.record_id)))
