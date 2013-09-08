import os
import glob

tags = ["pen", "arduino", "key", "negative", "blank"]

if os.environ["USER"] == "nikita":
    base_path = "/home/nikita/dev/pinkie/"
    # Get the highest-index camera available
    camera_index = sorted(glob.glob("/dev/video*"))[-1][10:]
    use_simplecv_display = True
elif os.environ["USER"] == "jian":
    base_path = "/Users/jian/Projects/Pinkie/"
    #camera_index = sorted(glob.glob("/dev/video*"))[-1][10:]
    camera_index = 0
    use_simplecv_display = False

camera_index = int(camera_index)
