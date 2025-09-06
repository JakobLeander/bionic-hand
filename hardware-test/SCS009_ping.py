# =============================================================================
#  Scs0009_ping.py
#  Test pinging the servo to get its model number
#  Copyright (c) 2025 Jakob Leander
#  Licensed under the MIT License.
# =============================================================================
#!/usr/bin/env python


import sys

sys.path.append("..")
from ServoController.Scs0009Controller import Scs0009Controller

# Default setting
id = 1  # SCServo ID : 1
DEVICENAME = "COM4"  # Check which port is being used on your controller

controller = Scs0009Controller(DEVICENAME)

servo_model_number = controller.ping(id)

print(f"Servo model number: {servo_model_number}")
