import utils
import time
import template
import windows
import ark
import variables
import settings

def pego_pickup():
    utils.turn_up(15)
    time.sleep(0.5)
    ark.open_structure()
    if template.template_sleep("inventory",0.7,2) == False:
        utils.zero()
        utils.set_yaw(settings.station_yaw)
        utils.press_key("Jump")
        utils.turn_up(15)
        time.sleep(0.5)
        ark.open_structure()
    if template.check_template("inventory",0.7):
        ark.drop_all()
        time.sleep(0.2)
        ark.transfer_all_from()
        time.sleep(0.2)
        ark.close_inventory() # prevents pego being FLUNG
        
    time.sleep(0.5)
    utils.turn_down(utils.current_pitch)
    time.sleep(0.2)