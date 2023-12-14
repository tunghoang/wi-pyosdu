import json
from .Token import access_token, auth_headers, auth_admin_headers
from ..config import *
from .Http import *

__LEGAL_BASE_URL = f'{OSDU_BASE}/api/legal/v1'
def legal_info():
  resp = httpGet(f'{__LEGAL_BASE_URL}/info')
  return resp.json()

def legal_get_legals():
  resp = httpGet(f'{__LEGAL_BASE_URL}/legaltags', headers=auth_admin_headers())
  response_data = resp.json()
  #print(response_data)
  return response_data['legalTags']
  #return json.loads(resp.content)['legalTags']

def legal_create_legal(name, desc, countryOfOrigin):
  resp = httpPostJson(f'{__LEGAL_BASE_URL}/legaltags', headers=auth_admin_headers(), json={
    'name': name,
    'description': desc,
    'properties': {
      'contractId': "PVN12345",
      'countryOfOrigin': countryOfOrigin,
      "exportClassification": "EAR99",
      'dataType': 'Third party data',
      'originator': 'AGS',
      'personalData': 'No personal data',
      'expirationDate': '2030-12-31',
      'securityClassification': 'Private'
    }
  })
  response_data = resp.json()
  print(response_data)
