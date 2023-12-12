from .Token import access_token, auth_headers, auth_admin_headers
from config import *
from .Http import *
import json

__ENTITLEMENT_BASE_URL = f'{OSDU_BASE}/api/entitlements/v2'
def entitlement_info():
  resp = httpGet(f'{__ENTITLEMENT_BASE_URL}/info', headers=auth_headers())
  print(resp.content.decode('utf-8'))

def entitlement_list_groups():
  headers = auth_admin_headers()
  resp = httpGet(f'{__ENTITLEMENT_BASE_URL}/groups', headers=headers)
  return resp.json()

def entitlement_list_members(group):
  resp = httpGet(f'{__ENTITLEMENT_BASE_URL}/groups/{group}/members', headers=auth_admin_headers())
  return resp.json()
  
def entitlement_add_to_group(user, group, owner=False):
  resp = httpPostJson(f'{__ENTITLEMENT_BASE_URL}/groups/{group}/members', headers=auth_admin_headers(), json = {
    'email': user,
    'role': 'OWNER' if owner else 'MEMBER'
  })
  return resp.json()

def entitlement_remove_from_group(user, group):
  resp = httpDelete(f'{__ENTITLEMENT_BASE_URL}/groups/{group}/members/{user}', headers=auth_admin_headers())
  print(resp.content.decode('utf-8'))
