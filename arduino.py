import serial
import time
import math
import scipy as sp

class Lazr(object):
    def __init__(self, port='/dev/ttyACM0', bps=9600):
        self.ser = serial.Serial(port, bps)
        self.ser.flush()
        
    def lamp(self, mode):
		self.ser.write("/start/lampon/\n" if mode else "/start/lampoff/\n")
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
        X, Y = (960, 1500) # Coordinates of the camera mount, in img coordinates
        scale_x, scale_y = (85.0, 28.0) # number of pixels per cm
        height = 50 # height of the stand, in cm
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
        theta = clamp(theta, 0, 40)
        theta = 40 - theta

        phi = clamp(phi, 0, 180)
        phi = phi

        # return int(theta), int(phi)
        return int(phi), int(theta)

    def aim_to_xy_nn(self, x, y, cache=[]):
        """Aim to x/y using nearest-neighbor algorithm"""
        if len(cache) == 0:
            with open("laser.calibration", "r") as f:
                import pickle
                cache.append(pickle.load(f))
        d = cache[0]

        x_, y_ = None, None
        r_ = float('inf')
        for xx, yy in d:
            r = math.sqrt((x-xx)**2 + (y-yy)**2)
            if r < r_:
                r_ = r
                x_, y_ = xx, yy
        print "Aiming to", d[x_, y_]
        self.aim(*d[x_, y_])

    def aim_to_xy(self, x, y, cache=[]):
        """Aim to x/y using spline interpolation algorithm"""
        if not cache:
            with open("laser.calibration", "r") as f:
                import pickle
                d = pickle.load(f)

                items = d.items()
                keys = [i[0] for i in items]
                keys_x = [k[0] for k in keys]
                keys_y = [k[1] for k in keys]
                vals = [i[1] for i in items]
                vals_x = [k[0] for k in vals]
                vals_y = [k[1] for k in vals]

                spline_x = sp.interpolate.bisplrep(keys_x, keys_y, vals_x)
                spline_y = sp.interpolate.bisplrep(keys_x, keys_y, vals_y)
                cache.extend([spline_x, spline_y])

        spline_x, spline_y = cache
        theta = int(sp.interpolate.bisplev(x, y, spline_x))
        phi = int(sp.interpolate.bisplev(x, y, spline_y))

        if theta < 0:
            theta = 0
        elif theta > 179:
            theta = 179

        if phi < 0:
            phi = 0
        elif phi > 40:
            phi = 40

        print "Aiming to", theta, phi
        self.aim(theta, phi)

l = Lazr()
