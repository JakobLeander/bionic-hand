# =============================================================================
#  Scs0009_zero_position.py
#  Set servo to zero position
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

degree = 0

controller.set_speed(id, 50)  # Set speed to 10%

controller.move_angle(id, degree)
