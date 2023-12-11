from .Http import httpGet
from .Token import auth_headers, auth_admin_headers
from config import *
import json
def get_legals():
  resp = httpGet(f'{OSDU_BASE}/api/legal/v1/legaltags', headers=auth_admin_headers())
  print(f'{OSDU_BASE}/api/legal/v1/legaltags')
  print(resp.content)
  return json.loads(resp.content)['legalTags']
