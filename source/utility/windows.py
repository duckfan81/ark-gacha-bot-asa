import ctypes
import time
from ctypes import wintypes

from . import local_player, screen


WINDOW_TITLE = "ArkAscended"

INPUT_MOUSE = 0

MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_MOVE_NOCOALESCE = 0x2000
MOUSEEVENTF_ABSOLUTE = 0x8000

WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202

PIXELS_PER_DEGREE = 128.6 / 90.0

MAX_LR_SENS = 3.2
MAX_UD_SENS = 3.2
MAX_FOV = 1.25

MIN_SCALE = 0.25
MAX_SCALE = 4.0

hwnd = None

ULONG_PTR = ctypes.c_uint64 if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_uint32


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


class INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
    ]


class INPUT(ctypes.Structure):
    _anonymous_ = ("u",)
    _fields_ = [
        ("type", wintypes.DWORD),
        ("u", INPUT_UNION),
    ]


class POINT(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_long),
        ("y", ctypes.c_long),
    ]


SendInput = ctypes.windll.user32.SendInput
SendInput.argtypes = [wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int]
SendInput.restype = wintypes.UINT

FindWindowW = ctypes.windll.user32.FindWindowW
FindWindowW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]
FindWindowW.restype = wintypes.HWND

PostMessageW = ctypes.windll.user32.PostMessageW
PostMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
PostMessageW.restype = wintypes.BOOL

mouse_event = ctypes.windll.user32.mouse_event
mouse_event.argtypes = [
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    ULONG_PTR
]
mouse_event.restype = None


def find_window_by_title(title: str = WINDOW_TITLE) -> int:
    global hwnd

    hwnd = FindWindowW(None, title)

    if not hwnd:
        raise RuntimeError(f"Window not found: {title}")

    return hwnd


def get_hwnd(title: str = WINDOW_TITLE) -> int:
    global hwnd

    if hwnd:
        return hwnd

    return find_window_by_title(title)


def _safe_ratio(max_value: float, current_value: float, name: str) -> float:
    if current_value <= 0:
        raise ValueError(f"Invalid {name}: {current_value}")

    return max_value / current_value


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


def _send_mouse_move(dx: int, dy: int) -> None:
    if dx == 0 and dy == 0:
        return

    event = INPUT(
        type=INPUT_MOUSE,
        mi=MOUSEINPUT(
            dx=int(dx),
            dy=int(dy),
            mouseData=0,
            dwFlags=MOUSEEVENTF_MOVE | MOUSEEVENTF_MOVE_NOCOALESCE,
            time=0,
            dwExtraInfo=0,
        ),
    )

    sent = SendInput(1, ctypes.byref(event), ctypes.sizeof(INPUT))

    if sent != 1:
        raise ctypes.WinError()


def turn(degrees_x: int, degrees_y: int, steps: int = 10, delay: float = 0.005) -> None:
    lr_sens = local_player.get_look_lr_sens()
    ud_sens = local_player.get_look_ud_sens()
    fov = local_player.get_fov()

    fov_scale = _safe_ratio(MAX_FOV, fov, "fov")

    scale_x = _safe_ratio(MAX_LR_SENS, lr_sens, "look_lr_sens") * fov_scale
    scale_y = _safe_ratio(MAX_UD_SENS, ud_sens, "look_ud_sens") * fov_scale

    scale_x = _clamp(scale_x, MIN_SCALE, MAX_SCALE)
    scale_y = _clamp(scale_y, MIN_SCALE, MAX_SCALE)

    dx_total = degrees_x * PIXELS_PER_DEGREE * scale_x
    dy_total = degrees_y * PIXELS_PER_DEGREE * scale_y

    sent_x = 0
    sent_y = 0

    steps = max(1, int(steps))

    for i in range(1, steps + 1):
        target_x = round(dx_total * i / steps)
        target_y = round(dy_total * i / steps)

        move_x = target_x - sent_x
        move_y = target_y - sent_y

        sent_x = target_x
        sent_y = target_y

        _send_mouse_move(move_x, move_y)

        if delay > 0:
            time.sleep(delay)


def move_mouse(x: int, y: int) -> None:
    width = screen.mon["width"]
    height = screen.mon["height"]

    if width <= 0 or height <= 0:
        raise ValueError(f"Invalid screen size: {width}x{height}")

    scaled_x = int(x * 65535 / width)
    scaled_y = int(y * 65535 / height)

    mouse_event(
        MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE,
        scaled_x,
        scaled_y,
        0,
        0,
    )


def click(x: int, y: int, window_title: str = WINDOW_TITLE) -> None:
    target_hwnd = get_hwnd(window_title)

    lparam = (y << 16) | x

    if not PostMessageW(target_hwnd, WM_LBUTTONDOWN, 0, lparam):
        raise ctypes.WinError()

    if not PostMessageW(target_hwnd, WM_LBUTTONUP, 0, lparam):
        raise ctypes.WinError()