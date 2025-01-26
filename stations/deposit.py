import utils
import time
import template
import ark
import windows
import variables
import json
import settings
import discordbot

def load_resolution_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def open_crystals():
    count = 0
    while template.check_template("crystal_in_hotbar",0.7) and count < 350: # count is alittle higher incase while pressing the button it doesnt triger
        for x in range(10):
            utils.press_key(f"UseItem{x+1}")
            count += 1

def dedi_deposit(height):
    if height == 3:
        utils.turn_up(15)
        utils.turn_left(10)
        time.sleep(0.2)
        utils.press_key("Use")
        time.sleep(0.2)
        utils.turn_right(40)
        time.sleep(0.2)
        utils.press_key("Use")
        time.sleep(0.2)
        utils.turn_left(30)
        utils.turn_down(15)

    utils.turn_left(10)
    utils.press_key("Crouch")
    time.sleep(0.2)
    utils.press_key("Use")
    time.sleep(0.2)
    utils.turn_right(40)
    time.sleep(0.2)
    utils.press_key("Use")
    time.sleep(0.2)
    utils.turn_down(30)
    time.sleep(0.2)
    utils.press_key("Use")
    time.sleep(0.2)
    utils.turn_left(40)
    time.sleep(0.2)
    utils.press_key("Use")
    time.sleep(0.2)
    utils.press_key("Jump")
    utils.turn_up(30)
    utils.turn_right(10)

def vault_deposit(side,items):
    if side == "left":
        utils.turn_left(90)
    else:
        utils.turn_right(90)

    time.sleep(0.5)
    ark.open_structure()
    if template.template_sleep("inventory",0.7,2):
        for x in range(len(items)):
            ark.search_in_inventory(items[x])
            ark.transfer_all_inventory()
            time.sleep(0.4)
        windows.click(variables.close_inv_x,variables.close_inv_y)
        if template.window_still_open("inventory",0.7,2):
            time.sleep(3) # guessing timer hit
            windows.click(variables.close_inv_x,variables.close_inv_y)
        time.sleep(0.5)
    if side == "left":
        utils.turn_right(90)
    else:
        utils.turn_left(90)
    time.sleep(0.5)

def drop_useless():
    discordbot.logger("dropping all useless things")
    time.sleep(0.5)
    utils.press_key("Crouch")
    time.sleep(0.4)
    utils.press_key("ShowMyInventory")
    if template.template_sleep("inventory",0.7,2):
        ark.search_in_inventory(settings.berry_type)
        ark.drop_all()
        time.sleep(0.4)
        windows.click(variables.close_inv_x,variables.close_inv_y)
        if template.window_still_open("inventory",0.7,2):
            time.sleep(3) # guessing timer hit
            windows.click(variables.close_inv_x,variables.close_inv_y)
    time.sleep(0.5)
    utils.press_key("Jump")
    time.sleep(0.5)
    utils.press_key("ShowMyInventory")

    if template.template_sleep("inventory",0.7,2):
        ark.drop_all()
        time.sleep(0.4)
        windows.click(variables.close_inv_x,variables.close_inv_y)
        if template.window_still_open("inventory",0.7,2):
            time.sleep(3) # guessing timer hit
            windows.click(variables.close_inv_x,variables.close_inv_y)
    time.sleep(0.5)
    utils.turn_down(85)
    time.sleep(0.5)
    ark.open_structure()
    if template.template_sleep("inventory",0.7,2):
        ark.transfer_all_from() # dont need a close as a bag will disapear
        if template.window_still_open("inventory",0.7,2):
            time.sleep(3) # guessing timer hit
            windows.click(variables.close_inv_x,variables.close_inv_y)
    else:
        discordbot.logger("no bag dropped")
    time.sleep(0.8)


def depo_grinder():
    utils.turn_right(180)
    time.sleep(0.5)
    ark.open_structure()
    if template.template_sleep("inventory",0.7,2) == False:
        time.sleep(2)
        ark.open_structure()
        time.sleep(0.4)

    if template.check_template("inventory",0.7):
        ark.transfer_all_inventory()
        time.sleep(0.3)
        windows.click(variables.dedi_withdraw_x,variables.dedi_withdraw_y)
        time.sleep(0.3)
        windows.click(variables.close_inv_x,variables.close_inv_y)
        if template.window_still_open("inventory",0.7,2):
            time.sleep(3) # guessing timer hit
            windows.click(variables.close_inv_x,variables.close_inv_y)
    time.sleep(0.5)
    utils.turn_right(180)

def collect_grindables():
    time.sleep(0.5)
    utils.turn_right(90)
    time.sleep(0.75)
    ark.open_structure()
    if template.template_sleep("inventory",0.7,2) == False:
        time.sleep(2)
        ark.open_structure()
        time.sleep(0.4)
    if template.check_template("inventory",0.7):
        ark.transfer_all_from()
        time.sleep(0.2)
        windows.click(variables.close_inv_x,variables.close_inv_y)
        if template.window_still_open("inventory",0.7,2):
            time.sleep(3) # guessing timer hit
            windows.click(variables.close_inv_x,variables.close_inv_y)
    time.sleep(0.5)
    utils.turn_left(90)
    time.sleep(0.8) # stopping hitting E on the fabricator
    dedi_deposit(settings.height_grind)
    time.sleep(0.2)
    drop_useless()


def vaults():
    vaults_data = load_resolution_data("json_files/vaults.json")
    for entry_vaults in vaults_data:
        name = entry_vaults["name"]
        side = entry_vaults["side"]
        items = entry_vaults["items"]
        discordbot.logger(f"openening up {name} on the {side} side to depo{items}")
        vault_deposit(side,items)

def deposit_all():
    time.sleep(0.5)
    utils.zero()
    utils.set_yaw(settings.station_yaw)
    discordbot.logger("opening crystals")
    open_crystals()
    discordbot.logger("depositing in ele dedi")
    dedi_deposit(settings.height_ele)
    vaults()
    if settings.height_grind != 0:
        discordbot.logger("depositing in grinder")
        depo_grinder()
        ark.teleport_not_default(settings.grindables)
        discordbot.logger("collecting grindables")
        collect_grindables()
    else:
        drop_useless()
