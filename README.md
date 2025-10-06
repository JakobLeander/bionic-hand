
# Bionic Hand Project

This repository contains the code and resources for building and controlling a bionic hand using Python and Arduino hardware.

## Features
- Python-based servo control for SCS0009 serial bus servos
- Arduino receiver and emitter code for hardware communication
- Hardware test scripts for individual component validation
- Wiring diagrams and media resources

## Getting Started
1. **Hardware Setup**

    Connect all components as shown below:

![Wiring Diagram](media/wiring.png)

2. **Create a virtual environment**
    <!-- Ensure you have Python 3.8+ installed before proceeding. -->
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
 
3. **Testing Hardware**

    Run the test scripts in the "hardware-test" folder to verify each component:
    -  SCS009_ping.py: Ping a servo and validate it responds
    -  SCS009_rotate.py: Rotate a single servo back and forth
    -  SCS009_zero_all.py: Center all servos
    -  arduinoemitter.ino: Makes the arduino output serial data
    -  arduino_reciever.py: Read and print serial data from arduino

## Python Hand Gestures
Use the main control script `bionic_hand_gestures.py` to make the hand do prerecorded movements

Example usage:

	  python bionic_hand_gestures.py


## Python Hand Muscle Control
Use the main control script `bionic_hand_muscle.py` to control the hand via a muscle sensor from Sparkfun

Example usage:

	  python bionic_hand_muscle.py


## License
MIT License © 2025 Jakob Leander

