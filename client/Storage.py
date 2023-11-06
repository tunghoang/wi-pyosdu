from .Token import access_token, auth_headers
from config import *
from .Http import httpGet, httpPutJson, httpPostJson
from models.Record import Record
import json

__STORAGE_BASE_URL = f'{OSDU_BASE}/api/storage/v2'
def get_kinds():
  resp = httpGet(f'{__STORAGE_BASE_URL}/query/kinds', headers=auth_headers())
  return json.loads(resp.content)['results']

def get_record_versions(record_id):
  resp = httpGet(f'{__STORAGE_BASE_URL}/records/versions/{record_id}', headers=auth_headers())
  return json.loads(resp.content)

def get_record(record_id):
  resp = httpGet(f'{__STORAGE_BASE_URL}/records/{record_id}', headers=auth_headers())
  return json.loads(resp.content)

def put_record(record: Record):
  resp = httpPutJson(f'{__STORAGE_BASE_URL}/records', json=[record.todict()], headers=auth_headers())
  return json.loads(resp.content)

def delete_record(record_id:str):
  resp = httpPostJson(f'{__STORAGE_BASE_URL}/records/delete', json=[record_id], headers=auth_headers())
  print(resp.content)
  return resp.status_code
