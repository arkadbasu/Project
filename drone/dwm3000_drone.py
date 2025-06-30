import spidev
import RPi.GPIO as GPIO
import time
import math

SPI_BUS = 0
CS_PINS = [8, 7]  # Two DWM3000 modules
IRQ_PINS = [17, 27]

spis = [spidev.SpiDev(), spidev.SpiDev()]
for i, spi in enumerate(spis):
    spi.open(SPI_BUS, i)
    spi.max_speed_hz = 1000000

GPIO.setmode(GPIO.BCM)
for cs in CS_PINS:
    GPIO.setup(cs, GPIO.OUT)
for irq in IRQ_PINS:
    GPIO.setup(irq, GPIO.IN)

def send_poll(spi, cs_pin):
    GPIO.output(cs_pin, GPIO.LOW)
    spi.xfer2([0x10, 0x01, 0x02, 0x03])  # Example poll frame
    GPIO.output(cs_pin, GPIO.HIGH)
    print(f"Poll sent from CS{cs_pin}")

def wait_for_response(spi, cs_pin, timeout=0.1):
    start = time.time()
    while time.time() - start < timeout:
        GPIO.output(cs_pin, GPIO.LOW)
        resp = spi.xfer2([0x20, 0x00, 0x00, 0x00])  # Example read
        GPIO.output(cs_pin, GPIO.HIGH)
        if resp[0] == 0x20:
            print(f"Response received on CS{cs_pin}:", resp)
            return time.time()
        time.sleep(0.01)
    print(f"No response on CS{cs_pin}")
    return None

def calculate_distance(t1, t2):
    c = 299702547  # m/s
    tof = t2 - t1
    return (tof * c) / 2

def calculate_angle(d1, d2, separation):
    # d1, d2: distances from each module; separation: distance between modules
    try:
        angle = math.acos((d1**2 + separation**2 - d2**2) / (2 * d1 * separation))
        return math.degrees(angle)
    except:
        return None

SEPARATION = 0.2  # meters between two modules (adjust for your setup)

try:
    t1 = time.time()
    send_poll(spis[0], CS_PINS[0])
    t2 = wait_for_response(spis[0], CS_PINS[0])
    send_poll(spis[1], CS_PINS[1])
    t3 = wait_for_response(spis[1], CS_PINS[1])
    if t2 and t3:
        d1 = calculate_distance(t1, t2)
        d2 = calculate_distance(t1, t3)
        angle = calculate_angle(d1, d2, SEPARATION)
        print(f"Distance1: {d1:.2f} m, Distance2: {d2:.2f} m, Angle: {angle:.2f} deg")
except Exception as e:
    print("Error:", e)
finally:
    for spi in spis:
        spi.close()
    GPIO.cleanup()