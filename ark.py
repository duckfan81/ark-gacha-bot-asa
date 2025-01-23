import pyautogui
import numpy as np
import time
import screen
import discordbot
import variables
import settings
import utils
import win32clipboard
import windows
import template
import stations.render as render

global bed_number
global first_run

first_run = True

def ini():
    time.sleep(0.2)
    if template.check_template_no_bounds("console",0.55) == False:
        utils.press_key("ConsoleKeys")

    with open("txt_files/iniFile.txt","r") as file:
        ini = file.read()

    count = 0
    while template.check_template_no_bounds("console",0.55) == False:
        if count > 20:
            break
        count += 1
        time.sleep(0.1)
    time.sleep(0.2)
    pyautogui.write(ini, interval=0.005) # issues when insta writing 
    utils.press_key("Enter")
    time.sleep(0.3)
    pyautogui.scroll(10) # puts char in first person 

def open_structure():
    utils.press_key("AccessInventory")
    if template.template_sleep("inventory",0.7,2) == False:
        utils.press_key("AccessInventory")
        template.template_sleep("inventory",0.7,2)
    if settings.singleplayer == False: # in single player i havent had the issue of the waiting screen
        if template.template_sleep("waiting_inv",0.8,2): # if the waiting_inv is shown on the screen in the 2 seconds after inventory apears 
            template.window_still_open("waiting_inv",0.8,5) # if server is laggy might take a while to get the data from the object
    
def dedi_withdraw(amount:int):
    time.sleep(0.1)
    discordbot.logger(f"withdrawing {amount} from the dedi") 
    for x in range(amount):
        time.sleep(0.5)
        windows.click(variables.dedi_withdraw_x,variables.dedi_withdraw_y)
    time.sleep(0.1)
    
def search_in_object(item:str): 
    discordbot.logger(f"searching in structure/dino for {item}")
    time.sleep(0.2)
    windows.click(variables.search_object_x,variables.transfer_all_y)
    windows.click(variables.search_object_x,variables.transfer_all_y) #double click to overright if previous
    time.sleep(0.2)
    utils.write(item)
    time.sleep(0.1)

def search_in_inventory(item:str):
    discordbot.logger(f"searching in inventory for {item}")
    time.sleep(0.2)
    windows.click(variables.search_inventory_x,variables.transfer_all_y) 
    time.sleep(0.2)
    windows.click(variables.search_inventory_x,variables.transfer_all_y) # double click to overright if previous
    time.sleep(0.2)
    utils.write(item)
    time.sleep(0.1)

def drop_all():  
    discordbot.logger(f"dropping all items")
    time.sleep(0.2)
    windows.click(variables.drop_all_x,variables.transfer_all_y) 
    time.sleep(0.1)

def transfer_all_from(): 
    discordbot.logger(f"transfering all from object")
    time.sleep(0.2)
    windows.click(variables.transfer_all_from_x, variables.transfer_all_y)
    time.sleep(0.1)

def transfer_all_inventory(): 
    discordbot.logger(f"transfering all in inventory")
    time.sleep(0.2)
    windows.click(variables.transfer_all_inventory_x,variables.transfer_all_y)
    time.sleep(0.1)

def check_state():
    if template.check_template("beds_title",0.7):
        bed_spawn_in(settings.bed_spawn)
        utils.yaw_zero()
        utils.set_yaw(settings.station_yaw)

    if render.render_flag == True:
        render.leave_tekpod()

    # if starving..... 

def popcorn_inventory(item):
    open = False
    if template.check_template("inventory",0.7) == False:
        open = True
        utils.press_key("ShowMyInventory")
        template.template_sleep("inventory",0.7,2)
        time.sleep(0.5)
    search_in_inventory(item)
    time.sleep(0.5)

    while template.inventory_first_slot(item,0.35):
        pyautogui.click(variables.inv_slot_start_x+30,variables.inv_slot_start_y+30)
        utils.press_key("DropItem")
        time.sleep(0.2)

    if open == True:
        windows.click(variables.close_inv_x,variables.close_inv_y)


