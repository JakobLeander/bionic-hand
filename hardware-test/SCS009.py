# https://github.com/pollen-robotics/rustypot
# Servo debug tool: https://github.com/Robot-Maker-SAS/FeetechServo/blob/main/feetech%20debug%20tool%20master/FD1.9.8.2/FD.exe
# install and build rustypot python bindings: https://github.com/pollen-robotics/rustypot/tree/develop
# - Install rust
# - cargo run --release --bin stub_gen --features python
# maturin build --release --features python --features pyo3/extension-module
import numpy as np
import time

# rom rustypot import Scs0009PyController
from rustypot import Scs0009PyController

io = Scs0009PyController(
    serial_port="COM04",
    baudrate=1000000,
    timeout=0.5,
)
