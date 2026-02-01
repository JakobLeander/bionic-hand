# =============================================================================
#  bionic_hand_colmi_ring.py
#  Controlling the bionic hand with a colmi ring
#  Copyright (c) 2025 Jakob Leander
#  Licensed under the MIT License.
# =============================================================================
#!/usr/bin/env python
from http import client
import sys
import time

from ServoController.Scs0009Controller import Scs0009Controller
import asyncio
import keyboard
from colmi_ring.colmi_client import ColmiClient

# Find these values with fd.exe from feetech
CENTER_DEFAULT = 511
INDEX_CENTER_R = 545
INDEX_CENTER_L = 475
MIDDLE_CENTER_R = 549
MIDDLE_CENTER_L = 511
RING_CENTER_R = 480
RING_CENTER_L = 518
THUMB_CENTER_R = 518
THUMB_CENTER_L = 498

# Define limits for fingers not thumb
FINGER_MIN_R = -40  # fully open
FINGER_MAX_L = 40  # fully open
FINGER_MAX_R = 85  # fully closed
FINGER_MIN_L = -85  # fully closed

# Define limits for thumb
# OBS be carefull not to hit the other fingers when closing
THUMB_MIN_R = -40  # fully open
THUMB_MAX_L = 40  # fully open
THUMB_MAX_R = 85  # fully closed
THUMB_MIN_L = -85  # fully closed

MIN_SPEED = 0
MAX_SPEED = 100

SRVID_INDEX_R = 1
SRVID_INDEX_L = 2
SRVID_MIDDLE_R = 3
SRVID_MIDDLE_L = 4
SRVID_RING_R = 5
SRVID_RING_L = 6
SRVID_THUMB_R = 7
SRVID_THUMB_L = 8

DEVICENAME = "COM5"  # Set to correct port for your system

controller = Scs0009Controller(DEVICENAME)

RING_ADDRESS = "32:31:47:36:08:07"  # Replace with your Colmi Ring's Bluetooth address


async def main():
    """
    Main entry point for controlling the bionic hand.
    Add your initialization and control logic here.
    """
    print("Hold SPACE to stop")

    open_hand()
    client = ColmiClient(RING_ADDRESS)

    async with client:
        await client.start_streaming()

        while True:
            x_abs = abs(client.accX)
            if x_abs > 8192:
                x_abs = 8192  # Clamp to max value

            fist_closed_percent = x_abs / 81.92  # Scale to 0-100%
            ring_controlled_hand(fist_closed_percent)

            await asyncio.sleep(0.5)

            if keyboard.is_pressed(" "):  # Check if space key is pressed
                print("Space key pressed - stopping streaming")
                await client.stop_streaming()
                break


def ring_controlled_hand(closed_percent):
    print(f"Closing hand to {closed_percent:.2f}%")
    speed = 50
    move_index(
        FINGER_MIN_R + (FINGER_MAX_R - FINGER_MIN_R) * closed_percent / 100,
        FINGER_MAX_L - (FINGER_MAX_L - FINGER_MIN_L) * closed_percent / 100,
        speed,
    )
    move_middle(
        FINGER_MIN_R + (FINGER_MAX_R - FINGER_MIN_R) * closed_percent / 100,
        FINGER_MAX_L - (FINGER_MAX_L - FINGER_MIN_L) * closed_percent / 100,
        speed,
    )
    move_ring(
        FINGER_MIN_R + (FINGER_MAX_R - FINGER_MIN_R) * closed_percent / 100,
        FINGER_MAX_L - (FINGER_MAX_L - FINGER_MIN_L) * closed_percent / 100,
        speed,
    )
    move_thumb(THUMB_MIN_R + 20, THUMB_MAX_L - 20, speed)


def open_hand():
    """
    Open all fingers
    """
    speed = 30
    move_index(FINGER_MIN_R, FINGER_MAX_L, speed)
    move_middle(FINGER_MIN_R, FINGER_MAX_L, speed)
    move_ring(FINGER_MIN_R, FINGER_MAX_L, speed)
    move_thumb(THUMB_MIN_R, THUMB_MAX_L, speed)


def close_hand():
    """
    Close all fingers
    """
    speed = 30
    move_index(FINGER_MAX_R, FINGER_MIN_L, speed)
    move_middle(FINGER_MAX_R, FINGER_MIN_L, speed)
    move_ring(FINGER_MAX_R, FINGER_MIN_L, speed)
    time.sleep(0.5)
    move_thumb(20, -20, speed)


def move_index(angle_r, angle_l, speed):
    """
    Move the index finger to the specified angles.

    Args:
        angle_one (int): Angle in degrees (-85 to +85).
        angle_two (int): Angle in degrees (-85 to +85).
    """

    if speed < MIN_SPEED or speed > MAX_SPEED:
        raise ValueError(f"Speed must be between {MIN_SPEED} and {MAX_SPEED}")

    controller.set_speed(SRVID_INDEX_R, speed)
    controller.set_speed(SRVID_INDEX_L, speed)
    controller.move_angle(SRVID_INDEX_R, angle_r, INDEX_CENTER_R)
    controller.move_angle(SRVID_INDEX_L, angle_l, INDEX_CENTER_L)


def move_middle(angle_r, angle_l, speed):
    """
    Move the middle finger to the specified angles.

    Args:
        angle_one (int): Angle in degrees (-85 to +85).
        angle_two (int): Angle in degrees (-85 to +85).
    """

    if speed < MIN_SPEED or speed > MAX_SPEED:
        raise ValueError(f"Speed must be between {MIN_SPEED} and {MAX_SPEED}")

    controller.set_speed(SRVID_MIDDLE_R, speed)
    controller.set_speed(SRVID_MIDDLE_L, speed)
    controller.move_angle(SRVID_MIDDLE_R, angle_r, MIDDLE_CENTER_R)
    controller.move_angle(SRVID_MIDDLE_L, angle_l, MIDDLE_CENTER_L)


def move_ring(angle_r, angle_l, speed):
    """
    Move the ring finger to the specified angles.

    Args:
        angle_one (int): Angle in degrees (-85 to +85).
        angle_two (int): Angle in degrees (-85 to +85).
    """

    if speed < MIN_SPEED or speed > MAX_SPEED:
        raise ValueError(f"Speed must be between {MIN_SPEED} and {MAX_SPEED}")

    controller.set_speed(SRVID_RING_R, speed)
    controller.set_speed(SRVID_RING_L, speed)
    controller.move_angle(SRVID_RING_R, angle_r, RING_CENTER_R)
    controller.move_angle(SRVID_RING_L, angle_l, RING_CENTER_L)


def move_thumb(angle_r, angle_l, speed):
    """
    Move the thumb to the specified angles.

    Args:
        angle_one (int): Angle in degrees (-85 to +85).
        angle_two (int): Angle in degrees (-85 to +85).
    """

    if speed < MIN_SPEED or speed > MAX_SPEED:
        raise ValueError(f"Speed must be between {MIN_SPEED} and {MAX_SPEED}")

    controller.set_speed(SRVID_THUMB_R, speed)
    controller.set_speed(SRVID_THUMB_L, speed)
    controller.move_angle(SRVID_THUMB_R, angle_r, THUMB_CENTER_R)
    controller.move_angle(SRVID_THUMB_L, angle_l, THUMB_CENTER_L)


if __name__ == "__main__":
    asyncio.run(main())