def implant_eat():
    if template.check_template("inventory", 0.7) == False:
        utils.press_key("ShowMyInventory")
        
    if template.template_sleep("inventory",0.7,2) == False:
    
        if template.check_template("exit_resume",0.4) == True:
            utils.press_key("PauseMenu")
            time.sleep(1)
        else:
            utils.press_key("PauseMenu") # bed screen or tp screen

        time.sleep(1)
        utils.press_key("ShowMyInventory")
        
    time.sleep(1)
    utils.press_key("ShowMyInventory")
    time.sleep(1.5)
    pyautogui.keyDown("s")
    time.sleep(1)        # walking back to avoid suiciding on parts needing to be accessed
    pyautogui.keyUp("s")
    time.sleep(0.2)
    utils.press_key("ShowMyInventory")
    time.sleep(1.5)
    pyautogui.click(variables.implant_eat_x,variables.implant_eat_y)
    time.sleep(10) # acouting for lag on high ping 
    utils.press_key("Use")
    while template.check_template("death_regions") == False:
        time.sleep(0.2)
    time.sleep(1)


def white_flash():
    roi = screen.get_screen_roi(500,500,100,100)
    total_pixels = roi.size
    num_255_pixels = np.count_nonzero(roi == 255)
    percentage_255 = (num_255_pixels / total_pixels) * 100
    return percentage_255 >= 80


def console_ccc():
    if template.check_template("inventory",0.7):
        windows.click(variables.close_inv_x,variables.close_inv_y)
        template.window_still_open("inventory",0.7,2)
        time.sleep(0.4)
    if template.check_template("teleporter_title",0.7):
        windows.click(variables.search_bar_bed_alive_x-200,variables.search_bar_bed_y)
        template.window_still_open("teleporter_title",0.7,2)
        time.sleep(0.4)
    if template.check_template("beds_title",0.7):
        windows.click(variables.search_bar_bed_alive_x-200,variables.search_bar_bed_y)
        template.window_still_open("beds_title",0.7,2)
        time.sleep(0.4)

    time.sleep(0.1)
    utils.press_key("ConsoleKeys")
    count = 0
    while template.check_template_no_bounds("console",0.55) == False:
        if count > 31:
            break
        time.sleep(0.2)
        if count % 10 == 0 and count != 0:
            utils.press_key("ConsoleKeys")
        count += 1
    if template.check_template_no_bounds("console",0.55):
        pyautogui.write("ccc") # for some reason utils.write doesnt register
        time.sleep(0.3)
        utils.press_key("Enter")
        time.sleep(0.6) # slow to try and prevent opening clipboard to empty data
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        ccc_data = data.split()
        return ccc_data
    
def console_write(info:str):
    utils.press_key("ConsoleKeys")
    count = 0
    while template.check_template_no_bounds("console",0.55) == False:
        if count > 21:
            break
        time.sleep(0.2)
        if count % 10 == 0 and count != 0:
            utils.press_key("ConsoleKeys")
        count += 1
    if template.check_template_no_bounds("console",0.55):
        pyautogui.write(info)
        time.sleep(0.3)
        utils.press_key("Enter")
        time.sleep(0.2)
    
def bed_spawn_in(bed_name:str):

    if template.check_template("beds_title",0.7) == False:
        implant_eat()
    
    if template.check_template("death_regions",0.7) == True:
        windows.click(variables.search_bar_bed_dead_x,variables.search_bar_bed_y)
        windows.click(variables.search_bar_bed_dead_x,variables.search_bar_bed_y) # double click for saftey against pre-writen HAS TO BE COMBINED
        utils.write(bed_name)
    else:
        windows.click(variables.search_bar_bed_alive_x,variables.search_bar_bed_y)
        windows.click(variables.search_bar_bed_alive_x,variables.search_bar_bed_y) # double click for saftey against pre-writen HAS TO BE COMBINED
        utils.write(bed_name)

    time.sleep(0.2)
    windows.click(variables.first_bed_slot_x,variables.first_bed_slot_y)
    if template.template_sleep("ready_clicked_bed",0.7,1) == False:
        pass # maybe use ocr to see when bed is ready    

    windows.click(variables.spawn_button_x,variables.spawn_button_y)

    while white_flash() == False: # waiting for white flash to be true
        time.sleep(0.1)
    while white_flash() == True: # now waiting till its false
        time.sleep(0.1)

    time.sleep(10) # animation spawn in is about 7 seconds 
    while template.check_template("tribelog_check",0.8) == False and count < 100: # stopping inf loops 
        utils.press_key("ShowTribeManager")
        time.sleep(0.1)
        count += 1
    
    time.sleep(0.5)
    windows.click(variables.close_inv_x,variables.close_inv_y) # now ready to do whatever we need to 
    template.window_still_open("tribelog_check",0.8,2)

    global first_run
    if first_run:
        ini()
        first_run = False
    time.sleep(0.5)

    

