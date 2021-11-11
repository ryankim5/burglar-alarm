from burglar_alarm.PCF8574 import PCF8574_GPIO
from burglar_alarm.errors.errors import I2CNotFoundError
from burglar_alarm.Adafruit_LCD1602 import Adafruit_CharLCD
from time import sleep
from datetime import datetime


PCF8574_address = 0x27
PCF8574A_address = 0x3F

class LCD:
    def __init__(self, mcp_output, begin):
        self.mcp1, self.mcp2 = mcp_output
        self.begin1, self.begin2 = begin
        try:
            self.mcp = PCF8574_GPIO(PCF8574_address)
        except:
            try:
                self.mcp = PCF8574_GPIO(PCF8574A_address)
            except:
                raise I2CNotFoundError("I2C of LCD is not found. Please check connection of wires.")
        self.lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=self.mcp)
    
    def display(self, message, cursor, clear=True):
        """LCD.display(message, cursor, clear=True)
        The display function allows you to display text on a LCD."""
        self.mcp.output(self.mcp1, self.mcp2)
        self.lcd.begin(self.begin1, self.begin2)
        x, y = cursor
        if clear:
            self.lcd.clear()
        self.lcd.setCursor(x, y)
        self.lcd.message(message)