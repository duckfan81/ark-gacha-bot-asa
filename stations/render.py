import pyautogui
import template 
import variables
import time
import windows
import utils
import settings
import local_player
import discordbot
import ark
global render_flag
global retry
render_flag = False #starts as false as obviously we are not rendering anything
retry = 0 

def enter_tekpod():
    global render_flag
    global retry
    time.sleep(1)
    utils.zero()
    utils.set_yaw(settings.station_yaw)
    utils.turn_down(10) #more efficent at opening tekpod
    time.sleep(1)
    pyautogui.keyDown(local_player.get_input_settings("Use"))
    if template.template_sleep_no_bounds("bed_radical",0.60,2) == False:
        time.sleep(1)
        utils.zero()
        utils.set_yaw(settings.station_yaw)
        time.sleep(1)
        pyautogui.keyDown(local_player.get_input_settings("Use"))
    if template.check_template_no_bounds("bed_radical",0.6):
        windows.move_mouse(variables.radical_laydown_x,variables.radical_laydown_y)
        time.sleep(0.5)
        pyautogui.keyUp(local_player.get_input_settings("Use"))
    if template.template_sleep_no_bounds("tek_pod_xp",0.7,4) == False and retry < 3:
        discordbot.logger("failed to get into the tekpod waiting 10 seconds before retrying")
        time.sleep(10)
        retry += 1
        ark.check_state()
        enter_tekpod()
    if template.check_template_no_bounds("tek_pod_xp",0.7):
        discordbot.logger("NOW RENDERING STATION")
        retry = 0
        render_flag = True

def leave_tekpod():
    time.sleep(0.4)
    pyautogui.press(local_player.get_input_settings("Use"))
    if template.window_still_open_no_bounds("tek_pod_xp",0.7,10): # long time for big timers 
        pyautogui.press(local_player.get_input_settings("Use"))
    time.sleep(1)
    utils.current_yaw = settings.render_pushout
    utils.set_yaw(settings.station_yaw)
    time.sleep(0.5)
    global render_flag
    render_flag = False

if __name__ == "__main__":
    pass
    