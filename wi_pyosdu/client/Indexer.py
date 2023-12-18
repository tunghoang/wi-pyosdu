from .Token import access_token, auth_headers, auth_admin_headers
from ..config import *
from .Http import *
import json

__INDEXER_BASE_URL = f'{OSDU_BASE}/api/indexer/v2'
def indexer_info():
  resp = httpGet(f'{__INDEXER_BASE_URL}/info', headers=auth_headers())
  print(resp.content.decode('utf-8'))

#def indexer_reindex_kind(kind, cursor):
#  #headers = auth_admin_headers()
#  headers = auth_headers()
#  resp = httpPostJson(f'{__INDEXER_BASE_URL}/reindex', json={
#    'kind': kind,
#    'cursor': cursor
#  },headers=headers)
#  print(resp.content.decode('utf-8'))
def indexer_reindex_kind(kind):
  #headers = auth_admin_headers()
  headers = auth_headers()
  resp = httpPostJson(f'{__INDEXER_BASE_URL}/reindex', json={
    'kind': kind
  },headers=headers)
  print(resp.content.decode('utf-8'))
