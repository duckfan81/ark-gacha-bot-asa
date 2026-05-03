import time
import settings

from source.utility import utils
from source.ASA.strucutres import inventory
from source.ASA.player import player_inventory, player_state


PITCH_LOCATIONS = [0, -25, -12, -4, 4, -5.5, 1, 9, 17]

CROP_WAIT = 0.2
AFTER_HARVEST_WAIT = 0.3

TURN_BETWEEN_STACKS = 90
RESET_PITCH = 0

MIDDLE_STACK_SPLIT_INDEX = 4


def wait(seconds: float) -> None:
    time.sleep(seconds * settings.lag_offset)


def harvest_crop() -> None:
    inventory.open()

    try:
        inventory.search_in_object("y")
        inventory.transfer_all_from()

        # transfer snow pellets back into crop plot
        player_inventory.transfer_all_inventory()

    finally:
        inventory.close()

def harvest_stack(start_index: int = 0, stop_index: int | None = None) -> None:
    total_plots = len(PITCH_LOCATIONS) - 1

    if stop_index is None:
        stop_index = total_plots

    if start_index < 0 or stop_index > total_plots or start_index >= stop_index:
        raise ValueError(
            f"Invalid harvest range: start_index={start_index}, stop_index={stop_index}"
        )

    player_state.human.crouch()

    current_pitch = RESET_PITCH

    for index in range(start_index, stop_index):
        target_pitch = PITCH_LOCATIONS[index + 1]

        utils.turn_down(current_pitch - target_pitch)
        current_pitch = target_pitch

        if index == 4:
            player_state.human.reset_crouch()

        wait(CROP_WAIT)
        harvest_crop()
        wait(AFTER_HARVEST_WAIT)

    utils.set_pitch(RESET_PITCH)


def harvest_3() -> None:
    # Looking at the left-most stack to begin with
    for stack_index in range(3):
        harvest_stack()

        if stack_index < 2:
            utils.turn_right(TURN_BETWEEN_STACKS)


def harvest_for_side(side: str) -> None:
    """
    Starting position:
    - looking at the left-most crop stack
    - pitch reset to 0

    left side harvests:
    - full left stack
    - first 4 plots of middle stack

    right side harvests:
    - full right stack
    - last 4 plots of middle stack
    """

    side = side.lower()

    if side == "left":
        harvest_stack()

        utils.turn_right(TURN_BETWEEN_STACKS)

        harvest_stack(
            start_index=0,
            stop_index=MIDDLE_STACK_SPLIT_INDEX,
        )

    elif side == "right":
        # Skip left stack and middle stack, face right stack.
        utils.turn_right(TURN_BETWEEN_STACKS * 2)

        harvest_stack()

        # Face middle stack.
        utils.turn_left(TURN_BETWEEN_STACKS)

        harvest_stack(
            start_index=MIDDLE_STACK_SPLIT_INDEX,
            stop_index=None,
        )

    else:
        raise ValueError(f"Invalid gacha side: {side}")

