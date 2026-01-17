from adafruit_drv2605 import DRV2605
import board
import busio
import time

i2c = busio.I2C(board.SCL, board.SDA)
drv = DRV2605(i2c)

print("Testing haptic patterns...")

# Single tick (step)
drv.sequence = [1]
drv.play()
time.sleep(0.5)

# Double confirm
drv.sequence = [1, 0.08, 1]
drv.play()
time.sleep(0.5)

# Triple success
drv.sequence = [1, 0.06, 1, 0.06, 1]
drv.play()
time.sleep(0.5)

# Long warning buzz
drv.sequence = [14]
drv.play()
time.sleep(1)

print("Test complete")
