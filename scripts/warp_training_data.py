"""
Saves test samples

Usage: python scripts/warp_training_data.py dir
"""
from SimpleCV import Image
import os, sys
import numpy as np

def warp(img):
	while True:
		warped = img.invert().shear([tuple(x) for x in np.random.random((4, 2)) * np.array(img.size())]).invert()
		if warped.hueHistogram()[0] < 0.8 * img.width * img.height:
			return warped

def rotate(img):
	return img.invert().rotate(np.random.rand() * 360).invert()

images = os.listdir(sys.argv[1])
images = [f for f in images if not (f.startswith("WARPED_") or f.startswith("ROTATED_"))]
num_images = len(images)

if False:
	warp_fn = warp
	warp_fn_name = "WARPED_"
else:
	warp_fn = rotate
	warp_fn_name = "ROTATED_"


for num, filename in enumerate(images):
	img = Image(os.path.join(sys.argv[1],filename))
	for i in range(10):
		warped = warp_fn(img)
		warped.save(os.path.join(sys.argv[1], warp_fn_name + filename + "_{}.jpg".format(i)))
	print "{}/{}".format(num+1, num_images)
