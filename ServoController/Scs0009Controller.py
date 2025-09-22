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
    CENTER_POSITION = 512
    MIN_DEGREE = -85
    MAX_DEGREE = +85
    MIN_SPEED = 1
    MAX_SPEED = 2048

    def __init__(self, com_port):
        """
        Initialize the SCS0009Controller.

        Args:
            com_port (str): Serial port name.
                Valid values (Windows): "COM1", "COM2", "COM3", etc.
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

    def ping(self, id: int) -> int:
        """
        Ping the servo to check communication and retrieve its model number.

        Args:
            id (int): ID of the servo to ping.

        Returns:
            int: The model number of the servo if successful.

        Raises:
            RuntimeError: If there is a communication error or the servo returns an error code.
        """
        model_number, comm_result, error = self.packetHandler.ping(id)
        if comm_result != COMM_SUCCESS:
            raise RuntimeError(
                f"Communication error: {self.packetHandler.getTxRxResult(comm_result)}"
            )
        if error != 0:
            raise RuntimeError(
                f"Servo error: {self.packetHandler.getRxPacketError(error)}"
            )
        return model_number

    def is_moving(self, id: int) -> bool:
        """
        Determine if the servo is currently moving.

        Args:
            id (int): ID of the servo.
        Returns:
            bool: True if the servo is moving, False otherwise.
        """
        moving, comm_result, error = self.packetHandler.ReadMoving(id)
        if comm_result != COMM_SUCCESS:
            raise RuntimeError(
                f"Communication error: {self.packetHandler.getTxRxResult(comm_result)}"
            )
        if error != 0:
            raise RuntimeError(
                f"Servo error: {self.packetHandler.getRxPacketError(error)}"
            )

        return moving != 0

    def set_speed(self, id: int, speed: int):
        """
        Set the speed of the servo.

        Args:
            id (int): ID of the servo.
            speed (int): Speed value (0-100).
        """
        if speed < 0 or speed > 100:
            raise ValueError(f"Speed must be between 0 and 100")

        # Map speed from 0-100 to 1-2048
        servo_speed = int(
            self.MIN_SPEED + (speed / 100) * (self.MAX_SPEED - self.MIN_SPEED)
        )

        comm_result, error = self.packetHandler.WriteSpeed(id, servo_speed)
        if comm_result != COMM_SUCCESS:
            raise RuntimeError(
                f"Communication error: {self.packetHandler.getTxRxResult(comm_result)}"
            )
        if error != 0:
            raise RuntimeError(
                f"Servo error: {self.packetHandler.getRxPacketError(error)}"
            )

    def move_angle(self, id: int, angle: int, center_pos: int = CENTER_POSITION):
        """
        Set the angle of the servo.

        Args:
            id (int): ID of the servo.
            degree (int): Angle value in degrees (-150 - +150).
        """
        if angle < self.MIN_DEGREE or angle > self.MAX_DEGREE:
            raise ValueError(f"Angle must be between -150 and +150 degrees")

        center_offset = center_pos - self.CENTER_POSITION
        position = int(((angle + 150) / 300) * (self.MAX_POSITION - self.MIN_POSITION))
        position = center_offset + position

        comm_result, error = self.packetHandler.WritePosition(id, position)
        if comm_result != COMM_SUCCESS:
            raise RuntimeError(
                f"Communication error: {self.packetHandler.getTxRxResult(comm_result)}"
            )
        if error != 0:
            raise RuntimeError(
                f"Servo error: {self.packetHandler.getRxPacketError(error)}"
            )

    # Descructor to ensure port is closed when the object is deleted
    def __del__(self):
        self.portHandler.closePort()
