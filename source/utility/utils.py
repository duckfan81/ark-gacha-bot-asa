import ctypes
import time
from . import local_player ,windows
from source.logs import gachalogs as logs
from source.ASA.player import console , player_state
"""
FUNCTIONS FOR KEYBOARD 
"""
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_CHAR = 0x0102

keymap = {
    "tab":0x09,"escape" :0x1B,"return":0x0D, "enter":0x0D, "leftcontrol":0xA2, "zero": 0x30,
    "one":0x31, "two":0x32, "three":0x33 , "four":0x34 , "five":0x35 , "six":0x36 , "seven":0x37,
    "eight":0x38, "nine":0x39, "thumbmousebutton": 0x05, "thumbmousebutton2": 0x06, "spacebar": 0x20,"hyphen":0xBD,
    "leftshift":0xA0 , "tilde":0xC0
}

default_keymap = { 
    "use": "e", "consolekeys": "tilde", "showtribemanager": "l", "showmyinventory": "i", "accessinventory": "f", "dropitem":"o",
    "pausemenu": "escape","reload":"r","run":"leftshift","crouch":"c","useitem1": "one","useitem2": "two","useitem3": "three","useitem4": "four",
    "useitem5": "five","useitem6": "six","useitem7": "seven","useitem8": "eight","useitem9": "nine","useitem10": "zero"
}

hwnd = windows.hwnd
ctypes.windll.user32.VkKeyScanA.argtypes = [ctypes.c_char]
ctypes.windll.user32.VkKeyScanA.restype = ctypes.c_short  

def keymap_return(key_input):
    key = key_input.lower()

    if key in default_keymap: # this would only be triggered if the input.ini file is empty || base key mpa

        key = default_keymap[key]
        if key in keymap:
            return keymap[key]

    if key in keymap:
        return keymap[key]
 
    if len(key) == 1:
        result = ctypes.windll.user32.VkKeyScanA(ord(key))
   
        vk_code = result & 0xFF
        
        return vk_code

def press_key(input_action):
    vk_code = keymap_return(local_player.get_input_settings(input_action))

    ctypes.windll.user32.PostMessageW(hwnd, WM_KEYDOWN , vk_code, 0)
    time.sleep(0.05)
    ctypes.windll.user32.PostMessageW(hwnd, WM_KEYUP , vk_code, 0)

def post_charecter(char):
    ctypes.windll.user32.PostMessageW(hwnd, WM_CHAR, ord(char), 0)

def write(text):
    for c in text:
        post_charecter(c)
        
def ctrl_a(): # hotkey for sending ctrl a 
    ctypes.windll.user32.SendMessageW(windows.hwnd, WM_KEYDOWN, 0x11, 0)
    time.sleep(0.1)
    ctypes.windll.user32.SendMessageW(windows.hwnd, WM_KEYDOWN, 0x41, 0)
    time.sleep(0.1)  
    
    ctypes.windll.user32.SendMessageW(windows.hwnd, WM_KEYUP, 0x41, 0)
    time.sleep(0.1)
    ctypes.windll.user32.SendMessageW(windows.hwnd, WM_KEYUP, 0x11, 0)
"""
FUNCTIONS FOR MOUSE MOVEMENT
"""

current_yaw = 0.0
current_pitch = 0.0

PLAYER_PITCH_MINIMUM = -80.0
PLAYER_PITCH_MAX = 87.0


def normalize_yaw(yaw: float) -> float:
    yaw = (float(yaw) % 360 + 360) % 360

    if yaw > 180:
        yaw -= 360

    return yaw


def clamp_pitch(pitch: float) -> float:
    return max(PLAYER_PITCH_MINIMUM, min(float(pitch), PLAYER_PITCH_MAX))


def yaw_diff(target: float, current: float) -> float:
    return ((float(target) - float(current)) + 180) % 360 - 180


def read_yaw_pitch():
    ccc_data = console.console_ccc()
    return float(ccc_data[3]), float(ccc_data[4])


def refresh_yaw_pitch() -> None:
    global current_yaw
    global current_pitch

    try:
        current_yaw, current_pitch = read_yaw_pitch()
        current_yaw = normalize_yaw(current_yaw)
        current_pitch = clamp_pitch(current_pitch)
    except Exception as e:
        logs.logger.error(f"error reading yaw/pitch from ccc: {e}")


