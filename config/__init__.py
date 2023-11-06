from os import environ
from dotenv import load_dotenv
load_dotenv()

OSDU_BASE = environ.get('OSDU_BASE')
TOKEN_FETCH_URL = f'{environ.get("AUTH_URL")}/realms/osdu/protocol/openid-connect/token'
CLIENT_ID = environ.get("CLIENT_ID")
CLIENT_SECRET = environ.get("CLIENT_SECRET")
USERNAME = environ.get("USERNAME")
PASSWORD = environ.get("PASSWORD")
PARTITION_ID = environ.get("PARTITION_ID")

class __Session:
  access_token = None
  refresh_token = None

  def set_refresh_token(self, rtoken):
    self.refresh_token = rtoken
    with open('.refresh_token', 'w') as f:
      f.write(rtoken)

  def get_refresh_token(self):
    if self.refresh_token is None:
      try:
        with open('.refresh_token', 'r') as f:
          self.refresh_token = f.read()
      except:
        return None
    return self.refresh_token

OSDUSession = __Session()
