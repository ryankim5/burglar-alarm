passphrase = ""
command = input("Please insert a command.")
if command == "A":
    second_command = input("Mode A. Please enter Second Command.")
    if second_command == "*":
        passphrase = input("New Passphrase:")
        print("OK")
else:
    print("Invalid Command")