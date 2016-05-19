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
