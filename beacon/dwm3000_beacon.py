import spidev
import RPi.GPIO as GPIO
import time

SPI_BUS = 0
SPI_DEVICE = 0
CS_PIN = 8
IRQ_PIN = 17

spi = spidev.SpiDev()
spi.open(SPI_BUS, SPI_DEVICE)
spi.max_speed_hz = 1000000

GPIO.setmode(GPIO.BCM)
GPIO.setup(CS_PIN, GPIO.OUT)
GPIO.setup(IRQ_PIN, GPIO.IN)

def read_poll():
    GPIO.output(CS_PIN, GPIO.LOW)
    poll = spi.xfer2([0x10, 0x00, 0x00, 0x00])  # Example: read poll frame
    GPIO.output(CS_PIN, GPIO.HIGH)
    return poll

def send_response():
    GPIO.output(CS_PIN, GPIO.LOW)
    spi.xfer2([0x20, 0xAA, 0xBB, 0xCC])  # Example: send response frame
    GPIO.output(CS_PIN, GPIO.HIGH)
    print("Response sent")

try:
    print("Beacon ready, waiting for poll...")
    while True:
        poll = read_poll()
        if poll[0] == 0x10:  # Example poll frame check
            print("Poll received:", poll)
            send_response()
        time.sleep(0.01)
except KeyboardInterrupt:
    pass
finally:
    spi.close()
    GPIO.cleanup()