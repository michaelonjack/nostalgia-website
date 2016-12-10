from imgurpython import ImgurClient
import urllib2
from json import load

album = 'pQMg2'

def get_input(string):
	''' Get input from console regardless of python 2 or 3 '''
	try:
		return raw_input(string)
	except:
		return input(string)

def get_config():
	''' Create a config parser for reading INI files '''
	try:
		import ConfigParser
		return ConfigParser.ConfigParser()
	except:
		import configparser
		return configparser.ConfigParser()

def authenticate(client_id,client_secret):
	# Get client ID and secret from auth.ini
	#config = get_config()
	#config.read('auth.ini')
	#client_id = config.get('credentials', 'client_id')
	#client_secret = config.get('credentials', 'client_secret')
	
	client = ImgurClient(client_id, client_secret)

	# Authorization flow, pin example (see docs for other auth types)
	authorization_url = client.get_auth_url('pin')

	print("Go to the following URL: {0}".format(authorization_url))

	# Read in the pin, handle Python 2 or 3 here.
	pin = get_input("Enter pin code: ")
	
	# ... redirect user to `authorization_url`, obtain pin (or code or token) ...
	credentials = client.authorize(pin, 'pin')
	client.set_user_auth(credentials['access_token'], credentials['refresh_token'])

	print("Authentication successful! Here are the details:")
	print(" Access token: {0}".format(credentials['access_token']))
	print(" Refresh token: {0}".format(credentials['refresh_token']))

	return client

def upload_to_imgur(client,url):
	config = {
		'album': album,
		'name': 'Dankey Kang',
		'title': 'Dankey Kang',
		'description': 'Did this honestly work?'
	}
	
	print("Uploading image..")
	image = client.upload_from_url(url,config=config,anon=False)
	print("done.")
	
	return image
	
if __name__ == "__main__":
	client_id="d67e71100199547"
	client_secret="1e07c0aef31debbd6228a23344c26cb9c536790b"
	
	request = urllib2.Request('https://api.imgur.com/3/album/pQMg2')
	request.add_header('Authorization','Client-ID d67e71100199547')
	response = urllib2.urlopen(request)
	json_obj = load(response)
	for image in json_obj['data']['images']:
		print image['link']
	