def teleport_not_default(teleporter_name:str):
    
    time.sleep(0.3)
    utils.turn_down(80)    # include the looking down part into the teleport as it is common for everytime
    time.sleep(0.3)
    utils.press_key("Use")

    if template.template_sleep("teleporter_title",0.7,2) == False:
        utils.turn_down(80)
        time.sleep(0.2)
        utils.press_key("Use")
        template.template_sleep("teleporter_title",0.7,2)

    time.sleep(0.5)
    if template.teleport_icon(0.55) == False: # checking to see if we have the bed bug causing crashes 
        time.sleep(10)
    
    windows.click(variables.search_bar_bed_alive_x,variables.search_bar_bed_y)
    windows.click(variables.search_bar_bed_alive_x,variables.search_bar_bed_y)
    utils.write(teleporter_name)

    time.sleep(0.2)
    windows.click(variables.first_bed_slot_x,variables.first_bed_slot_y)
    time.sleep(0.2)
    windows.click(variables.spawn_button_x,variables.spawn_button_y)

    time.sleep(1)          
    while white_flash() == True:  #dont need white flash== False as if we are in render white flash will not appear on the screen   
        time.sleep(0.1)          # would cause a inf loop
    count = 0

    while template.check_template_no_bounds("tribelog_check",0.8) == False and count < 100: # stopping inf loops 
        utils.press_key("ShowTribeManager")
        time.sleep(0.1)
        count += 1

    if template.check_template_no_bounds("tribelog_check",0.8):
        time.sleep(0.5)
        windows.click(variables.close_inv_x,variables.close_inv_y) # now ready to do whatever we need to 
        
    template.window_still_open_no_bounds("tribelog_check",0.8,2)
    
    time.sleep(0.4)
    if settings.singleplayer: # correcting for singleplayers wierd tp mechanics
        utils.current_pitch = 0
        utils.turn_down(80)
    utils.turn_up(80)
    #utils.pitch_zero() # correcting pitch back to 0 from looking down at the tp
    time.sleep(0.4)


def teleport_default(teleporter_name): # param teleporter_name incase of unable to default
    
    ccc_data_before = console_ccc()
    utils.press_key("Reload")

    time.sleep(1)          
    while white_flash() == True: #dont need white flash== False as if we are in render white flash will not appear on the screen   
        time.sleep(0.1)

    count = 0
    while template.check_template("tribelog_check",0.8) == False and count < 100: # stopping inf loops 
        utils.press_key("ShowTribeManager")
        time.sleep(0.1)
        count += 1

    if template.check_template("tribelog_check",0.8):
        time.sleep(1)
        windows.click(variables.close_inv_x,variables.close_inv_y) # now ready to do whatever we need to 
        
    template.window_still_open("tribelog_check",0.8,2)
    time.sleep(0.2)

    ccc_data_after = console_ccc()
    result = [a == b for a, b in zip(ccc_data_after[:3], ccc_data_before[:3])]

    if not (False in result):

        time.sleep(0.4)
        utils.pitch_zero()
        time.sleep(0.4)
        utils.turn_down(80)
        time.sleep(0.5)
        teleport_not_default(teleporter_name)

        

if __name__ == "__main__":
    time.sleep(2)
    console_ccc()


   