# -*- coding: utf-8 -*-
import json
from os import environ
from config import *
from models.FileGeneric import FileGeneric
from client.File import *

def info():
  file_info()

def get_file_list_test():
  print(json.dumps(file_get_file_list()))

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--info', action="store_true")
parser.add_argument("--file_list", action="store_true")

parser.add_argument("--metadata", action="store_true")
parser.add_argument('--filesource')
parser.add_argument('--filename')

parser.add_argument("--delete", action="store_true")
parser.add_argument("--record_id")

parser.add_argument("--ingest", action="store_true")
parser.add_argument("--local_path")
#parser.add_argument("--filename") Already have it

args = parser.parse_args()

if args.info:
  info()
elif args.file_list:
  get_file_list_test()
elif args.metadata and args.filesource and args.filename:
  file_add_metadata(args.filesource, args.filename)
elif args.delete and args.record_id:
  file_delete_record(args.record_id)

elif args.ingest and args.local_path and args.filename:
  file_ingest_file(args.filename, args.local_path)
