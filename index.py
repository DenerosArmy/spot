from arduino import Lazr
from vision import ContourClassifier
import scipy
import settings


class Index(object):

    def __init__(self):
        self.lazr = LazrSystem()
        self.vsys = ContourClassifier()

    def take_picture(self, filename):
        retval, img_arr = self.vsys.cam.read()
        scipy.misc.imsave(settings.base_path+'pics/'+filename, image_array)

    def point_at_coordinates(self, x, y):
        self.lazr.charge(True)
        self.lazr.aim(x, y)

    def point_at_obj(self, obj):
        state = self.vsys.get_state(obj)
        if state:
            self.point_at_coordinates(state[0], state[1])

    def step(self):
        return self.vsys.step()

if __name__ == '__main__':
    idx = Index()
    while idx.step():
        pass
