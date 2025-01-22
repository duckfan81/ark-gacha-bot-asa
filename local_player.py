import settings
import re 

def get_user_settings(setting_name):
    with open(f"{settings.base_path}ARK Survival Ascended/ShooterGame/Saved/Config/Windows/GameUserSettings.ini", "r") as file:
        for line in file:
            if setting_name in line:
                key, value = line.strip().split("=")
                return value
            
def get_look_lr_sens():
    return float(get_user_settings("LookLeftRightSensitivity"))

def get_look_ud_sens():
    return float(get_user_settings("LookUpDownSensitivity"))

def get_fov():
    return float(get_user_settings("FOVMultiplier"))

def get_input_settings(input_name):
    action_mappings = {}

    with open(f"{settings.base_path}ARK Survival Ascended/ShooterGame/Saved/Config/Windows/input.ini", "r") as file:

        if input_name == "ConsoleKeys":
            for line in file:
                if input_name in line:
                    name, value = line.strip().split("=")
                    return value
                   
                
        for line in file:
            match = re.match(r'ActionMappings=\(ActionName="([^"]+)",.*Key=([A-Za-z0-9_]+)\)', line.strip())
            if match:
                action_name = match.group(1)
                key = match.group(2)          
                
                if action_name == input_name:
                    return key
                
    return input_name
                