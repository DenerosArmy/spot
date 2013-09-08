from arduino import l
from SimpleCV import *
import settings
import time
import random

camera = SimpleCV.Camera(settings.camera_index)
display = SimpleCV.Display(camera.getImage().size())

def get_mapping(theta, phi):
    assert 0 <= theta <= 180
    assert 0 <= phi < 40

    img = camera.getImage()
    binarized = img.splitChannels()[0].binarize(250).invert()
    blobs = binarized.findBlobs(minsize=1)
    if not blobs or len(blobs) != 1:
        return None, None
    x, y = blobs[0].centroid()
    x = int(x)
    y = int(y)
    return x, y


def get_positions():
    for x in range(60, 115, 5):
        for y in range(0, 30, 3):
            yield (x, y)


positions = list(get_positions())
random.shuffle(positions)
x, y, theta, phi = None, None, None, None

num = 25

d = {}
import os, pickle
if os.path.exists("laser.calibration"):
    d = pickle.load(open("laser.calibration", "r"))

def save(x, y, theta, phi):
    d[(x, y)] = (theta, phi)
    pickle.dump(d, open("laser.calibration", "w"))

tried = False
while not display.isDone():
    if num > 0:
        num -= 1
    if theta is None:
        if positions:
            while theta is None:
                theta, phi = positions.pop()
                if (theta, phi) in d:
                    theta, phi = None, None
            l.aim(theta, phi)
            time.sleep(0.2)
            l.aim(theta, phi)
        else:
            raise SystemExit
    if theta is not None and x is None:
        x, y = get_mapping(theta, phi)
    img = camera.getImage()
    # img.save(display)
    img2 = (img * 0.5 + img.splitChannels()[0].binarize(240).invert() * 0.5)
    if x is not None:
        img2.drawCircle((x, y), 10, Color.CYAN, thickness=2)
    img2.save(display)
    if num > 0:
        pass
    elif display.mouseLeft and x is not None:
        save(x, y, theta, phi)
        print "X, Y, theta, phi", x, y, theta, phi
        x, y, theta, phi = None, None, None, None
        num = 25
        (img * 0.0).save(display)
        time.sleep(0.1)
    elif display.mouseRight:
        x, y = get_mapping(theta, phi)
        if x is None:
            x, y = display.mouseX, display.mouseY
    elif display.mouseMiddle:
        l.aim(theta, phi)

