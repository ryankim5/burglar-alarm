import RPi.GPIO as GPIO
from time import sleep


class Buzzer:
    def __init__(self, buzzerPin):
        self.pin = buzzerPin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(buzzerPin, GPIO.OUT)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)
