import mfrc522
import time

reader = mfrc522.MFRC522()

print("Place relic disc near reader...")

while True:
    (status, tag_type) = reader.MFRC522_Request(reader.PICC_REQIDL)
    if status == reader.MI_OK:
        print("Disc detected")
        # Read data (simplified)
        (status, uid) = reader.MFRC522_Anticoll()
        if status == reader.MI_OK:
            print("UID:", [hex(i) for i in uid])
        # Write example data
        # reader.MFRC522_Write("MIQ:TEST:SAVE")
        break
    time.sleep(0.5)
