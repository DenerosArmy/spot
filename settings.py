import os
import glob

if os.environ["USER"] == "nikita":
    base_path = "/home/nikita/dev/pinkie/"
    # Get the highest-index camera available
    camera_index = sorted(glob.glob("/dev/video*"))[-1][10:]
else:
    base_path = "/Users/jian/Projects/Pinkie/"
    camera_index = sorted(glob.glob("/dev/video*"))[-1][10:]

camera_index = int(camera_index)
