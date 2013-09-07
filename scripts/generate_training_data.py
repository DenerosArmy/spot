"""Saves test samples"""
from SimpleCV import Camera
import os
c = Camera(int(raw_input("Camera index:")))
name = raw_input("Object Name: ")
if os.environ["USER"] == "nikita":
    base_path = "/home/nikita/dev/pinkie/"
else:
    base_path = "/Users/jian/Projects/Pinkie/"
os.mkdir(os.path.join(base_path, "training_data", name))
i = 0
print "Press [enter] to take another image, or use [q] to exit."
while raw_input() != "q":
    img = c.getImage()
    img.save(os.path.join(base_path, "training_data", name, "{}.jpg".format(i)))
    print "Saved image ", i
    i += 1
    print "Press [enter] to take another image, or use [q] to exit."
print "Successfully saved data for {0}.".format(name)
