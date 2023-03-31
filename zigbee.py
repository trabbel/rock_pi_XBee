START_DELIMITER = 0x7e

def writeFrame(frame: bytearray, addr16: int, addr64: int, payload: bytearray, payloadSize: int) -> int:
    # Define a temporary array of sufficient size for everything that may be escaped
    tempFrame = bytearray(17 + payloadSize)
    # Frame delimiter
    frame[0] = START_DELIMITER
    # Payload length starting with frame type byte, excluding checksum and necessary escape characters
    frame_len = 0x0E + payloadSize
    tempFrame[0] = (frame_len >> 8) & 0xFF
    tempFrame[1] = frame_len & 0xFF
    # API ID (TX request)
    tempFrame[2] = 0x10
    # Frame ID
    tempFrame[3] = 0x01
    # 64-bit destination address
    for i in range(8):
        tempFrame[4+i] = (addr64 >> (7-i)*8) & 0xFF
    # 16-bit address
    tempFrame[12] = (addr16 >> 8) & 0xFF
    tempFrame[13] = (addr16 >> 0) & 0xFF
    # Broadcast radius
    tempFrame[14] = 0x00
    # Options
    tempFrame[15] = 0x00
    # Payload
    tempFrame[16:16+payloadSize] = payload[:]
    # Checksum is calculated based on the original data (non-escaped payload),
    # starting with the frame type
    checksum = 0x00
    for i in range(2, 16+payloadSize):
        checksum += tempFrame[i]
    tempFrame[16+payloadSize] = 0xFF - (checksum%255)
    # Escape the payload and count how many additional escape characters have to be transmitted
    escapes = escapePayload(tempFrame, frame, payloadSize)

    '''for i in range(18+payloadSize+escapes):
            debug("%02x " % tempFrame[i], end="")
    debug("\n")'''

    # The frame is now written in the buffer and ready to send
    return 18 + payloadSize + escapes


def escapePayload(payload: bytearray, tx_buf: bytearray, payloadSize: int) -> int:
    # Counter for needed escape characters
    escapes = 0
    # Where to start writing the payload in the buffer
    pos = 1
    # Go through each payload byte
    for i in range(17 + payloadSize):
        # Check if the current byte has to be escaped
        # 0x7e         | frame delimiter, signifies a new frame
        # 0x7d         | escape character, signifies that the next character is escaped
        # 0x11, 0x13   | software control character
        if payload[i] == 0x7E or payload[i] == 0x7D or payload[i] == 0x11 or payload[i] == 0x13:
            # If a byte has to be escaped, first write 0x7d, followed by the byte XORed with 0x20
            tx_buf[pos] = 0x7D
            tx_buf[pos+1] = payload[i] ^ 0x20
            pos += 2
            escapes += 1
        else:
            # Otherwise write the byte
            tx_buf[pos] = payload[i]
            pos += 1
    return escapes