import ctypes
import time
import local_player
import windows
import ark 

"""
FUNCTIONS FOR KEYBOARD 
"""
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_CHAR = 0x0102

keymap = {
    "tab":0x09,"escape" :0x1B,"return":0x0D, "enter":0x0D, "leftcontrol":0xA2, "zero": 0x30,
    "one":0x31, "two":0x32, "three":0x33 , "four":0x34 , "five":0x35 , "six":0x36 , "seven":0x37,
    "eight":0x38, "nine":0x39, "thumbmousebutton": 0x05, "thumbmousebutton2": 0x06, "spacebar": 0x20
}
hwnd = windows.hwnd
ctypes.windll.user32.VkKeyScanA.argtypes = [ctypes.c_char]
ctypes.windll.user32.VkKeyScanA.restype = ctypes.c_short  

def get_vk_code_for_char(char):
    
    char = char.lower()

    if char in keymap:
        return keymap[char]
 
    if len(char) == 1:
        result = ctypes.windll.user32.VkKeyScanA(ctypes.c_char(char.encode('ascii')))
   
        vk_code = result & 0xFF
        
        return vk_code

def press_key(input_action):

    vk_code = get_vk_code_for_char(local_player.get_input_settings(input_action))
    ctypes.windll.user32.PostMessageW(hwnd, WM_KEYDOWN , vk_code, 0)
    time.sleep(0.05)
    ctypes.windll.user32.PostMessageW(hwnd, WM_KEYUP , vk_code, 0)

def post_charecter(char):
    ctypes.windll.user32.PostMessageW(hwnd, WM_CHAR, ord(char), 0)

def write(text):
    for c in text:
        post_charecter(c)
        

"""
FUNCTIONS FOR MOUSE MOVEMENT
"""

current_yaw = 0
current_pitch = 0
player_pitch_minimum = -80
player_pitch_max = 87

def normalize_yaw(yaw):
    yaw = (yaw % 360 + 360) % 360
    if (yaw > 180):
        yaw -= 360
    return yaw 

def set_yaw(yaw):
    global current_yaw
    diff = ((yaw - current_yaw) + 180) % 360 - 180
    if diff < 0:
        turn_left(-diff)
    else:
        turn_right(diff)
    current_yaw = yaw

def set_pitch(pitch):
    global current_pitch
    change = current_pitch - pitch 
    if change < 0:
        turn_up(-change)
    else:
        turn_down(change)
    current_pitch = pitch
    
def yaw_zero():
    global current_yaw
    ccc_data = ark.console_ccc()

    if float(ccc_data[3]) > 0:
        turn_left(float(ccc_data[3]))
    else:
        turn_right(-float(ccc_data[3]))
    current_yaw = 0

def pitch_zero():
    global current_pitch
    ccc_data = ark.console_ccc()
    
    if float(ccc_data[4]) > 0:
        turn_down(float(ccc_data[4]))
    else:
        turn_up(-float(ccc_data[4]))
    current_pitch = 0

def zero():
    global current_pitch
    global current_yaw
    ccc_data = ark.console_ccc()

    if float(ccc_data[3]) > 0:
        turn_left(float(ccc_data[3]))
    else:
        turn_right(-float(ccc_data[3]))
    
    if float(ccc_data[4]) > 0:
        turn_down(float(ccc_data[4]))
    else:
        turn_up(-float(ccc_data[4]))
    current_yaw = 0
    current_pitch = 0

def turn_right(degrees):
    global current_yaw
    windows.turn(degrees, 0)
    current_yaw = normalize_yaw(current_yaw + degrees)


def turn_left(degrees):
    global current_yaw
    windows.turn(-degrees, 0)
    current_yaw = normalize_yaw(current_yaw - (-degrees))
    

def turn_down(degrees):
    global current_pitch
    allowed = min(abs(player_pitch_minimum - current_pitch), degrees)
    windows.turn(0, allowed)
    current_pitch -= allowed


def turn_up(degrees):
    global current_pitch
    allowed = min(abs(player_pitch_max - current_pitch), degrees)
    windows.turn(0, -allowed)
    current_pitch += allowed
