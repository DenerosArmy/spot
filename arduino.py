import serial


class LazrSystem(object):

    def __init__(self, port='/dev/ttyACM0', bps=9600):
        self.ser = serial.Serial(port, bps)
        self.mode = False

    def charge(self, mode):
        if mode != self.mode:
            self.ser.write("on/" if mode else "off/")
            self.mode = mode

    def aim(self, x, y):
        self.ser.write("aim/")
        pan = x
        tilt = y
        self.ser.write(chr(pan) + "/" + chr(tilt) + "/")

    def line(self, x1, y1, x2, y2, speed = 5):
        self.ser.write("line/")
        pan1 = x1
        tilt1 = y1
        pan2 = x2
        tilt2 = y2
        self.ser.write(chr(pan1) + "/" + chr(tilt1) + "/" + chr(pan2) + "/" + chr(tilt2) + "/" + chr(speed) + "/")
