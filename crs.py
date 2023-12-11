# -*- coding: utf-8 -*-
import json
from os import environ
from config import *
from client.CRSCatalog import *


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--info', action="store_true")
parser.add_argument('--get_crs', action="store_true")

args = parser.parse_args()

if args.info:
  print(crs_catalog_info())
elif args.get_crs:
  print(crs_catalog_get_crs())
