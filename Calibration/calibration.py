def calibrateInertialSensorData(data, AM, SM, OV):
    import numpy as np
    # data: raw data to be calibrated
    # AM: alignment matrix
    # SM: sensitivity matrix
    # OV: offset vector

    # double[] tempdata = data;
    # double[,] data2d = new double[3, 1];
    # data2d[0, 0] = data[0];
    # data2d[1, 0] = data[1];
    # data2d[2, 0] = data[2];
    tempdata = np.array(data, dtype=np.float)
    data2d = np.zeros([3, 1], dtype=np.float)
    data2d[0,0] = data[0]
    data2d[1,0] = data[1]
    data2d[2,0] = data[2]

    # data2d = MatrixMultiplication(MatrixMultiplication(MatrixInverse3x3(AM), MatrixInverse3x3(SM)), MatrixMinus(data2d, OV));
    data2d = np.dot(np.dot(np.linalg.inv(AM),np.linalg.inv(SM)),(data2d-OV))

    # tempdata[0] = data2d[0, 0];
    # tempdata[1] = data2d[1, 0];
    # tempdata[2] = data2d[2, 0];
    tempdata[0] = data2d[0, 0];
    tempdata[1] = data2d[1, 0];
    tempdata[2] = data2d[2, 0];

    return tempdata;


# some test code

import numpy as np
ALIGNMENT_ACCEL = np.array([[0,-1.0,0],[-1.0,0,0],[0,0,-1.0]])
SENSITIVITY_ACCEL = np.array([[83.0,0,0],[0,83.0,0],[0,0,83.0]])
OFFSET_ACCEL = np.array([[2047.0],[2047.0],[2047.0]])

ALIGNMENT_GYRO = np.array([[0,-1.0,0],[-1.0,0,0],[0,0,-1.0]])
SENSITIVITY_GYRO = np.array([[65.5,0,0],[0,65.5,0],[0,0,65.5]])
OFFSET_GYRO = np.array([[0.0],[0.0],[0.0]])

print calibrateInertialSensorData([2033,2035,1237],ALIGNMENT_ACCEL,SENSITIVITY_ACCEL,OFFSET_ACCEL)

print calibrateInertialSensorData([-129,62,-13],ALIGNMENT_GYRO,SENSITIVITY_GYRO,OFFSET_GYRO)

