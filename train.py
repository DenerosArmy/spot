from SimpleCV import *

base_path = "/Users/jian/Projects/Pinkie/training_data"
tags = ["pen", "pi", "key", "negative"]

#def get_negative_tags(positive_tags):
    #negative_tags = []
    #positive_tags = set(positive_tags)
    #for tag in os.listdir(base_path):
        #if tag != ".DS_Store" and tag not in positive_tags:
            #negative_tags.append(tag)
    #return negative_tags

def train(tags):
    #negative_tags = get_negative_tags(tags)
    e = EdgeHistogramFeatureExtractor()
    hue = HueHistogramFeatureExtractor()
    morph = MorphologyFeatureExtractor()
    features = [e, hue, morph]
    c = MachineLearning.TreeClassifier(features, flavor="Forest")
    imgsets = [ImageSet(os.path.join(base_path, tag)) for tag in tags]
    #imgsets.append(ImageSet([os.path.join(base_path, tag)+"/" for tag in negative_tags]))
    #imgsets.append(ImageSet(os.path.join(base_path, "negative")))
    #print ImageSet([os.path.join(base_path, tag) for tag in negative_tags])
    c.train(imgsets, tags)
    return c

classifier = train(tags)
