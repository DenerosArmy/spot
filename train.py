from SimpleCV import *

base_path = "/Users/jian/Projects/Pinkie/training_data"
tags = ["pen", "pi", "key", "negative"]

def train(tags):
    e = EdgeHistogramFeatureExtractor()
    hue = HueHistogramFeatureExtractor()
    morph = MorphologyFeatureExtractor()
    features = [e, hue, morph]
    c = MachineLearning.TreeClassifier(features, flavor="Forest")
    paths = [os.path.join(base_path, tag) for tag in tags]
    c.train(paths, tags)
    return c

classifier = train(tags)
