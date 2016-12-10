from auth import authenticate
from imgurpython import ImgurClient

def transfer_to_imgur(category,links):
	access_token = 'bcd470555cdaaaa6f7f09f3cdad53707859652d8'
	refresh_token = 'f076999c5f9f3f74bec325218953a771e8596438'
	client = authenticate(access_token, refresh_token)
	
	for link in links: 
		
		album = imgur_album_dict[category]
		config = {
			'album': album,
			'name': category,
			'title': category,
			'description': 'From ' + link 
		}
		
		image = client.upload_from_url(link, config=config, anon=False)
		print('...')

imgur_album_dict = {
		"general":"ebt94",
		"games":"r5DjN",
		"ads":"NGfeo",
		"technology":"JK4Zf",
		"television":"eAsZW",
		"movies":"Q5TNS" }

if __name__ == '__main__':
	links = [line.strip() for line in open('links.txt')]
	print('Uploading...')
	transfer_to_imgur('television',links)
	print('Done.')
	
