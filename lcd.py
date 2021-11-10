from burglar_alarm.PCF8574 import PCF8574_GPIO
from burglar_alarm.Adafruit_LCD1602 import Adafruit_CharLCD
from time import sleep
from datetime import datetime

num = 1
def loop():
    global num
    mcp.output(3,1)
    lcd.begin(16, 2)
    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.message(f"BURGLAR-ALARM")

def destory():
    lcd.clear()

PCF8574_address = 0x27
PCF8574A_address = 0x3F

try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)

lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == "__main__":
    print("STARTED lcd.py...")
    try:
        loop()
    except KeyboardInterrupt:
        destory()