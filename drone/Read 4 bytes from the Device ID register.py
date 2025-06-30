# Register address for DEV_ID
DEV_ID_ID = 0x03  # Device ID register

# Send read command (MSB = 0 means READ), and 4 dummy bytes to clock out the response
resp = spi.xfer2([DEV_ID_ID & 0x7F, 0x00, 0x00, 0x00, 0x00])
device_id = resp[1:]  # Discard the first byte (echoed command), get 4 bytes of response

# Print Device ID
print("Device ID:", device_id)
print("Hex:", "0x" + ''.join(f"{b:02X}" for b in device_id))
