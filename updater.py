
import requests

current_version = 'v0.3.0'
url = 'https://api.github.com/repos/tvanderplas/goblin-care/releases'
releases = requests.get(url)
print('releases -', releases.status_code)
latest = releases.json()[0]['tag_name']
if current_version == latest:
	print('Up to date')
else:
	print('Not up to date')
	release_id = str(releases.json()[0]['id'])
	asset_list_url = url + f'/{release_id}/assets'
	assets = requests.get(asset_list_url)
	print('assets -', assets.status_code)
	asset_id = str(assets.json()[0]['id'])
	download_url = url + f'/assets/{asset_id}'
	download = requests.get(download_url, headers={'Accept':'application/octet-stream'})
	print('download -', download.status_code)
	update_file = open('Goblin Care.zip', 'wb')
	update_file.write(download.content)
