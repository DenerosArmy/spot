from arduino import Lazr
from vision import ContourClassifier
import scipy
import settings
import os


class Index(object):

    def __init__(self):
        self.lazr = Lazr()
        self.vsys = ContourClassifier()

    def take_picture(self, filename):
        retval, img_arr = self.vsys.cam.read()
        scipy.misc.imsave(os.path.join(settings.base_path,'pics',filename), img_arr)

    def point_at_coordinates(self, x, y):
        self.lazr.charge(True)
        self.lazr.aim_to_xy(x, y)

    def point_at_obj(self, obj):
        state = self.vsys.get_state(obj)
        if state:
            self.point_at_coordinates(state[0], state[1])

    def step(self):
        return self.vsys.step()

if __name__ == '__main__':
    idx = Index()
    idx.lazr.charge(False)
    #while idx.step():
	#idx.point_at_obj("key")
