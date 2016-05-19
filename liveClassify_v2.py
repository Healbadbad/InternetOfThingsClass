import numpy as np
import pdb
from iotdata_simpleMostlyStatic import IOTData_simple
from ShimmerBluetooth import ShimmerBluetooth
from peakdetect2 import locatePeaks

import pickle as pkl
from sklearn.ensemble import RandomForestClassifier

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
    pkInds = locatePeaks(energy,enThreshold*1,5,minamp = enThreshold)
    # for i in range(len(energy)):
    #     if energy[i]<enThreshold:
    #         energy[i] = 0
    # pkInds,o2 = peakdetect.peakdet(energy,enThreshold)
    return len(pkInds)

# devices = ["Ground_Truth_Treadmill1", "Ground_Truth_Treadmill2", "Ground_Truth_Treadmill3", "Ground_Truth_Treadmill5"]
# device = IOTData(devices, 'Ground_Truth_data\\03_27_16\\')
# devices = IOTData(None, comport = "COM5")

featuregenerator = IOTData_simple(windowsize = 256)

print "loading classifier"
pkledClassifier = open('randomforestclassifier2.pkl','rb')
classifier = pkl.load(pkledClassifier)
pkledClassifier.close()

print "initializing bluetooth connection"
sensors = [ShimmerBluetooth("COM9", 256)]

predictions = [None]*len(sensors)
stepCount = [0]*len(sensors)

try:
    print "entering main loop"
    while True:
        for i in range(len(sensors)):

            # aquire data
            df = np.array(sensors[i].getFrame())
            featureVector = featuregenerator.generateWindowFeatures(df)
            print(len(featureVector))
            featureVector = np.reshape(featureVector,(1,-1))

            # classify
            pred = classifier.predict(featureVector)
            predictions[i] = pred[0]

            # estimate step count
            # i dunno?
            accelMagnitude = np.sqrt(np.square(df[:,0])+np.square(df[:,1])+np.square(df[:,2]))
            if predictions[i] != "not_walking":
                stepCount[i] += countSteps(accelMagnitude)

            # save prediciton
            predictions[i] = pred

        # output predictions
        print '-'*20
        for i in range(len(sensors)):
            print 'Sensor #', i+1, ':',predictions[i], 'and', stepCount[i], 'total steps'

except KeyboardInterrupt:
    for sensor in sensors:
        sensor.closeDevice()

