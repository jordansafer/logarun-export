#!/usr/bin/env python

"""
Strava Development Sandbox.

Get your *Client ID* and *Client Secret* from https://www.strava.com/settings/api

Usage:
  strava_local_client.py get_write_token <client_id> <client_secret> [options]
  strava_local_client.py find_settings

Options:
  -h --help      Show this screen.
  --port=<port>  Local port for OAuth client [default: 8000].
"""

import stravalib
from flask import Flask, request

app = Flask(__name__)

API_CLIENT = stravalib.Client()

# set these in __main__
CLIENT_ID = None
CLIENT_SECRET = None

@app.route("/auth")
def auth_callback():
    code = request.args.get('code')
    access_token = API_CLIENT.exchange_code_for_token(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        code=code
        )
    with open("strava_access.txt","w+") as f:
        f.write(access_token)
    print(access_token)
    return "Strava access granted"


def getToken(client_id, client_secret):
    import subprocess
    import sys

    CLIENT_ID, CLIENT_SECRET = client_id, client_secret
    auth_url = API_CLIENT.authorization_url(
        client_id=args['<client_id>'],
        redirect_uri='http://127.0.0.1:{port}/auth'.format(port=args['--port']),
        scope='activity:write',
        state='from_cli'
        )
    if sys.platform == 'darwin':
        print('On OS X - launching {0} at default browser'.format(auth_url))
        subprocess.call(['open', auth_url])
    else:
        print('Go to {0} to authorize access: '.format(auth_url))
    app.run(port=int(args['--port']))
