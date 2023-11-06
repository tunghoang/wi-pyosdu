from .Token import access_token, auth_headers
from config import *
from .Http import httpGet, httpPutJson, httpPostJson
from models.Record import Record
import json

__WBD_BASE_URL = f'{OSDU_BASE}/api/os-wellbore-ddms'
def wbd_info():
  resp = httpGet(f'{__WBD_BASE_URL}/about')
  return json.loads(resp.content)

def wbd_version():
  resp = httpGet(f'{__WBD_BASE_URL}/version', headers=auth_headers())
  return json.loads(resp.content)

def wbd_welllogs_data(record_id):
  resp = httpGet(f'{__WBD_BASE_URL}/ddms/v3/welllogs/{record_id}/data', headers=auth_headers())
  return json.loads(resp.content)

def wbd_create_wellbore(record):
  pass
