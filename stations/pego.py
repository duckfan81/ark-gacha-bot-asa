import utils
import time
import template
import windows
import ark
import variables

def pego_pickup():
    utils.turn_up(15)
    time.sleep(1)
    ark.open_structure()
    if template.template_sleep("inventory",0.7,2) == False:
        utils.turn_up(5)
        ark.open_structure()
    ark.transfer_all_from()
    time.sleep(0.2)
    windows.click(variables.close_inv_x,variables.close_inv_y)
    time.sleep(1.5)
    utils.turn_down(utils.current_pitch)
    time.sleep(0.2)