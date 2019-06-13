
import pygame as pg
from menu import Menu

pg.init() # pylint: disable=no-member

if __name__ == '__main__':
	menu = Menu()
	menu.play()
