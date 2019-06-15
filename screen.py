
import platform
if platform.system() == 'Windows':
	from ctypes import windll

	user32 = windll.user32
	user32.SetProcessDPIAware() # prevents stretching
	width = user32.GetSystemMetrics(0)
	height = user32.GetSystemMetrics(1)

if platform.system() == 'Linux':
	width = 1920
	height = 1080
if platform.system() == 'Darwin':
	width = 1920
	height = 1080
