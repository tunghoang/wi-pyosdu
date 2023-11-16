from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from threading import Thread
from requests_oauthlib import OAuth2Session
from config import *
import time
import traceback

class _RequestHandler(BaseHTTPRequestHandler):
  def __send_error(self, code, message, data):
    self.send_response(code, message=message)
    self.end_headers()
    if data:
      self.wfile.write(bytes(data, 'utf8'))
    AuthEngine.get_instance().stop = True

  def __send_success(self):
    self.send_response(200, message="OK")
    self.end_headers()
    self.wfile.write(bytes("Hello world", 'utf8'))
    AuthEngine.get_instance().stop = True
    
  def do_GET(self):
    print(self.path)
    self.protocol_version = "HTTP/1.1"
    qs_start = self.path.find("?")
    if qs_start > 0:
      params = parse_qs(self.path[qs_start + 1:])
      if 'code' in params:
        oauth_client = OAuth2Session(CLIENT_ID, state = OSDUSession.state)
        try:
          token = oauth_client.fetch_token(TOKEN_FETCH_URL, client_secret=CLIENT_SECRET, authorization_response=self.path)
          OSDUSession.set_oauth_token(token['access_token'])
          OSDUSession.set_refresh_token(token['refresh_token'])
          self.__send_success()
        except Exception as e:
          traceback.print_exc()
          self.__send_error(403, "Error", f"{params}")
      else:
        self.__send_error(403, "Forbidden", f"{params}")
    else:
      self.__send_error(403, "Forbidden")

class AuthEngine:
  instance = None

  def __init__(self):
    self.stop = False
    self.oauth_state = None
    self.httpd = HTTPServer(("", 7000), _RequestHandler)

  def loop(self):
    oauth_client = OAuth2Session(CLIENT_ID)
    auth_url, state = oauth_client.authorization_url(OAUTH_BASE_URL)
    print(auth_url)
    OSDUSession.state = state
    server_thread = Thread(target = self.httpd.serve_forever)
    server_thread.start()
    while not AuthEngine.get_instance().stop:
      time.sleep(0.1)
    self.httpd.shutdown()
    server_thread.join()

  @staticmethod
  def get_instance():
    if AuthEngine.instance == None:
      AuthEngine.instance = AuthEngine()
    return AuthEngine.instance
