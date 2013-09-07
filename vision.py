import math, random, collections
import numpy as np
import time as tm
from SimpleCV import *
import cv
import cv2
import settings

class ContourClassifier(object):

    NEGATIVE_CLS = "negative"

    def __init__(self):
        self.cam = cv2.VideoCapture(settings.camera_index)
        from train import classifier
        self.classifier = classifier
        self.objs = {}

    def find_contours(self, img_arr):
        imgray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(imgray, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def get_bounding_rect(self, cnt, img_arr, img, threshold=10, padding=10, draw=True):
        x,y,w,h = cv2.boundingRect(cnt)
        top_left_outer = (x-padding if x-padding >= 0 else 0,
                          y-padding if y-padding >= 0 else 0)
        bottom_right_outer = (x+w+padding if x+w+padding <= img.width else img.width,
                              y+h+padding if y+h+padding <= img.height else img.height)
        if w > threshold and h > threshold:
            if draw:
                cv2.rectangle(img_arr, top_left_outer, bottom_right_outer, (0,0,255), 1)
                cv2.rectangle(img_arr, (x,y), (x+w,y+h), (0,255,0), 1)
            #print top_left_outer, w+padding, h+padding
            return img.crop(top_left_outer[0], top_left_outer[1],
                            bottom_right_outer[0]-top_left_outer[0],
                            bottom_right_outer[1]-top_left_outer[1], smart=True)

    def add_observation(self, img_arr, draw=True):
        img = Image(img_arr)
        for cnt in self.find_contours(img_arr):
            obj_candidate = self.get_bounding_rect(cnt, img_arr, img, draw=draw)
            #if obj_candidate:
                #obj = self.classifier.classify(obj_candidate)
                #if obj != self.NEGATIVE_CLS:
                    #x,y,w,h = cv2.boundingRect(cnt)
                    #cv2.rectangle(img_arr, (x,y), (x+w,y+h), (255,0,0), 3)
                    #cv.PutText(cv.fromarray(img_arr), obj, (x, y), thinFont, fontColor)
                    #self.objs[obj] =

    def step(self):
        try:
            #print "Processing: START"
            retval, img_arr = self.cam.read()
            assert img_arr is not None, "Camera in use by other process"
            self.add_observation(img_arr)
            if settings.use_simplecv_display:
                SimpleCV.Image(cv.fromarray(img_arr)).show()
            else:
                cv.ShowImage("Index", cv.fromarray(img_arr))
            #print "Processing: DONE"
            return True
        except KeyboardInterrupt:
            return False


class VisionSystem(object):

    def __init__(self, dx=150, dy=150, overlap_factor=2):
        self.cam = cv2.VideoCapture(settings.camera_index)

        self.dx = dx
        self.dy = dy
        self.overlap_factor = overlap_factor
        from train import classifier
        self.classifier = classifier

        self.objs = {}

    def step(self):
        try:
            print "Processing: START"
            retval, img_arr = self.cam.read()
            self.add_observation(img_arr, annotate=True)
            self.annotate_img(img_arr)
            cv.ShowImage("Index", cv.fromarray(img_arr))
            print "Processing: DONE"
            return True
        except KeyboardInterrupt:
            return False

    def img_to_cvmat(self, img):
        return cv.GetMat(img.getBitmap())

    def add_observation(self, img_arr, annotate=False):
        img = Image(img_arr)
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
                        fontFace = 0
                        fontHscale = 0.75
                        fontVscale = 0.75
                        fontShear = 0
                        fontThickness = 1
                        thinFont = cv.InitFont(fontFace, fontHscale, fontVscale, fontShear, fontThickness)
                        fontColor = cv.RGB(0, 0, 255)
                        cv.Rectangle(cv.fromarray(img_arr), (x, y), (x+self.dx/2, y+self.dy/2), fontColor)
                        cv.PutText(cv.fromarray(img_arr), obj, (x, y), thinFont, fontColor)
                    self.objs[obj].add_observation(observation)
                else:
                    self.objs[obj] = VisionObjectFilter(observation, img.width, img.height, label=obj)

    def annotate_img(self, img):
        for obj in self.objs:
            try:
                x, y = self.get_state(obj)
                x = int(x)
                y = int(y)
                x -= self.dx/2
                y -= self.dy/2
            except TypeError:
                continue
            fontFace = 0
            fontHscale = 0.75
            fontVscale = 0.75
            fontShear = 0
            fontThickness = 1
            thinFont = cv.InitFont(fontFace, fontHscale, fontVscale, fontShear, fontThickness)
            fontColor = cv.RGB(255, 0, 0)
            cv.Rectangle(cv.fromarray(img), (x, y), (x+self.dx, y+self.dy), fontColor)
            cv.PutText(cv.fromarray(img), obj, (x, y), thinFont, fontColor)

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
        self.last_obs_t = tm.time()
        self.slack_time = 2

    def add_observation(self, observation):
        self.last_obs_t = tm.time()
        self.observations.add(observation)

    def infer_state(self):
        if tm.time() - self.last_obs_t > self.slack_time:
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
      self.prev_t = tm.time()
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
      t = tm.time()
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
