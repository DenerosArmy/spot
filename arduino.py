import serial
ser = serial.Serial('/dev/tty.usbmodem1411', 9600)
ser.write("tits123")
