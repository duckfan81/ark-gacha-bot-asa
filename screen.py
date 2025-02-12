import numpy as np
import mss
import settings
import win32
import windows
import ctypes

def find_screen_size():
    rect = ctypes.wintypes.RECT()
    if ctypes.windll.user32.GetWindowRect(windows.hwnd, ctypes.byref(rect)):
        height = rect.bottom - rect.top
        print(f"using {height} as screen resolution ")
        return height
    
screen_resolution = find_screen_size()

if screen_resolution == 1080:
    mon = {"top": 0, "left": 0, "width": 1920, "height": 1080}
elif screen_resolution == 1440:
    mon = {"top": 0, "left": 0, "width": 2560, "height": 1440}
else:
    print("not a usable screensize")
    exit()

def get_screen_roi(start_x, start_y, width, height):

    region = {"top": start_y, "left": start_x, "width": width, "height": height}
    with mss.mss() as sct:
        screenshot = sct.grab(region)
        return np.array(screenshot)
    
if __name__ =="__main__":
    pass