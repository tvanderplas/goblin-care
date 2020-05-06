
from screeninfo import get_monitors

try:
    from ctypes import windll
    """prevents stretching on windows"""
    windll.user32.SetProcessDPIAware()
except:
    pass

width = get_monitors()[0].width
height = get_monitors()[0].height
