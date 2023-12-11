from .Token import access_token, auth_headers, auth_admin_headers
from config import *
from .Http import httpGet, httpPutJson, httpPostJson
from .File import file_get_upload_url, file_upload_file
from models.Record import Record
from models.FileGeneric import FileGeneric
import json

__STORAGE_BASE_URL = f'{OSDU_BASE}/api/storage/v2'
def storage_info():
  resp = httpGet(f'{__STORAGE_BASE_URL}/info', headers=auth_headers())
  data = json.loads(resp.content)
  return data
def get_kinds():
  resp = httpGet(f'{__STORAGE_BASE_URL}/query/kinds', headers=auth_headers())
  return json.loads(resp.content)

def get_record_versions(record_id):
  resp = httpGet(f'{__STORAGE_BASE_URL}/records/versions/{record_id}', headers=auth_headers())
  return json.loads(resp.content)

def get_record(record_id):
  resp = httpGet(f'{__STORAGE_BASE_URL}/records/{record_id}', headers=auth_headers())
  return json.loads(resp.content)

def storage_get_record(record_id):
  resp = httpGet(f'{__STORAGE_BASE_URL}/records/{record_id}', headers=auth_headers())
  return json.loads(resp.content)

def put_record(record: Record):
  resp = httpPutJson(f'{__STORAGE_BASE_URL}/records', json=[record.todict()], headers=auth_headers())
  return json.loads(resp.content)

def storage_put_record(record: Record):
  resp = httpPutJson(f'{__STORAGE_BASE_URL}/records', json=[record.todict()], headers=auth_headers())
  return json.loads(resp.content)

def storage_put_json(jsonFile):
  payload = json.load(jsonFile)
  if type(payload) != list:
    payload = [payload]
  resp = httpPutJson(f'{__STORAGE_BASE_URL}/records', json=payload, headers=auth_headers())
  return json.loads(resp.content)

def delete_record(record_id:str):
  resp = httpPostJson(f'{__STORAGE_BASE_URL}/records/delete', json=[record_id], headers=auth_headers())
  #resp = httpPostJson(f'{__STORAGE_BASE_URL}/records/delete', json=[record_id], headers=auth_admin_headers())
  print(resp.content)
  return resp.status_code

def storage_delete_record(record_id:str):
  resp = httpPostJson(f'{__STORAGE_BASE_URL}/records/delete', json=[record_id], headers=auth_headers())
  #resp = httpPostJson(f'{__STORAGE_BASE_URL}/records/delete', json=[record_id], headers=auth_admin_headers())
  print(resp.content)
  return resp.status_code

def storage_query_records(kind):
  #resp = httpGet(f'{__STORAGE_BASE_URL}/query/records?kind={kind}', headers=auth_headers())
  resp = httpGet(f'{__STORAGE_BASE_URL}/query/records?kind={kind}', headers=auth_admin_headers())
  print(resp.content)

def storage_put_file(local_file_path, filename):
  res_obj = file_get_upload_url()
  file_id = res_obj['FileID']
  file_source = res_obj['Location']['FileSource']
  signed_url = res_obj['Location']['SignedURL']

  file_upload_file(signed_url, local_file_path)

  file_record = FileGeneric(file_source, filename)
  ret = put_record(file_record)
  print(ret)
