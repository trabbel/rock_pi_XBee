from zigbee import writeFrame, readFrame
from utils import waitForByte
import serial
import time
import threading

string = "test~"
payload = bytearray()
payload.extend(string.encode())
print(payload)
tx_buf = bytearray(300)
rx_buf = bytearray(300)

xbee = serial.Serial('/dev/ttyS1', 115200)

length = writeFrame(tx_buf, 0xFFFE, 0x0013a20041f223b8, payload, len(payload))
print(tx_buf[:length])
print(length)

def receive():
     while True:
         if xbee.in_waiting >0:
              rx_callback(rx_buf)



def rx_callback(buffer):
    length = 0
    c = b''
    timeoutCnt = 0
    # Wait until a frame delimiter arrives
    while xbee.in_waiting > 0 and c != b'\x7E':
        c = xbee.read()

    if c != b'\x7E':
        return

    # Parse the frame. In case of an error, a negative length
    # is returned
    result = readFrame(xbee, buffer)
    length = result[1]#.length

    print(f"Payload Size: {length}")

    if length <= 0:
        return

    for i in range(length):
        print(f"{buffer[i]:02x}", end='')
    print()

    if result[0] == 0x90:
        print(f"{buffer[12:length].decode('utf-8')}")


thread = threading.Thread(target=receive)
thread.start()

while True:
    xbee.write(tx_buf[:length])
    time.sleep(2)