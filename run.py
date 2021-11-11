from burglar_alarm import lcd, Keypad

def loop():
    display = lcd.LCD((3, 1), (16, 2))
    display.display("Burglar Alarm", (0, 0))
if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt:
        destroy()