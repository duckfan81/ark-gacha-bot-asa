from source.utility import utils

GACHA_ANGLE_FROM_MIDDLE_CROP = 135
SIDE_STACK_ANGLE_FROM_GACHA = 45
STACK_ANGLE_TO_MIDDLE = 90


def face_gacha_from_middle_crop(side: str) -> None:
    side = side.lower()

    if side == "left":
        utils.turn_right(GACHA_ANGLE_FROM_MIDDLE_CROP)
    elif side == "right":
        utils.turn_left(GACHA_ANGLE_FROM_MIDDLE_CROP)
    else:
        raise ValueError(f"Invalid gacha side: {side}")


def face_side_stack_from_gacha(side: str) -> None:
    side = side.lower()

    if side == "left":
        utils.turn_left(SIDE_STACK_ANGLE_FROM_GACHA)
    elif side == "right":
        utils.turn_right(SIDE_STACK_ANGLE_FROM_GACHA)
    else:
        raise ValueError(f"Invalid gacha side: {side}")


def face_middle_crop_from_side_stack(side: str) -> None:
    side = side.lower()

    if side == "left":
        utils.turn_right(STACK_ANGLE_TO_MIDDLE)
    elif side == "right":
        utils.turn_left(STACK_ANGLE_TO_MIDDLE)
    else:
        raise ValueError(f"Invalid gacha side: {side}")


def face_middle_crop_from_gacha(side: str) -> None:
    side = side.lower()

    if side == "left":
        utils.turn_left(GACHA_ANGLE_FROM_MIDDLE_CROP)
    elif side == "right":
        utils.turn_right(GACHA_ANGLE_FROM_MIDDLE_CROP)
    else:
        raise ValueError(f"Invalid gacha side: {side}")