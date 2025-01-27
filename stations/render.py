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
render_flag = False #starts as false as obviously we are not rendering anything

def enter_tekpod():
    global render_flag
    retry = 0  
    while retry < 3:  
        time.sleep(1)
        utils.zero()
        utils.set_yaw(settings.station_yaw)
        utils.turn_down(10)
        time.sleep(1)
        pyautogui.keyDown(local_player.get_input_settings("Use"))
        
        if not template.template_sleep_no_bounds("bed_radical", 0.6,2):
            discordbot.logger("cannot find the bed radical")
            pyautogui.keyUp(local_player.get_input_settings("Use"))
            time.sleep(1)
            utils.zero()
            utils.set_yaw(settings.station_yaw)
            utils.turn_down(10)
            time.sleep(1)
            pyautogui.keyDown(local_player.get_input_settings("Use"))
        time.sleep(1)
        if template.check_template_no_bounds("bed_radical", 0.6):
            windows.move_mouse(variables.radical_laydown_x, variables.radical_laydown_y)
            time.sleep(0.5)
            pyautogui.keyUp(local_player.get_input_settings("Use"))
        time.sleep(1)
        if template.template_sleep_no_bounds("tek_pod_xp", 0.7, 4):
            discordbot.logger("NOW RENDERING STATION")
            utils.current_pitch = 0
            render_flag = True
            time.sleep(0.5)
            utils.press_key("ShowMyInventory")

            if template.template_sleep("inventory", 0.7, 2):
                ark.drop_all()
                time.sleep(0.4)
                windows.click(variables.close_inv_x, variables.close_inv_y)
            if template.window_still_open("inventory", 0.7, 2):
                time.sleep(3)  # Guessing timer hit
                windows.click(variables.close_inv_x, variables.close_inv_y)
            return  
        else:
            discordbot.logger(f"failed to get into the tekpod. attempt {retry + 1}/3. retrying in 10 seconds")
            time.sleep(10)
            ark.check_state()
            retry += 1 

    discordbot.logger("Failed to enter the tekpod after 3 attempts.")


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
    