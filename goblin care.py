
import pygame as pg
from menu import Menu
import requests

current_version = 'v0.3.0'
url = 'https://api.github.com/repos/tvanderplas/goblin-care/releases'
r = requests.get(url)
latest = r.json()[0]['tag_name']
if current_version is latest:
	print('Up to date')
else:
	print('Not up to date')

pg.init() # pylint: disable=no-member

if __name__ == '__main__':
	menu = Menu()
	menu.play()
