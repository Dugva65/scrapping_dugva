import base64
import binascii
import webbrowser
import requests
import os
import urllib.parse

from http.server import HTTPServer, BaseHTTPRequestHandler
from commons import *

state = binascii.hexlify(os.urandom(20)).decode('utf-8')
code = None

class RequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		global code
		self.close_connection = True
		query = urllib.parse.parse_qs (urllib.parse.urlparse(self.path).query)
		if not query['state'] or query['state'][0] != state:
			raise RuntimeError('state argument missing or invalid')
		code = query['code']

def generate_code_authorize_spotify_api():
  params_oauth_url = {
    'client_id': clientID,
    'redirect_uri': redirect_uri,
    'response_type': 'code',
    'scope': ' '.join(scope),
    'state': state
  }

  response = requests.get(auth_url, params=params_oauth_url)

  webbrowser.open_new_tab(response.url)
  server = HTTPServer(('localhost', 8080), RequestHandler)
  server.handle_request()


def generate_access_token():
  data = {
	  'grant_type': "authorization_code",
	  'code': code,
	  'redirect_uri': redirect_uri
  }

  message = f"{clientID}:{clientSecret}"
  message_bytes = message.encode('ascii')
  base64_bytes = base64.b64encode(message_bytes)
  base64_message = base64_bytes.decode('ascii')

  headers = {
    "Accept": "application/json",
    "Content-type": "application/x-www-form-urlencoded",
    "Authorization": f"Basic {base64_message}"
  }

  response = requests.post(auth_url_token, data=data, headers=headers)
  response_json = response.json()
  return response_json["access_token"]
