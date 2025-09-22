# =============================================================================
#  Scs0009_rotate.py
#  Test rotating the servo
#  Copyright (c) 2025 Jakob Leander
#  Licensed under the MIT License.
# =============================================================================
#!/usr/bin/env python


import sys
import time

sys.path.append("..")
from ServoController.Scs0009Controller import Scs0009Controller

# Default setting
id = 1  # SCServo ID : 1
DEVICENAME = "COM4"  # Check which port is being used on your controller

controller = Scs0009Controller(DEVICENAME)

degree = -45

controller.set_speed(id, 50)  # Set speed to 10%

while True:
    controller.move_angle(id, degree, 600)
    moving = True

    while moving:
        time.sleep(0.1)
        moving = controller.is_moving(id)

    degree = -degree
