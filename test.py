# -*- coding: utf-8 -*-
import json
from os import environ
from config import *
from client.Http import *

from client.Token import access_token
from client.Storage import get_kinds, get_record_versions, get_record, put_record, delete_record, storage_put_file, storage_query_records
from client.SeiStore import *
from client import get_legals
from client.WBD import *
from client.File import *
from client.Dataset import *

from models.Basin import Basin
from models.Well import Well
from models.Wellbore import Wellbore
from models.Organisation import Organisation

def basic_test():
  # BASIC TESTS

  for legal in get_legals():
    print("===========================")
    print(legal['name'])
    print(legal['description'])
    print(legal['properties'])

  print(get_kinds())
  print(get_record('osdu:wks:master-data--Well:HT-1P'))

def get_kinds_test():
  print(json.dumps(get_kinds()))

def basin_construction_test():
  # BASIN CONSTRUCTION TESTS
  basin = Basin('HaiThach', 'HT', r"Mỏ Hải Thạch")

  basinObj = basin.todict()
  print(type(basinObj), basinObj)
  return basin

def well_construction_test():
  well = Well("HT-2P", "HT_2P", "Hải Thạch 2P", basinId="HaiThach")
  print(well.todict())
  return well

def put_basin_test():
  record = basin_construction_test()
  print("\n", record.tojson())
  # PUT BASIN STORAGE SERVICE TEST
  result = put_record(record)
  print(result)

def delete_record_test():
  record_id = 'osdu:wks:master-data--Well:HT-1P'
  print(delete_record(record_id))

def put_well_test():
  well = well_construction_test()
  result = put_record(well)
  print(result)

def org_construction_test():
  org = Organisation('PVN', "PetroVietnam", "Tổng công ty Dầu khí Việt Nam")
  print(org.todict())
  return org

def put_org_test():
  record = org_construction_test()
  result = put_record(record)
  print(result)

def wellbore_construction_test():
  wellbore = Wellbore("HT-1P-1", "HT_1P_1", "Hải Thạch 1P Main hole")
  return wellbore

def put_wellbore_test():
  record = wellbore_construction_test()
  result = put_record(record)
  print(result)

def wellbore_ddms_test():
  print(wbd_info())
  print(wbd_version())

def seistore_basic_test():
  print(seistore_status())
  print(seistore_check_access())

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--basic_test', action="store_true")
parser.add_argument('--get_kinds_test', action="store_true")
parser.add_argument('--get_record')
parser.add_argument('--delete_record')
parser.add_argument('--put_org_test', action="store_true")
parser.add_argument('--put_well_test', action="store_true")
parser.add_argument('--put_basin_test', action="store_true")
parser.add_argument('--put_wellbore_test', action="store_true")
parser.add_argument("--wellbore_test", action="store_true")
parser.add_argument('--wellbore_ddms_welllogs_data')
parser.add_argument("--seistore_basic_test", action="store_true")
parser.add_argument("--file_get_file_signed_url")
parser.add_argument("--file_ingest_file")
parser.add_argument("--dataset_list_test", action="store_true")
parser.add_argument("--dataset_upload_file")
parser.add_argument("--storage_put_file")
parser.add_argument("--storage_query_records")

args = parser.parse_args()
if args.basic_test:
  basic_test()
elif args.get_kinds_test:
  get_kinds_test()
elif args.get_record:
  record = get_record(args.get_record)
  print(json.dumps(record))
elif args.delete_record:
  print(delete_record(args.delete_record))
elif args.put_org_test:
  print(put_org_test())
elif args.put_basin_test:
  put_basin_test()
elif args.put_well_test:
  put_well_test()
elif args.put_wellbore_test:
  put_wellbore_test()
elif args.wellbore_test:
  wellbore_ddms_test()
elif args.wellbore_ddms_welllogs_data:
  print(wellbore_ddms_welllogs_data(args.wellbore_ddms_welllogs_data))
elif args.seistore_basic_test:
  seistore_basic_test()
elif args.file_get_file_signed_url:
  print(file_get_file_signed_url(args.file_get_file_signed_url))
elif args.file_ingest_file:
  file_ingest_file(args.file_ingest_file)
elif args.dataset_list_test:
  dataset_list()
elif args.dataset_upload_file:
  dataset_upload_file(args.dataset_upload_file)
elif args.storage_put_file:
  storage_put_file(args.storage_put_file, 'samplefile')
elif args.storage_query_records:
  kind = args.storage_query_records
  storage_query_records(kind)

#delete_record_test()
#basic_test()
#put_org_test()
