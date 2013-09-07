from SimpleCV import *

if os.environ["USER"] == "nikita":
    base_path = "/home/nikita/dev/pinkie/"
else:
    base_path = "/Users/jian/Projects/Pinkie/"

tags = ["pen", "pi", "key", "negative"]

def train(tags):
    e = EdgeHistogramFeatureExtractor()
    hue = HueHistogramFeatureExtractor()
    morph = MorphologyFeatureExtractor()
    features = [e, hue, morph]
    c = MachineLearning.TreeClassifier(features, flavor="Forest")
    paths = [os.path.join(base_path, "training_data", tag) for tag in tags]
    c.train(paths, tags)
    return c

classifier = train(tags)
