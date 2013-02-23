'''
This is a very rudimentary (and manual) example for using OAuth 2.0 
with Google APIs.

Google offers an OAuth 2.0 client module for python:
        https://developers.google.com/api-client-library/python/guide/aaa_oauth
'''
from oauth2client.client import OAuth2WebServerFlow
import json
import requests
from pprint import pprint

# Load configuration data.
# Items in the configuration are obtained from the Google Apps admin dashboard.
# The redirect_uri should be a real callback URL for the web application using
# the Google API.
with open('config.json') as fh:
    config = json.load(fh)

# Create a "flow" object, which is normall used troughout the handshake.
flow = OAuth2WebServerFlow(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            scope=config['scope'],
            redirect_uri=config['redirect_uri'])

# Obtain the authorization URI, used for obtaining a code.
auth_uri = flow.step1_get_authorize_url()            
print 'Go to this URL, copy the "code" value from the resulting URL\'s query string:\n%s\n' % auth_uri

# Manually obtain the code, since the redirect_uri in the config is bogus.
code = raw_input('Paste the "code" value:\n')

'''
The code in this comment block results in an SSL error.
Giving up on the oauth2client as a consequence.

credentials = flow.step2_exchange(code)
print credentials
http = httplib2.Http()
http = credentials.authorize(http)
'''

# Manually perform the POST in lieu of using oauth2client. 
params = {
    'code'          : code,
    'client_id'     : config['client_id'],
    'client_secret' : config['client_secret'],
    'redirect_uri'  : config['redirect_uri'],
    'grant_type'    : 'authorization_code'
}

# Use the "code" value with credentials to obtain an access_token for the user.
url = 'https://accounts.google.com/o/oauth2/token'
resp = requests.post(url, data=params)
result = json.loads(resp.text)
access_token = result['access_token']

# Call REST endpoints with this acess_taken in the query string for payload.
url = config['scope'] + '?%s=%s' % ('access_token', access_token)
resp = requests.get(url)
print '\nresult:\n%s' % resp.text
