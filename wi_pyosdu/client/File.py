from .Token import access_token, auth_headers
from ..config import *
from .Http import *
from ..models.Record import Record
from ..models.FileGeneric import FileGeneric
import json

__FILE_BASE_URL = f'{OSDU_BASE}/api/file/v2'
def file_info():
  resp = httpGet(f'{__FILE_BASE_URL}/info', headers=auth_headers())
  print(resp.content.decode('utf-8'))

def __file_get_upload_url():
  resp = httpGet(f'{__FILE_BASE_URL}/files/uploadURL', headers=auth_headers())
  return json.loads(resp.content)

def file_get_upload_url():
  return __file_get_upload_url()

def __file_upload_file(signed_url, local_file_path):
  resp = httpPutFile(signed_url, local_file_path)
  print(resp.status_code, resp.content)

def file_upload_file(signed_url, local_file_path):
  __file_upload_file(signed_url, local_file_path)

def __file_add_metadata(filesource, filename):
  dataset = FileGeneric(filesource, filename)
  resp = httpPostJson(f'{__FILE_BASE_URL}/files/metadata', json=dataset.todict(), headers=auth_headers())
  print(resp.status_code, resp.content)
  resJson = resp.json()
  if 'id' in resJson:
    return resJson['id']
  raise Exception(f'Error: {resJson}')

def file_add_metadata(filesource, filename):
  return __file_add_metadata(filesource, filename) 

def file_ingest_file(filename, local_file_path):
  obj = __file_get_upload_url()
  file_id = obj['FileID']
  file_source = obj['Location']['FileSource']
  signed_url = obj['Location']['SignedURL']
  print(obj)
  __file_upload_file(signed_url, local_file_path)
  return __file_add_metadata(file_source, filename)

def file_delete_record(file_record_id):
  resp = httpDelete(f'{__FILE_BASE_URL}/files/{file_record_id}/metadata', headers=auth_headers())
  print(resp.status_code, resp.content)

def file_get_file_list():
  resp = httpPostJson(f'{__FILE_BASE_URL}/getFileList', json = {
    "TimeFrom": "2023-01-10T00:00:00.000Z",
    "TimeTo": "2024-12-01T00:00:00.000Z",
    "PageNum": 0,
    "Items": 100,
    "UserID": "app@pvn.vn"
  }, headers=auth_headers())
  return json.loads(resp.content)

def file_get_file_signed_url(srn):
  resp = httpPostJson(f'{__FILE_BASE_URL}/delivery/getFileSignedUrl', json = {
    "srns": [srn]  
  }, headers = auth_headers())
  return json.loads(resp.content)

def file_get_file(file_record_id):
  resp = httpGet(f'{__FILE_BASE_URL}/files/{file_record_id}/metadata', headers=auth_headers())
  resJson = resp.json()
  return resJson['data']['DatasetProperties']['FileSourceInfo']

def file_get_downloadURL(file_record_id):
  resp = httpGet(f'{__FILE_BASE_URL}/files/{file_record_id}/downloadURL', headers=auth_headers())
  return resp.json()

def file_download_file(file_record_id, output_file_name):
    downloadUrl = file_get_downloadURL(file_record_id)['SignedUrl']
    file_download(downloadUrl, output_file_name)

def file_download(url, outputFileName):
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(outputFileName, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
