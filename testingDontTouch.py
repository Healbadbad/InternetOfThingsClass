
from iotdata import IOTData

sensor = IOTData("COM9", 256)
df = sensor.getFrame()
