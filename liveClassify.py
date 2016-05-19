import numpy as np
from iotdata import IOTData
from ShimmerBluetooth import ShimmerBluetooth

import weka.core.serialization as serialization
from weka.classifiers import Classifier
import weka.core.jvm as jvm
from weka.core.converters import Loader
from weka.classifiers import Evaluation
from weka.core.classes import Random

# devices = ["Ground_Truth_Treadmill1", "Ground_Truth_Treadmill2", "Ground_Truth_Treadmill3", "Ground_Truth_Treadmill5"]
# device = IOTData(devices, 'Ground_Truth_data\\03_27_16\\')
# devices = IOTData(None, comport = "COM5")

jvm.start()
objects = serialization.read_all("test.model")
classifier = Classifier(jobject=objects[0])


# sensors = [ShimmerBluetooth("COM9", 256)]
dataManager = IOTData(None, comport = 'COM30')
predictions = [0]*len(sensors)
stepCount = 0

try:
    while True:
        for i in range(len(sensors)):

            # aquire data
            # df = sensors[i].getFrame()
            df = dataManager.getNextWindow()

            # run the data frame (df) through nathan's code, output is signle row arff
            inst = # nathan, looks like the iotdata class has some capabilities for handling streaming data, ill let you do this

            # classify
            pred = classifier.classify_instance(inst)

            # estimate step count
            stepCount += countSteps(df)

            # save prediciton
            predictions[i] = pred

        # output predictions
        print predictions, stepCount

except KeyboardInterrupt:
    for sensor in sensors:
        sensor.closeDevice()

jvm.stop()


def countSteps(data):
    # remove the mean
    data = data - np.mean(data)
    #disregard end samples
    data = data[0:(len(data)-len(data)%8)]
    # break the time domain signal into 8-long windows
    data = np.reshape(data,(-1,8))
    # calculate energy in the windows
    energy = np.sum(np.square(data),axis=1)
    # calculate an energy threshold
    enThreshold = 1.5*np.mean(energy)
    for i in range(len(energy)):
        if energy[i]<enThreshold:
            energy[i] = 0
    pkInds,o2 = peakdetect.peakdet(energy,enThreshold)
    return len(peakInds)



