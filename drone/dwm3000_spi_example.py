import spidev
import RPi.GPIO as GPIO
import time
import numpy as np

# Example SPI setup for DWM3000
SPI_BUS = 0
SPI_DEVICE = 0  # Use 0 or 1 for each DWM3000
CS_PIN = 8      # GPIO8 (CE0) or GPIO7 (CE1)
IRQ_PIN = 17    # Example GPIO for IRQ

# Initialize SPI
spi = spidev.SpiDev()
spi.open(SPI_BUS, SPI_DEVICE)
spi.max_speed_hz = 1000000

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(CS_PIN, GPIO.OUT)
GPIO.setup(IRQ_PIN, GPIO.IN)

# Example: Read device ID
GPIO.output(CS_PIN, GPIO.LOW)
resp = spi.xfer2([0xde, 0xca, 0x00, 0x01])  # Before it was 0x00, 0x00, 0x00, 0x00
GPIO.output(CS_PIN, GPIO.HIGH)
print('DWM3000 response:', resp)

def send_poll(spi, cs_pin):
    # Send a TWR poll message (replace with actual DWM3000 TX command)
    GPIO.output(cs_pin, GPIO.LOW)
    spi.xfer2([0x01, 0x02, 0x03, 0x04])  # Example poll frame
    GPIO.output(cs_pin, GPIO.HIGH)
    print('Poll sent')

def wait_for_response(spi, cs_pin, timeout=0.1):
    # Wait for a TWR response (replace with actual DWM3000 RX command)
    start = time.time()
    while time.time() - start < timeout:
        GPIO.output(cs_pin, GPIO.LOW)
        resp = spi.xfer2([0xde, 0xca, 0x00, 0x01])  # Change to actual
        GPIO.output(cs_pin, GPIO.HIGH)
        if resp[0] != 0x00:
            print('Response received:', resp)
            return time.time()
        time.sleep(0.01)
    print('No response received')
    return None

def calculate_distance(t1, t2):
    # t1: time poll sent, t2: time response received
    # In real TWR, use device timestamps and clock calibration
    tof = t2 - t1
    c = 299702547  # speed of light in m/s
    distance = (tof * c) / 2
    return distance

try:
    t1 = time.time()
    send_poll(spi, CS_PIN)
    t2 = wait_for_response(spi, CS_PIN)
    if t2:
        distance = calculate_distance(t1, t2)
        print(f"Estimated distance: {distance:.2f} meters (mocked)")
except Exception as e:
    print('Error:', e)
finally:
    spi.close()
    GPIO.cleanup()
