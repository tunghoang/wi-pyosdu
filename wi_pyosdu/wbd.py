# -*- coding: utf-8 -*-
import json
from os import environ
from .config import *
from .client.WBD import *

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--info', action="store_true")
parser.add_argument('--welllog_data', action="store_true")
parser.add_argument('--welllog_id')
args = parser.parse_args()

if args.info:
  print(json.dumps(wbd_info()))
elif args.welllog_data and args.welllog_id:
  print(wbd_welllog_data(args.welllog_id))
