import utils
import time
import template
import windows
import ark
import variables

def pego_pickup():
    utils.turn_up(15)
    time.sleep(0.5)
    ark.open_structure()
    if template.template_sleep("inventory",0.7,2) == False:
        utils.turn_up(5)
        ark.open_structure()
    if template.check_template("inventory",0.7):
        ark.transfer_all_from()
        time.sleep(0.2)
        windows.click(variables.close_inv_x,variables.close_inv_y) # prevents pego being FLUNG
    if template.template_sleep("inventory",0.7,2):
        time.sleep(3) # guessing timer hit waiting it out
        windows.click(variables.close_inv_x,variables.close_inv_y)
        template.window_still_open("inventory",0.7,2)
        
    time.sleep(0.5)
    utils.turn_down(utils.current_pitch)
    time.sleep(0.2)