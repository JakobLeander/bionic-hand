import serial

SERIALPORT = "COM3"
serial_port = serial.Serial(SERIALPORT, 9600, timeout=1)

value_int = 0

while True:
    value_str = serial_port.readline().decode("utf-8").rstrip()
    try:
        value_int = int(value_str)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")

    print(value_int)
