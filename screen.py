
from ctypes import windll

user32 = windll.user32
user32.SetProcessDPIAware()
"""prevents stretching"""

width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1)
