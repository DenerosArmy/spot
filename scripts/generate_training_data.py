"""Saves test samples"""
from SimpleCV import Camera
c = Camera(0)
name = raw_input("Object Name: ")
i = 0
print "Press [enter] to take another image, or use [q] to exit."
while raw_input() != "q":
    img = c.getImage()
    img.save("/Users/jian/Projects/Pinkie/training_data/{0}_{1}.jpg".format(name, i))
    print "Saved image ", i
    i += 1
    print "Press [enter] to take another image, or use [q] to exit."
print "Successfully saved data for {0}.".format(name)
