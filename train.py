from SimpleCV import *
from settings import base_path, tags
import os

def train(tags):
    e = EdgeHistogramFeatureExtractor()
    hue = HueHistogramFeatureExtractor()
    morph = MorphologyFeatureExtractor()
    features = [e, hue, morph]
    c = MachineLearning.TreeClassifier(features, flavor="Forest")
    paths = [os.path.join(base_path, "training_data", tag) for tag in tags]
    c.train(paths, tags)
    return c


retrain = False
cache_path = os.path.join(base_path, "classifier.cache")
if not retrain and os.path.exists(cache_path):
    print "Loading classifier from cache: {}".format(cache_path)
    classifier = TreeClassifier.load(cache_path)
else:
    print "Training classifier..."
    classifier = train(tags)
    classifier.save(cache_path)
