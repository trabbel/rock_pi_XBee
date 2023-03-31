from zigbee import writeFrame

string = "test~"
payload = bytearray()
payload.extend(string.encode())
print(payload)
frame = bytearray(300)

length = writeFrame(frame, 0xFFFE, 0x0013a20041f217cc, payload, len(payload))
print(frame[:length])
print(length)