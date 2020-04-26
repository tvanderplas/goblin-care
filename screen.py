
import os
from screeninfo import get_monitors

if os.name == "Windows":
    from ctypes import windll

    user32 = windll.user32
    user32.SetProcessDPIAware()
    """prevents stretching"""

width = get_monitors()[0].x
height = get_monitors()[0].y
