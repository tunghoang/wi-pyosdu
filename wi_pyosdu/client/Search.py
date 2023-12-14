from .Token import access_token, auth_headers
from ..config import *
from .Http import *
import json

__SEARCH_BASE_URL = f'{OSDU_BASE}/api/search/v2'
def search_info():
  resp = httpGet(f'{__SEARCH_BASE_URL}/info', headers=auth_headers())
  print(resp.content.decode('utf-8'))

def search_kind(kind, returnedFields=None, limit=1000):
  resp = httpPostJson(f'{__SEARCH_BASE_URL}/query', json={
    'kind': kind,
    'returnedFields': returnedFields,
    'limit': limit
  },headers=auth_headers())
  print(resp.content.decode('utf-8'))

def search_query(kind, text, returnedFields=None, limit=1000):
  payload = {
    'kind': kind,
    'query': text,
    'returnedFields': returnedFields,
    'limit': limit
  }
  resp = httpPostJson(f'{__SEARCH_BASE_URL}/query', json=payload, headers=auth_headers())
  return json.loads(resp.content)
