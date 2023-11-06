from .Http import httpPostForm
from config import *
import json

def __login(username, password):
  resp = httpPostForm(TOKEN_FETCH_URL, data={
    "grant_type": "password",
    "scope": "openid profile email",
    "username": username,
    "password": password,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
  })
  content = json.loads(resp.content)
  OSDUSession.access_token = content['access_token']
  OSDUSession.set_refresh_token(content['refresh_token'])

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

def access_token():
  if OSDUSession.access_token is None:
    refresh_token = OSDUSession.get_refresh_token()
    if refresh_token is None:
      __login(USERNAME, PASSWORD)
    else:
      __renew_access_token(refresh_token)
  return OSDUSession.access_token

def refresh_token():
  if OSDUSession.refresh_token is None:
    __login(USERNAME, PASSWORD)
  return OSDUSession.refresh_token

def auth_headers():
  return {
    'data-partition-id': PARTITION_ID,
    'Authorization': f'Bearer {access_token()}'
  }
