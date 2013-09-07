"""
Saves test samples

Usage: python scripts/generate_training_data.py
"""
from SimpleCV import Camera
import os
import settings
c = Camera(settings.camera_index)
name = raw_input("Object Name: ")
base_path = settings.base_path
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
