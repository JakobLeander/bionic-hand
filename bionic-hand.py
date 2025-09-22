# =============================================================================
#  bionic-hand.py
#  Controlling the bionic hand
#  Copyright (c) 2025 Jakob Leander
#  Licensed under the MIT License.
# =============================================================================
#!/usr/bin/env python
import sys
import time

from ServoController.Scs0009Controller import Scs0009Controller

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

DEVICENAME = "COM4"  # Set to correct port for your system

controller = Scs0009Controller(DEVICENAME)


def main():
    """
    Main entry point for controlling the bionic hand.
    Add your initialization and control logic here.
    """
    print("Bionic hand control started.")
    # TODO: Add initialization and control code

    horns()

    # open_hand()

    exit(0)

    while True:
        open_hand()
        time.sleep(2)
        close_hand()
        time.sleep(2)


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
    Open all fingers
    """
    speed = 30
    move_index(FINGER_MAX_R, FINGER_MIN_L, speed)
    move_middle(FINGER_MAX_R, FINGER_MIN_L, speed)
    move_ring(FINGER_MAX_R, FINGER_MIN_L, speed)
    time.sleep(0.5)
    move_thumb(20, -20, speed)


def point_index():
    """
    Point with index finger
    """
    speed = 30
    move_index(FINGER_MIN_R, FINGER_MAX_L, speed)
    move_middle(FINGER_MAX_R, FINGER_MIN_L, speed)
    move_ring(FINGER_MAX_R, FINGER_MIN_L, speed)
    time.sleep(0.5)
    move_thumb(60, -60, speed)


def no_no():
    """
    No no with index finger
    """
    speed = 30
    move_index(FINGER_MIN_R, FINGER_MAX_L, speed)
    move_middle(FINGER_MAX_R, FINGER_MIN_L, speed)
    move_ring(FINGER_MAX_R, FINGER_MIN_L, speed)
    time.sleep(0.5)
    move_thumb(60, -60, speed)
    time.sleep(1)

    speed = 50
    sleep_time = 0.3
    move_index(0, 85, speed)
    time.sleep(sleep_time)
    move_index(-85, 0, speed)
    time.sleep(sleep_time)
    move_index(0, 85, speed)
    time.sleep(sleep_time)
    move_index(-85, 0, speed)
    time.sleep(sleep_time)
    move_index(0, 85, speed)
    time.sleep(sleep_time)
    move_index(-85, 0, speed)


def horns():
    """
    Horns
    """
    speed = 30
    move_index(-20, 60, speed)
    move_middle(FINGER_MAX_R, FINGER_MIN_L, speed)
    move_ring(-60, 20, speed)
    time.sleep(0.5)
    move_thumb(60, -60, speed)


def victory():
    """
    Victory sign with index and middle finger
    """
    speed = 30
    move_index(0, 85, speed)
    move_middle(-85, 0, speed)
    move_ring(FINGER_MAX_R, FINGER_MIN_L, speed)
    time.sleep(0.5)
    move_thumb(60, -60, speed)


def scissor():
    """
    Scissor in rock paper scissors. Use open and close for paper and rock
    """
    speed = 30
    move_index(-30, 50, speed)
    move_middle(-50, 30, speed)
    move_ring(FINGER_MAX_R, FINGER_MIN_L, speed)
    time.sleep(0.5)
    move_thumb(60, -60, speed)


def thumbs_up():
    """
    Thumbs up sign
    """
    speed = 30
    move_thumb(THUMB_MIN_R, THUMB_MAX_L, speed)
    time.sleep(0.5)
    move_index(FINGER_MAX_R, FINGER_MIN_L, speed)
    move_middle(FINGER_MAX_R, FINGER_MIN_L, speed)
    move_ring(FINGER_MAX_R, FINGER_MIN_L, speed)


def perfect():
    """
    Perfect sign
    """
    speed = 30
    move_index(35, -35, speed)
    move_middle(FINGER_MIN_R, FINGER_MAX_L, speed)
    move_ring(FINGER_MIN_R, FINGER_MAX_L, speed)
    move_thumb(15, -15, speed)


def three():
    """
    Three
    """
    speed = 30
    move_index(-30, 50, speed)
    move_middle(-50, 30, speed)
    move_ring(FINGER_MAX_R, FINGER_MIN_L, speed)
    move_thumb(-40, -60, speed)


def four():
    """
    Four
    """
    speed = 30
    move_index(FINGER_MIN_R, FINGER_MAX_L, speed)
    move_middle(FINGER_MIN_R, FINGER_MAX_L, speed)
    move_ring(FINGER_MIN_R, FINGER_MAX_L, speed)
    time.sleep(0.5)
    move_thumb(-40, -60, speed)


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
    main()
