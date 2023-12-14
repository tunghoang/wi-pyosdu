from .Token import access_token, auth_headers
from ..config import *
from .Http import *
from ..models.Record import Record
import json

__CRS_CATALOG_BASE_URL = f'{OSDU_BASE}/api/crs/catalog/v2'
def crs_catalog_info():
  resp = httpGet(f'{__CRS_CATALOG_BASE_URL}/info', headers=auth_headers())
  print(resp.content.decode('utf-8'))

def crs_catalog_get_crs():
  resp = httpGet(f'{__CRS_CATALOG_BASE_URL}/coordinate-reference-system',headers=auth_headers())
  print(resp.content.decode('utf-8'))
