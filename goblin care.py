
from menu import Menu
import traceback as tb

if __name__ == '__main__':
	menu = Menu()
	try:
		menu.play()
	except Exception as error_:
		traceback_ = tb.format_list(tb.extract_tb(error_.__traceback__)) + [str(error_)]
		error_log = open('error.log', 'a')
		error_log.writelines(['\n\n'] + traceback_)
		error_log.close()
