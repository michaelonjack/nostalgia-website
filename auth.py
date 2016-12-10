#!/usr/bin/env python3

'''
	Here's how you go about authenticating yourself! The important thing to
	note here is that this script will be used in the other examples so
	set up a test user with API credentials and set them up in auth.ini.
'''
from imgurpython import ImgurClient
from helpers import get_input, get_config

def authenticate():
	# Get client ID, secret, and access and refresh tokens from auth.ini
	config = get_config()
	config.read('auth.ini')
	client_id = config.get('credentials', 'client_id')
	client_secret = config.get('credentials', 'client_secret')
	access_token = config.get('credentials', 'access_token')
	refresh_token = config.get('credentials', 'refresh_token')
	
	client = ImgurClient(client_id, client_secret)
	
	# ... redirect user to `authorization_url`, obtain pin (or code or token) ...
	client.set_user_auth(access_token, refresh_token)
 
	return client
	
	
	
# If you want to run this as a standalone script, so be it!
if __name__ == "__main__":
	authenticate()
	print 'success!\n'

	
