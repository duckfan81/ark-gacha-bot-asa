import settings
import re 
import os

def get_base_path():
    base_path = settings.base_path
    if "ARK Survival Ascended" not in base_path:
        base_path = os.path.join(base_path, "ARK Survival Ascended")
    return base_path


def get_user_settings(setting_name):

    settings_path = os.path.join(get_base_path(), "ShooterGame", "Saved", "Config", "Windows", "GameUserSettings.ini")
    if not os.path.exists(settings_path):
        raise FileNotFoundError(f"Settings file not found: {settings_path}")

    with open(settings_path, "r") as file:
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

    input_path = os.path.join(get_base_path(), "ShooterGame", "Saved", "Config", "Windows", "input.ini")
    
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input settings file not found: {input_path}")

    with open(input_path, "r") as file:

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
                