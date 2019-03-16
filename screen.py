
import tkinter
from ctypes import windll

windll.user32.SetProcessDPIAware()
"""prevents stretching"""

root = tkinter.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
