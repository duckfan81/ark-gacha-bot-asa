import utils
import time
import template
import windows
import ark
import variables
import settings

def pego_pickup(metadata):
    utils.turn_up(15)
    time.sleep(0.5)
    ark.open_structure()
    if template.template_sleep("inventory",0.7,2) == False:
        utils.zero()
        utils.set_yaw(metadata.yaw)
        utils.press_key("Run")
        utils.turn_up(15)
        time.sleep(0.5)
        ark.open_structure()
    if template.check_template("inventory",0.7):
        ark.drop_all_inv()
        time.sleep(0.2)
        ark.transfer_all_from()
        time.sleep(0.2)
        ark.close_inventory() # prevents pego being FLUNG
        
    time.sleep(0.5)
    utils.turn_down(utils.current_pitch)
    time.sleep(0.2)

def populate_hotbar():
    ark.open_inventory()
    ark.search_in_inventory("crystal")
    time.sleep(0.2)
    if template.check_template("crystal_in_inventory",0.7):
        windows.click(variables.get_pixel_loc("inv_slot_start_x")+50,variables.get_pixel_loc("inv_slot_start_y")+70)
        for x in range(10):
            utils.press_key(f"UseItem{x+1}")
            time.sleep(0.2)
    ark.close_inventory()
    time.sleep(0.2)