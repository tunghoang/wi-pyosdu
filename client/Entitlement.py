from .Token import access_token, auth_headers, auth_admin_headers
from config import *
from .Http import *
import json

__ENTITLEMENT_BASE_URL = f'{OSDU_BASE}/api/entitlements/v2'
def entitlement_info():
  resp = httpGet(f'{__ENTITLEMENT_BASE_URL}/info', headers=auth_headers())
  print(resp.content.decode('utf-8'))

def entitlement_list_groups():
  resp = httpPostJson(f'{__ENTITLEMENT_BASE_URL}/groups', headers=auth_admin_headers())
  print(resp.content.decode('utf-8'))

