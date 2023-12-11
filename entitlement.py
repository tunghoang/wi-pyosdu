# -*- coding: utf-8 -*-
import json
from os import environ
from config import *
from client.Entitlement import *

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--info', action='store_true')
parser.add_argument('--add2group', action='store_true')
parser.add_argument('--user')
parser.add_argument('--group')
parser.add_argument('--list_groups', action='store_true')
args = parser.parse_args()

if args.list_groups:
  print(json.dumps(entitlement_list_groups()))
elif args.info:
  entitlement_info()
