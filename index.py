from arduino import LazrSystem
from vision import VisionSystem


class Index(object):

    def __init__(self):
        self.lazr = LazrSystem()
        self.vsys = VisionSystem()

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
