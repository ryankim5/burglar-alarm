from burglar_alarm import lcd, Keypad
from datetime import datetime

# MatrixKeypad Settings
ROWS = 4
COLS = 4
KEYS = [
    '1', '2', '3', 'A',
    '4', '5', '6', 'B',
    '7', '8', '9', 'C',
    '*', '0', '#', 'D']
ROWSPINS = [12, 16, 18, 22]
COLSPINS = [19, 15, 13, 11]
DEBOUNCE_TIME = 50

# arming settings
armed = False
password = ""
mode = ""

def loop():
    global password, armed, mode
    display = lcd.LCD((3, 1), (16, 2))
    keypad = Keypad.MatrixKeypad(DEBOUNCE_TIME, ROWS, COLS, KEYS, ROWSPINS, COLSPINS)
    if armed:
        display.display("ARMED")
    else:
        display.display("UNARMED")
    while True:
        key_pressed = keypad.findPressedKey()
        # if key_pressed:
        #     display.display("KEYPAD PRESSED")
        #     display.display(f"KEY: {key_pressed}", (0, 1), clear=False)
        #     break
        if key_pressed == "A":
            mode = "a"
        
        if mode == "a":
            display.display("SECURITY MODE")
            while True:
                key_pressed = keypad.findPressedKey()
                if key_pressed == "*":
                    if not armed:
                        display.display("Enter your")
                        display.display("new passcode...", (0, 1), clear=False)
                        while True:
                            key_pressed = keypad.findPressedKey()
                            if key_pressed in ["A", "B", "C", "D"]:
                                display.display("Numbers Only")
                            elif key_pressed == "#":
                                if not password:
                                    display.display("Passphrase should")
                                    display.display("be not empty...", (0, 1), clear=False)
                                else:
                                    armed = True
                                    mode = ""
                            else:
                                if key_pressed:
                                    password += key_pressed
                    else:
                        display.display("Please enter passphrase...")
        time_now = datetime.now()
        hour, minute, second = (time_now.hour, time_now.minute, time_now.second)
        display.display(f"TIME: {hour}:{minute}:{second}", (0, 1), clear=False)


def destroy():
    exit(1)


if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt:
        destroy()