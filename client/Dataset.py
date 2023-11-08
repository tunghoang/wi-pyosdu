from .Token import access_token, auth_headers
from config import *
from .Http import httpGet, httpPutJson, httpPostJson, httpPutFile
from models.Record import Record
from models.FileGeneric import FileGeneric
import json

__DATASET_BASE_URL = f'{OSDU_BASE}/api/dataset/v1'

def dataset_list():
  resp = httpGet(f'{__DATASET_BASE_URL}/getDatasetRegistry', headers=auth_headers())
  print(resp.status_code, resp.content)
def __upload_file(signed_url, local_file_path):
  resp = httpPutFile(signed_url, local_file_path)
  print(resp)
  
def dataset_upload_file(local_file_path):
  resp = httpGet(f'{__DATASET_BASE_URL}/getStorageInstructions', headers=auth_headers())
  print(resp.content)
  signed_url = json.loads(resp.content)['storageLocation']['signedUrl']
  __upload_file(signed_url, local_file_path)
