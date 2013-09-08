from arduino import l
from SimpleCV import *
import settings
import time
import random

camera = SimpleCV.Camera(settings.camera_index)
display = SimpleCV.Display(camera.getImage().size())

while not display.isDone():
	camera.getImage().save(display)
	if display.mouseLeft:
		x, y = display.mouseX, display.mouseY
		l.aim_to_xy(x, y)
