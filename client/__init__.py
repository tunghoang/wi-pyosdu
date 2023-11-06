from .Http import httpGet
from .Token import auth_headers
from config import *
import json
def get_legals():
  resp = httpGet(f'{OSDU_BASE}/api/legal/v1/legaltags', headers=auth_headers())
  return json.loads(resp.content)['legalTags']
