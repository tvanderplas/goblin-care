
import pygame as pg
from menu import Menu
import traceback as tb

pg.init() # pylint: disable=no-member

if __name__ == '__main__':
	menu = Menu()
	try:
		menu.play()
	except Exception as error_:
		traceback_ = tb.format_list(tb.extract_tb(error_.__traceback__)) + [str(error_)]
		error_log = open('error.log', 'w')
		error_log.write(''.join(traceback_))
		error_log.close()
