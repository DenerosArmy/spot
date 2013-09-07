import serial
import time

class Lazr:
    def __init__(self, port='/dev/ttyACM1', bps=9600):
        self.ser = serial.Serial(port, bps)
        self.ser.flush()

    def charge(self, mode):
        self.ser.write("/start/on/\n" if mode else "/start/off/\n")
        self.ser.flush()
    
    def aim(self, x, y):
        pan = x
        tilt = y
        self.ser.write("/start/aim/" + chr(pan) + chr(tilt) + "/\n")
        
    def line(self, x1, y1, x2, y2, time=1, dt=10):
        pan1 = x1
        tilt1 = y1
        pan2 = x2
        tilt2 = y2
        self.ser.write("/start/line/" + chr(pan1) + chr(tilt1) + chr(pan2) + chr(tilt2) + chr(time) + chr(dt) + "/\n")
        self.ser.flush()
        self.ser.read
        
    def debug(self, command):
	    self.ser.write(command)
	    self.ser.flush()
	    
