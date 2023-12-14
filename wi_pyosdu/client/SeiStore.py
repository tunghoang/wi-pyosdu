from .Token import access_token, auth_headers
from ..config import *
from .Http import httpGet, httpPutJson, httpPostJson
from ..models.Record import Record
import json

__SEISTORE_BASE_URL = f'{OSDU_BASE}/api/seismic-store/v3'
def seistore_status():
  resp = httpGet(f'{__SEISTORE_BASE_URL}/svcstatus', headers=auth_headers())
  return resp.content

def seistore_check_access():
  resp = httpGet(f'{__SEISTORE_BASE_URL}/svcstatus/access', headers=auth_headers())
  return resp.content
