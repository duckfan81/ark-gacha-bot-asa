import json
import settings
screen_resolution = settings.screen_resolution # depending on your screen make it 1080 or 1440


def load_resolution_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def get_resolution_data(data, screen_resolution):
    for resolution_data in data["resolution"]:
        if resolution_data["screen"] == screen_resolution:
            return resolution_data["data"][0]
    return None

resolution_data = load_resolution_data("json_files/resolution.json")

target_data = get_resolution_data(resolution_data, screen_resolution)



transfer_all_from_x = target_data["transfer_all_from_x"]
transfer_all_y = target_data["transfer_all_y"]
transfer_all_inventory_x = target_data["transfer_all_inventory_x"]
drop_all_x = target_data["drop_all_x"]
search_inventory_x = target_data["search_inventory_x"]
search_object_x = target_data["search_object_x"]
dedi_withdraw_x = target_data["dedi_withdraw_x"]
dedi_withdraw_y = target_data["dedi_withdraw_y"]
search_bar_bed_y = target_data["search_bar_bed_y"]
search_bar_bed_dead_x = target_data["search_bar_bed_dead_x"]
search_bar_bed_alive_x = target_data["search_bar_bed_alive_x"] 
spawn_button_x = target_data["spawn_button_x"]
spawn_button_y = target_data["spawn_button_y"]
implant_eat_x = target_data["implant_eat_x"]
implant_eat_y = target_data["implant_eat_y"]
radical_laydown_x = target_data["radical_laydown_x"]
radical_laydown_y = target_data["radical_laydown_y"]
first_bed_slot_x = target_data["first_bed_slot_x"]
first_bed_slot_y = target_data["first_bed_slot_y"]
close_inv_x = target_data["close_inv_x"]
close_inv_y = target_data["close_inv_y"]
inv_slot_start_x = target_data["inv_slot_start_x"]
inv_slot_start_y = target_data["inv_slot_start_y"]
inv_slot_end_x = target_data["inv_slot_end_x"]
inv_slot_end_y = target_data["inv_slot_end_y"]
