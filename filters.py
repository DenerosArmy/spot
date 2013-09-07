import math, random, collections
import numpy as np
from time import time
from SimpleCV import Camera, Color, Display
import settings
# from util import *

class VisionSystem(object):
    def __init__(self, dx=150, dy=150, overlap_factor=2):
        self.cam = Camera(settings.camera_index)
        self.img = self.cam.getImage()
        self.display = Display(self.img.size())

        self.dx = dx
        self.dy = dy
        self.overlap_factor = overlap_factor
        from train import classifier
        self.classifier = classifier

        self.objs = {}

    def step(self):
        if self.display.isDone():
            raise SystemExit, "Exiting"
        try:
            img = self.cam.getImage()
            self.add_observation(img, annotate=True)
            self.annotate_img(img)
            img.save(self.display)
            if self.display.mouseLeft or self.display.mouseRight:
                self.display.done = True
        except KeyboardInterrupt:
            self.display.done = True

    def add_observation(self, img, annotate=False):
        for x in xrange(0, img.width, self.dx/self.overlap_factor):
            if x + self.dx >= img.width:
                continue
            for y in xrange(0, img.height, self.dy/self.overlap_factor):
                if y + self.dy >= img.height:
                    continue
                im = img.crop(x, y, self.dx, self.dy)

                # l = 45
                # for extractor in self.classifier.mFeatureExtractors:
                #     val = extractor.extract(im)
                #     if not val:
                #         continue
                #     l -= len(extractor.extract(im))
                # if l > 0:
                #     print "Wrong feature length", l
                #     continue
                # print "classifying"
                obj = self.classifier.classify(im)
                # print "done classifying"

                observation = ((x+self.dx)/2, (y+self.dy)/2), 0.0

                if obj == "negative" or obj == "key":
                    continue
                elif obj in self.objs:
                    if annotate:
                        img.drawRectangle(x, y, self.dx/2, self.dy/2, Color.BLUE)
                        img.drawText(obj, x, y, Color.BLUE)
                    self.objs[obj].add_observation(observation)
                else:
                    self.objs[obj] = VisionObjectFilter(observation, img.width, img.height, label=obj)

    def annotate_img(self, img):
        for obj in self.objs:
            try:
                x, y = self.get_state(obj)
                x -= self.dx/2
                y -= self.dy/2
            except TypeError:
                continue
            img.drawRectangle(x, y, self.dx, self.dy, Color.RED)
            img.drawText(obj, x, y, Color.RED)

    def get_state(self, obj):
        if obj not in self.objs:
            return None
        try:
            (x, y), z = self.objs[obj].infer_state()
            return x, y
        except ValueError:
            return None

class VisionObjectFilter(object):
    def __init__(self, initial_observation, tracking_bounds_width, tracking_bounds_height, label="entity"):
        self.label = label
        self.observations = set()
        self.kalman_filter = KalmanFilter(initial_observation)
        self.last_obs_t = time()
        self.slack_time = 2

    def add_observation(self, observation):
        self.last_obs_t = time()
        self.observations.add(observation)

    def infer_state(self):
        if time() - self.last_obs_t > self.slack_time:
            return set()

        #detections = hard_filter(self.observations)
        #self.observations = set()
        #return detection.pop()

        #detection = self.kalman_filter.predict()
        #return detection

        # detections = hard_filter(self.observations)
        for observation in self.observations:
            self.kalman_filter.update(observation)
        self.observations = set()
        detection = self.kalman_filter.predict()
        return detection


class KalmanFilter(object):
  """
  s = state
  z = measurement
  u = acceleration
  """

  def __init__(self, initial_observation):
      self.prev_t = time()
      self.dt = 0
      self.u = np.matrix([[0],[0],[0]]) # Previous velocity
      self.C = np.matrix([[1,0,0,0,0,0],
                          [0,1,0,0,0,0],
                          [0,0,1,0,0,0]])
      self.C_transpose = self.C.transpose()
      # BEGIN CRAP: These shouldn't be constants
      self.ns = 0.1 # Process noise: Variability of how fast the tracked entity is moving (std of acceleration) # TWEAKME
      self.nz = 0.1 # Measurement noise: Variability of measurements (how bad the measurements are) (std of acceleration) # TWEAKME
      # END CRAP
      self.var_s = self.ns**2
      self.var_z = self.nz**2
      self.Ez = np.matrix([[self.var_z,0,0],
                           [0,self.var_z,0],
                           [0,0,self.var_z]])
      self.Es_est = np.zeros((6,6))
      self.s_est = np.matrix([[initial_observation[0][0]],[initial_observation[0][1]],[initial_observation[1]],[0],[0],[0]])
      self.I = np.identity(6)

  @property
  def A(self):
      return np.matrix([[1,0,0,self.dt,0,0],
                        [0,1,0,0,self.dt,0],
                        [0,0,1,0,0,self.dt],
                        [0,0,0,1,0,0],
                        [0,0,0,0,1,0],
                        [0,0,0,0,0,1]])

  @property
  def B(self):
      t2 = (self.dt**2)/2
      return np.matrix([[t2],[t2],[t2],[self.dt],[self.dt],[self.dt]])

  @property
  def Es(self):
      t2 = (self.dt**2)*self.var_s
      t3 = t2*(self.dt/2)
      t4 = (t2**2)/(4*self.var_s)
      return np.matrix([[t4,0,0,t3,0,0],
                        [0,t4,0,0,t3,0],
                        [0,0,t4,0,0,t3],
                        [t3,0,0,t2,0,0],
                        [0,t3,0,0,t2,0],
                        [0,0,t3,0,0,t2]])

  def compute_Es(self, a):
      ax = 0.001
      ay = 0.001
      ar = 0.00001
      #ax = float(a[0])**2 + self.ns
      #ay = float(a[1])**2 + self.ns
      #ar = (float(a[2])**2)*0.1 + 0.001
      #ar = float(a[2])**2 + self.ns
      t2 = self.dt**2
      t3 = t2*(self.dt/2)
      t4 = (t2**2)/4
      return np.matrix([[t4*ax,0,0,t3*ax,0,0],
                        [0,t4*ay,0,0,t3*ay,0],
                        [0,0,t4*ar,0,0,t3*ar],
                        [t3*ax,0,0,t2*ax,0,0],
                        [0,t3*ay,0,0,t2*ay,0],
                        [0,0,t3*ar,0,0,t2*ar]])

  @property
  def a(self): # Acceleration
      v = self.s_est[3:6]
      a = (v-self.u)/self.dt
      self.u = v
      return 0.01*a
      #return 1

  def predict(self):
      t = time()
      self.dt = t - self.prev_t
      self.prev_t = t
      A = self.A
      B = self.B
      a = self.a
      self.s_est = A * self.s_est + np.multiply(B, np.concatenate((a,a)))
      #self.Es_est = A * self.Es_est * A.transpose() + self.compute_Es(a)
      self.Es_est = A * self.Es_est * A.transpose() + self.Es

      # FIXME: Cleaner, more efficient way
      prediction = self.s_est.transpose().tolist()[0]
      return ((prediction[0], prediction[1]),max(0,prediction[2]))

  def update(self, observation):
      observation = np.matrix([[observation[0][0]], [observation[0][1]], [observation[1]]])
      K = self.Es_est * self.C_transpose * np.linalg.inv((self.C * self.Es_est * self.C_transpose) + self.Ez)
      self.s_est = self.s_est + K * (observation - (self.C * self.s_est))
      self.Es_est = (self.I - (K*self.C)) * self.Es_est
