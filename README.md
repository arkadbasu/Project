# Two-Way Ranging (TWR) with DWM3000 Modules on Raspberry Pi

## Overview
This project enables TWR between two Raspberry Pi devices using DWM3000 UWB modules. The drone is equipped with two DWM3000 modules for distance and angle calculation, while the beacon uses one DWM3000 module.

## Structure
- `drone/`: Code for the drone (two DWM3000 modules)
- `beacon/`: Code for the beacon (one DWM3000 module)

## Features
- SPI communication with DWM3000
- TWR protocol implementation
- Distance and angle calculation for drone landing

## Setup Instructions
1. Wire the DWM3000 modules to the Raspberry Pi SPI interface (see below).
2. Install required Python packages: `spidev`, `RPi.GPIO`, `numpy`.
3. Run the example scripts in `drone/` and `beacon/`.

## DW3000 Driver Library
Qorvo’s DW3000 API in C is required for full TWR, because:

Timestamp registers are 40-bit and not easily SPI-readable in Python

Correct frame format, ranging response logic, and error handling are all embedded

git clone https://github.com/lucasbernal/dwm3000-raspberrypi.git
cd dwm3000-raspberrypi
mkdir build && cd build
cmake ..
make

## Wiring Diagram
- **DWM3000 <-> Raspberry Pi**
  - VCC  <-> 3.3V
  - GND  <-> GND
  - SCK  <-> SPI SCLK (GPIO 11)
  - MOSI <-> SPI MOSI (GPIO 10)
  - MISO <-> SPI MISO (GPIO 9)
  - CS   <-> SPI CE0 (GPIO 8) or CE1 (GPIO 7)
  - IRQ  <-> Any available GPIO (for interrupts)

## Notes
- Ensure SPI is enabled on the Raspberry Pi (`raspi-config`).
- Use separate CS pins for each DWM3000 on the drone.

## References
- [DWM3000 Datasheet](https://www.qorvo.com/products/p/DWM3000)
- [Raspberry Pi SPI Documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#spi)
