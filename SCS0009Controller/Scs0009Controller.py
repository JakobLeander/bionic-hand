# =============================================================================
#  Scs0009Controller.py
#  SCS0009 Servo Controller class for controlling SCS0009 serial bus servos.
#  Copyright (c) 2025 Jakob Leander
#  Licensed under the MIT License.
# =============================================================================
import sys

sys.path.append("..")
from SCServo import *  # Uses SCServo library


class Scs0009Controller:
    BAUDRATE = 1000000  # SCServo default baudrate : 1000000
    MIN_POSITION = 0
    MAX_POSITION = 1024  # SCS0009 has a range of 0-1024 (0-300 degrees)
    MIN_DEGREE = -150
    MAX_DEGREE = +150
    MIN_SPEED = 1
    MAX_SPEED = 2048

    def __init__(self, com_port):
        """
        Initialize the SCS0009Controller and set up serial communication.

        Args:
            com_port (str): Serial port name. Valid values (Windows): "COM1", "COM2", "COM3", etc.

        Raises:
            ConnectionError: If the port cannot be opened or baudrate cannot be set.
        """
        self.com_port = com_port

        # Initialize PortHandler instance
        self.portHandler = PortHandler(com_port)

        # Initialize PacketHandler instance
        self.packetHandler = scscl(self.portHandler)

        # Open port
        if not self.portHandler.openPort():
            raise ConnectionError(f"Failed to open port: {com_port}")

        # Set port baudrate
        if not self.portHandler.setBaudRate(self.BAUDRATE):
            raise ConnectionError(f"Failed to set baud-rate: {self.BAUDRATE}")

    def ping(self, scs_id):
        """
        Ping the servo to check communication and retrieve its model number.

        Args:
            scs_id (int): The ID of the servo to ping.

        Returns:
            int: The model number of the servo if successful.

        Raises:
            RuntimeError: If there is a communication error or the servo returns an error code.
        """
        model_number, comm_result, error = self.packetHandler.ping(scs_id)
        if comm_result != COMM_SUCCESS:
            raise RuntimeError(
                f"Communication error: {self.packetHandler.getTxRxResult(comm_result)}"
            )
        if error != 0:
            raise RuntimeError(
                f"Servo error: {self.packetHandler.getRxPacketError(error)}"
            )
        return model_number

    def set_speed(self, scs_id, speed):
        """
        Set the speed of the servo.

        Args:
            scs_id (int): The ID of the servo to control.
            speed (int): Speed value (0-100), where 0 is minimum and 100 is maximum speed.

        Raises:
            ValueError: If speed is outside the range 0-100.
            RuntimeError: If communication or servo error occurs.
        """
        if speed < 0 or speed > 100:
            raise ValueError(f"Speed must be between 0 and 100")

        # Map speed from 0-100 to 1-2048
        servo_speed = int(
            self.MIN_SPEED + (speed / 100) * (self.MAX_SPEED - self.MIN_SPEED)
        )

        comm_result, error = self.packetHandler.WriteSpeed(scs_id, servo_speed)
        if comm_result != COMM_SUCCESS:
            raise RuntimeError(
                f"Communication error: {self.packetHandler.getTxRxResult(comm_result)}"
            )
        if error != 0:
            raise RuntimeError(
                f"Servo error: {self.packetHandler.getRxPacketError(error)}"
            )

    def set_position(self, scs_id, degree):
        """
        Set the position of the servo in degrees.

        Args:
            scs_id (int): The ID of the servo to control.
            degree (int): Position value in degrees (-150 to +150).

        Raises:
            ValueError: If degree is outside the range -150 to +150.
            RuntimeError: If communication or servo error occurs.
        """
        if degree < self.MIN_DEGREE or degree > self.MAX_DEGREE:
            raise ValueError(f"Position must be between -150 and +150 degrees")

        position = int(
            self.MIN_POSITION
            + ((degree + 150) / self.MAX_DEGREE)
            * (self.MAX_POSITION - self.MIN_POSITION)
        )

        comm_result, error = self.packetHandler.WritePosition(scs_id, position)
        if comm_result != COMM_SUCCESS:
            raise RuntimeError(
                f"Communication error: {self.packetHandler.getTxRxResult(comm_result)}"
            )
        if error != 0:
            raise RuntimeError(
                f"Servo error: {self.packetHandler.getRxPacketError(error)}"
            )

    def __del__(self):
        """
        Destructor to ensure the serial port is closed when the object is deleted.
        """
        self.portHandler.closePort()
