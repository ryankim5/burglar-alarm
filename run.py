from burglar_alarm import lcd, Keypad, wait, distance, buzzer
from datetime import datetime
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

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
inputed_password = ""
mode = ""

# Distance Sensor Settings
trigPin = 40
echoPin = 37
MAX_DISTANCE = 220
timeOut = MAX_DISTANCE * 60


# Buzzer Settings
is_buzzing = False
buzzerPin = 29


def loop():
    global password, armed, mode, inputed_password, is_buzzing, passwd
    display = lcd.LCD((3, 1), (16, 2))
    keypad = Keypad.MatrixKeypad(
        DEBOUNCE_TIME, ROWS, COLS, KEYS, ROWSPINS, COLSPINS)
    distanceSensor = distance.DistanceSensor(
        echoPin, trigPin, MAX_DISTANCE, timeOut)
    bzr = buzzer.Buzzer(buzzerPin)
    if armed:
        display.display("ARMED")
    else:
        display.display("UNARMED")
    while True:
        cm_far = distanceSensor.getDistance()
        key_pressed = keypad.findPressedKey()
        # if key_pressed:
        #     display.display("KEYPAD PRESSED")
        #     display.display(f"KEY: {key_pressed}", (0, 1), clear=False)
        #     break
        if key_pressed == "A":
            mode = "a"

        if key_pressed == "B":
            mode = "b"

        if mode == "a":
            display.display("SECURITY MODE")
            while True:
                inputed_password = ""
                if mode != "a":
                    break

                key_pressed = keypad.findPressedKey()
                if key_pressed == "*":
                    if not armed:
                        display.display("Enter your")
                        display.display("new passcode...", (0, 1), clear=False)
                        while True:
                            if mode != "a":
                                break

                            key_pressed = keypad.findPressedKey()
                            if key_pressed in ["A", "B", "C", "D"]:
                                display.display("Numbers Only")
                            elif key_pressed == "#":
                                if not password:
                                    display.display("Passphrase should")
                                    display.display(
                                        "be not empty...", (0, 1), clear=False)
                                else:
                                    armed = True
                                    mode = ""
                                    display.display(
                                        "ARMED" if armed else "UNARMED")
                            else:
                                if key_pressed:
                                    password += key_pressed
                    else:
                        display.display("Please enter")
                        display.display("passphrase...", (0, 1), clear=False)
                        while True:
                            if mode != "a":
                                break

                            key_pressed = keypad.findPressedKey()
                            if key_pressed in ["A", "B", "C", "D"]:
                                display.display("Numbers Only")
                            elif key_pressed == "#":
                                if not password:
                                    display.display("Passphrase should")
                                    display.display(
                                        "be not empty...", (0, 1), clear=False)
                                else:
                                    if inputed_password == password:
                                        armed = False
                                        mode = ""
                                        display.display(
                                            "ARMED" if armed else "UNARMED")
                                    else:
                                        mode = ""
                                        display.display(
                                            "WRONG PASS" + "-" + "ARMED" if armed else "UNARMED")
                            else:
                                if key_pressed:
                                    inputed_password += key_pressed
        elif mode == "b":
            inputed_password = ""
            if not is_buzzing:
                msg = 'ARMED' if armed else 'UNARMED'
                display.display(f"BZR NT-{msg}")
                mode = ""
            else:
                display.display("Password...")
                while True:
                    if mode != "b":
                        break

                    key_pressed = keypad.findPressedKey()
                    if key_pressed in ["A", "B", "C", "D"]:
                        display.display("Numbers Only")
                    elif key_pressed == "#":

                        if not password:
                            display.display("Passphrase should")
                            display.display(
                                "be not empty...", (0, 1), clear=False)
                        else:
                            if inputed_password == password:
                                mode = ""
                                display.display("BZR OFF")
                                is_buzzing = False
                            else:
                                mode = ""
                                display.display(
                                    "WRONG PASS" + "-" + "ARMED" if armed else "UNARMED")
                    else:
                        if key_pressed:
                            inputed_password += key_pressed

        time_now = datetime.now()
        hour, minute, second = (
            time_now.hour, time_now.minute, time_now.second)
        hour, minute, second = str(hour), str(minute), str(second)
        if len(hour) == 1:
            hour = "0" + hour
        if len(minute) == 1:
            minute = "0" + minute
        if len(second) == 1:
            second = "0" + second
        display.display(f"TIME: {hour}:{minute}:{second}", (0, 1), clear=False)

        if armed:
            if cm_far > 10:
                is_buzzing = True

        if is_buzzing:
            bzr.on()
        else:
            bzr.off()


def destroy():
    exit(1)
    GPIO.cleanup()


if __name__ == "__main__":
    try:
        print("Running run.py...")
        loop()
    except KeyboardInterrupt:
        destroy()
