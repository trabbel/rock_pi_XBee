from zigbee import writeFrame
import serial
import time

string = "test~"
payload = bytearray()
payload.extend(string.encode())
print(payload)
frame = bytearray(300)

xbee = serial.Serial('/dev/ttyS1', 115200)

length = writeFrame(frame, 0xFFFE, 0x0013a20041f217cc, payload, len(payload))
print(frame[:length])
print(length)

while True:
    xbee.write(frame[:length])
    time.sleep(2)