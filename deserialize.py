import weka.core.serialization as serialization
from weka.classifiers import Classifier
objects = serialization.read_all("test.model")
classifier = Classifier(jobject=objects[0])
print(classifier)
