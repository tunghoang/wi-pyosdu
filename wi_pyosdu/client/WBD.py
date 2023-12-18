from .Token import access_token, auth_headers
from ..config import *
from .Http import httpGet, httpPutJson, httpPostJson, httpDelete
from .Search import *
from .File import *
from ..models.Record import Record
import json, io
from pandas import read_parquet

__WBD_BASE_URL = f'{OSDU_BASE}/api/os-wellbore-ddms'
def wbd_info():
  resp = httpGet(f'{__WBD_BASE_URL}/about')
  return json.loads(resp.content)

def wbd_version():
  resp = httpGet(f'{__WBD_BASE_URL}/version', headers=auth_headers())
  return json.loads(resp.content)

def wbd_welllog_data(record_id):
  resp = httpGet(f'{__WBD_BASE_URL}/ddms/v3/welllogs/{record_id}/data', headers=auth_headers())
  return read_parquet(io.BytesIO(resp.content))

def wbd_delete_welllog(welllog_id):
  result = search_query('osdu:wks:work-product-component--WellLog:*', f'id:"{welllog_id}"', returnedFields=['id', 'data.Datasets'])
  if result['totalCount'] == 0:
    print(f"No welllog found {welllog_id}")
    return
  print(result) 
  datasets = result['results'][0]['data']['Datasets']
  for ds in datasets:
    file_delete_record(ds[:-1])

  resp = httpDelete(f'{__WBD_BASE_URL}/ddms/v3/welllogs/{welllog_id}', headers=auth_headers())
  print(resp.content)
