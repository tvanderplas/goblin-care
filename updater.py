
from ctypes import windll
import requests
import zipfile as zf
from subprocess import Popen

connect_error_title = "Goblin Care"
connect_error_message = "Unable to connect to update server. Please check internet and firewall settings."
url = 'https://api.github.com/repos/tvanderplas/goblin-care/releases'

def get_current_version():
	try:
		print('Checking for game installation...')
		version_info = open('version.txt', 'r')
	except FileNotFoundError:
		print('No installation found')
		version_info = open('version.txt', 'w')
		version_info.close()
		current_version = ''
	else:
		current_version = version_info.readline()
		version_info.close()
	return current_version

def check_latest_version(success):
	try:
		print('Connecting to update server...')
		releases = requests.get(url)
	except:
		success = False

	if success and (releases.status_code == 200):
		latest_version = releases.json()[0]['tag_name']
		release_id = str(releases.json()[0]['id'])
	else:
		latest_version = None
		release_id = None
		success = False
	return latest_version, release_id, success

def get_latest_version(success, release_id):
	asset_list_url = url + f'/{release_id}/assets'
	assets = requests.get(asset_list_url)
	if assets.status_code == 200:
		asset_id = str(assets.json()[0]['id'])
		download_url = url + f'/assets/{asset_id}'
		download = requests.get(download_url, headers={'Accept':'application/octet-stream'})
		if success and (download.status_code == 200):
			zip_filename = f'Goblin Care {latest}.zip'
			folder_name = f'Goblin Care {latest}'
			update_file = open(zip_filename, 'wb')
			update_file.write(download.content)
			with zf.ZipFile(zip_filename) as zip:
				zip.extractall(folder_name)
		else:
			success = False
	else:
		success = False
	return success

def change_version_info(latest):
	version_info = open('version.txt', 'w')
	version_info.writelines(latest)
	version_info.close()

current_version = get_current_version()
success = True
latest, release_id, success = check_latest_version(success)
if success:
	if (current_version == latest):
		print('Up to date')
	else:
		print('Not up to date')
		success = get_latest_version(success, release_id)
if success:
	change_version_info(latest)
	current_version = latest
else:
	windll.user32.MessageBoxW(0, connect_error_message, connect_error_title, 0)

command = f'"Goblin Care {current_version}/Goblin Care/goblin care.exe"'
Popen(command)
