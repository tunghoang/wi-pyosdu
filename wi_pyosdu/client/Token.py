from .Http import httpPostForm
from ..config import *
import json
from .em_http_server import AuthEngine
import random
############ OIDC methods ###################
def __login(username, password):
  print(username, password, CLIENT_ID, CLIENT_SECRET)
  resp = httpPostForm(TOKEN_FETCH_URL, data={
    "grant_type": "password",
    "scope": "openid profile email",
    "username": username,
    "password": password,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
  })
  content = json.loads(resp.content)
  print(content)
  OSDUSession.access_token = content['access_token']
  OSDUSession.set_refresh_token(content['refresh_token'])

def __admin_login():
  resp = httpPostForm(TOKEN_FETCH_URL, data={
    "grant_type": "client_credentials",
    "scope": "openid profile email",
    "client_id": ADMIN_CLIENT_ID,
    "client_secret": ADMIN_CLIENT_SECRET
  })
  content = json.loads(resp.content)
  OSDUSession.set_admin_token(content['access_token'])

def __renew_access_token(refresh_token):
  resp = httpPostForm(TOKEN_FETCH_URL, data={
    "grant_type": "refresh_token",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "refresh_token": refresh_token
  })
  content = json.loads(resp.content)
  if content.get('access_token', None) is None:
    print("Error: ", content.get('error'))
    __login(USERNAME, PASSWORD)
  else:
    OSDUSession.access_token = content['access_token']

####### OAuth implementation ##############
def __oauth_authorize():
  auth_engine = AuthEngine.get_instance()
  auth_engine.loop()
 
########## Export methods #################
def access_token():
  if AUTH_METHOD == 'OIDC_LOGIN':
    if OSDUSession.access_token is None:
      refresh_token = OSDUSession.get_refresh_token()
      if refresh_token is None:
        __login(USERNAME, PASSWORD)
      else:
        __renew_access_token(refresh_token)
    return OSDUSession.access_token
  elif AUTH_METHOD == 'OAUTH2':
    if OSDUSession.get_oauth_token() is None:
      __oauth_authorize()
    return OSDUSession.access_token

def admin_token():
  if OSDUSession.admin_token is None:
    admin_token = OSDUSession.get_admin_token()
    if admin_token is None:
      __admin_login()
  return OSDUSession.admin_token

def refresh_token():
  if OSDUSession.refresh_token is None:
    __login(USERNAME, PASSWORD)
  return OSDUSession.refresh_token

def auth_headers():
  return {
    'data-partition-id': PARTITION_ID,
    'Authorization': f'Bearer {access_token()}'
  }

def auth_admin_headers():
  return {
    'data-partition-id': PARTITION_ID,
    'Authorization': f'Bearer {admin_token()}'
  }
