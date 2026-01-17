# MiQ Hand Wiring Guide

## CSI Camera
- Ribbon cable to CM4 CSI port (15-pin)
- Enable in raspi-config → Interface → Camera → Yes

## 4” Touch e-Paper
- SPI: MOSI GPIO10, SCLK GPIO11, CS GPIO8, DC GPIO25, RST GPIO17, BUSY GPIO24
- Touch I2C: SDA GPIO2, SCL GPIO3
- VCC 3.3V, GND

## DRV2605 Haptics (LRA motor)
- I2C: SDA GPIO2, SCL GPIO3
- VCC 3.3V/5V, GND

## Solar Power Chain
- Solar panel → diode (1N5819 cathode to TP4056 IN+) → TP4056 IN-
- TP4056 BAT+ / BAT- → LiPo battery
- Battery + → boost IN+
- Battery - → boost IN-
- Boost 5V → CM4 5V pins
- Switch on 5V line for manual kill

## Recessed LED Halo (optional)
- WS2812B strip (data to GPIO18, 5V/GND from boost)
- Or simple LEDs → MOSFET gate to GPIO18, drain to LED-, source to GND

## RFID Reader (MFRC522 for relic disc)
- SPI: MOSI GPIO10, MISO GPIO9, SCLK GPIO11, CS GPIO8, RST GPIO25
- VCC 3.3V, GND
