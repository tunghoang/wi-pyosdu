from .Token import access_token, auth_headers
from config import *
from .Http import *
import json

__SEARCH_BASE_URL = f'{OSDU_BASE}/api/search/v2'
def search_info():
  resp = httpGet(f'{__SEARCH_BASE_URL}/info', headers=auth_headers())
  print(resp.content.decode('utf-8'))

def search_kind(kind):
  resp = httpPostJson(f'{__SEARCH_BASE_URL}/query', json={
    'kind': kind
  },headers=auth_headers())
  print(resp.content.decode('utf-8'))

def search_query(text):
  resp = httpPostJson(f'{__SEARCH_BASE_URL}/query', json={'query': text}, headers=auth_headers())
  print(resp.content)
