# -*- coding: utf-8 -*-
import json
from os import environ
from .config import *
from .client.Entitlement import *

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--info', action='store_true')
parser.add_argument('--add2group', action='store_true')
parser.add_argument('--user')
parser.add_argument('--group')
parser.add_argument('--list_groups', action='store_true')
parser.add_argument('--list_members', action='store_true')
parser.add_argument('--removefromgroup', action="store_true")
args = parser.parse_args()

if args.list_groups:
  print(json.dumps(entitlement_list_groups()))
elif args.info:
  entitlement_info()
elif args.list_members and args.group:
  print(json.dumps(entitlement_list_members(args.group)))
elif args.add2group and args.user and args.group:
  print(json.dumps(entitlement_add_to_group(args.user, args.group)))
elif args.removefromgroup and args.user and args.group:
  entitlement_remove_from_group(args.user, args.group)
