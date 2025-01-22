import numpy as np
import mss
import settings

if settings.screen_resolution == 1080:
    mon = {"top": 0, "left": 0, "width": 1920, "height": 1080}
elif settings.screen_resolution == 1440:
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