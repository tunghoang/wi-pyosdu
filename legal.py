# -*- coding: utf-8 -*-
import json
from os import environ
from config import *
from client.Legal import *

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--get_legaltags', action='store_true')
parser.add_argument('--create_legal', action='store_true')
parser.add_argument('--description')
parser.add_argument('--info', action='store_true')
args = parser.parse_args()

if args.get_legaltags:
  print(json.dumps(legal_get_legals()))
elif args.info:
  print(json.dumps(legal_info()))
elif args.create_legal:
  legal_create_legal('osdu-pvn-legal', 'legal for pvn prj', ['US', 'CA'])