def set_yaw(yaw: float) -> None:
    global current_yaw

    refresh_yaw_pitch()

    try:
        target = normalize_yaw(float(yaw))
        diff = yaw_diff(target, current_yaw)

        if diff < 0:
            turn_left(abs(diff))
        else:
            turn_right(diff)

        current_yaw = target

    except Exception as e:
        logs.logger.error(f"error setting yaw: {e}")


def set_pitch(pitch: float) -> None:
    global current_pitch

    try:
        target = clamp_pitch(float(pitch))
        diff = target - float(current_pitch)

        if diff > 0:
            turn_up(diff)
        elif diff < 0:
            turn_down(abs(diff))

        current_pitch = target

    except Exception as e:
        logs.logger.error(f"error setting pitch: {e}")


def yaw_zero(ccc_data=None) -> None:
    global current_yaw

    try:
        if ccc_data is None:
            ccc_data = console.console_ccc()

        yaw = float(ccc_data[3])

        if yaw > 0:
            turn_left(yaw)
        else:
            turn_right(abs(yaw))

        current_yaw = 0.0

    except Exception as e:
        logs.logger.error(f"error processing ccc_data[3]: {e}")


def pitch_zero(ccc_data=None) -> None:
    global current_pitch

    try:
        if ccc_data is None:
            ccc_data = console.console_ccc()

        pitch = float(ccc_data[4])

        if pitch > 0:
            turn_down(pitch)
        else:
            turn_up(abs(pitch))

        current_pitch = 0.0

    except Exception as e:
        logs.logger.error(f"error processing ccc_data[4]: {e}")


def zero() -> None:
    logs.logger.debug("setting view angles back to 0")

    ccc_data = console.console_ccc()

    yaw_zero(ccc_data)
    pitch_zero(ccc_data)


def get_yaw_pitch():
    global current_yaw
    global current_pitch

    current_yaw, current_pitch = read_yaw_pitch()
    current_yaw = normalize_yaw(current_yaw)
    current_pitch = clamp_pitch(current_pitch)

    return current_yaw, current_pitch


def turn_right(degrees: float) -> None:
    global current_yaw

    degrees = abs(float(degrees))

    windows.turn(degrees, 0)

    current_yaw = normalize_yaw(float(current_yaw) + degrees)


def turn_left(degrees: float) -> None:
    global current_yaw

    degrees = abs(float(degrees))

    windows.turn(-degrees, 0)

    current_yaw = normalize_yaw(float(current_yaw) - degrees)


def turn_down(degrees: float) -> None:
    global current_pitch

    degrees = abs(float(degrees))
    current_pitch = clamp_pitch(current_pitch)

    allowed = min(current_pitch - PLAYER_PITCH_MINIMUM, degrees)

    if allowed <= 0:
        return

    windows.turn(0, allowed)

    current_pitch = clamp_pitch(current_pitch - allowed)


def turn_up(degrees: float) -> None:
    global current_pitch

    degrees = abs(float(degrees))
    current_pitch = clamp_pitch(current_pitch)

    allowed = min(PLAYER_PITCH_MAX - current_pitch, degrees)

    if allowed <= 0:
        return

    windows.turn(0, -allowed)

    current_pitch = clamp_pitch(current_pitch + allowed)


def turn_to(yaw: float, pitch: float) -> None:
    global current_yaw
    global current_pitch

    try:
        target_yaw = normalize_yaw(float(yaw))
        target_pitch = clamp_pitch(float(pitch))

        diff_yaw = yaw_diff(target_yaw, current_yaw)

        if diff_yaw < 0:
            turn_left(abs(diff_yaw))
        else:
            turn_right(diff_yaw)

        diff_pitch = target_pitch - current_pitch

        if diff_pitch > 0:
            turn_up(diff_pitch)
        elif diff_pitch < 0:
            turn_down(abs(diff_pitch))

        current_yaw = target_yaw
        current_pitch = target_pitch

    except Exception as e:
        logs.logger.error(f"error turning to yaw/pitch: {e}")