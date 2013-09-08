import serial
import time
import math

class Lazr(object):

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
        self.ser.write(command + "\n")
        self.ser.flush()


    def convert_coordinates(self, x, y):
        X, Y = (300, 480) # Coordinates of the camera mount, in img coordinates
        scale_x, scale_y = (20.0, 20.0) # number of pixels per cm
        height = 10 # height of the stand, in cm
        x = x - X
        y = -(y - Y) # note how imgs have inverted y-coordinates

        # now rescale
        x /= scale_x
        y /= scale_y

        # convert to angular coordinates
        theta = math.atan(math.sqrt(x**2 + y**2) / height)
        phi = math.atan2(y, x)
        theta *= 180.0 / math.pi
        phi *= 180.0 / math.pi

        # Theta is angle upwards from the vertical, in the plane containing the y' axis
        # Phi is the angle from the y' axis in the direction of the x' axis

        #     y'
        #     ^
        #     |
        #     |
        #    base -----> x'

        # Additional transformations may be needed, depending on how the servos are mounted
        return theta, phi

    def convert_coordinates_2(self, x, y):
        theta, phi = self.convert_coordinates(x, y)
        def clamp(val, low, high):
            if val < low:
                return low
            elif val > high:
                return high
            return val
        theta = clamp(theta, 0, 90)
        theta = 90 - theta

        phi = clamp(phi, 0, 90)
        phi = phi + 90

        # return int(theta), int(phi)
        return int(phi), int(theta)

l = Lazr()
