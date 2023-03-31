import time
import serial


def waitForByte(serial_port: serial.Serial, timeout_cnt: int = 1000) -> int:
    timeout = 0
    while serial_port.in_waiting < 1:
        timeout += 1
        if timeout > timeout_cnt:
            return None
        time.sleep(0.000008)  # Wait for 8 microseconds
    return serial_port.read()[0]