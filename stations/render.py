import pyautogui
import template 
import variables
import time
import windows
import utils
import settings
import local_player


global render_flag
render_flag = False #starts as false as obviously we are not rendering anything

def enter_tekpod():
    global render_flag
    time.sleep(1)
    utils.zero()
    utils.set_yaw(settings.station_yaw)
    time.sleep(1)
    pyautogui.keyDown(local_player.get_input_settings("Use"))
    if template.template_sleep("bed_radical",0.63,2) == False:
        time.sleep(1)
        utils.zero()
        utils.set_yaw(settings.station_yaw)
        time.sleep(1)
        pyautogui.keyDown(local_player.get_input_settings("Use"))
    if template.check_template_no_bounds("bed_radical",0.6):
        windows.move_mouse(variables.radical_laydown_x,variables.radical_laydown_y)
        time.sleep(0.5)
        pyautogui.keyUp(local_player.get_input_settings("Use"))
        render_flag = True

def leave_tekpod():
    time.sleep(0.4)
    pyautogui.press(local_player.get_input_settings("Use"))
    time.sleep(1)
    utils.current_yaw = settings.render_pushout
    utils.set_yaw(settings.station_yaw)
    time.sleep(0.5)
    global render_flag
    render_flag = False

if __name__ == "__main__":
    pass
    