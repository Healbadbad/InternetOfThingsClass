from iotdata import IOTData
devices = ["Ground_Truth_Treadmill1", "Ground_Truth_Treadmill2", "Ground_Truth_Treadmill3", "Ground_Truth_Treadmill5"]
device = IOTData(devices, 'Ground_Truth_data\\03_27_16\\')
device.initdata(devices[0])

labels = [{'Begin': 1458998042.837, 'End': 1458998110.328, 'Label':'not_walking'}]
#Treadmill 1 was not walked on
device.generateAllFeaturesToARFF(labels, 50000, device.getLength())


device.initdata(devices[1])
labels = [
# Data Collection
# Anna 111
{'Begin': 1458998042.837, 'End': 1458998110.328, 'Label':'walking'},
{'Begin': 1458998110.329, 'End':1458998155.595, 'Label':'walking' },
{'Begin': 1458998155.595, 'End':1458998205.02, 'Label':'running' },
{'Begin': 1458998205.02, 'End':1458998227.432, 'Label':'running' },
{'Begin': 1458998227.432, 'End':1458998274.98, 'Label':'running' },
{'Begin': 1458998274.98, 'End':1458998332.8, 'Label':'walking' },

# Nathan 125
{'Begin': 1458998375.005, 'End': 1458998400.183, 'Label':'walking'},
{'Begin': 1458998400.183, 'End':1458998427.937, 'Label':'walking' },
{'Begin': 1458998427.937, 'End':1458998457.626, 'Label':'walking' },
{'Begin': 1458998457.626, 'End':1458998486.797, 'Label':'running' },
{'Begin': 1458998486.797, 'End':1458998516.699, 'Label':'running' },
{'Begin': 1458998546.71, 'End':1458998585.793, 'Label':'running' },

#Christian 184
{'Begin': 1458998690.386, 'End':1458998712.231, 'Label':'walking' },
{'Begin': 1458998712.231, 'End':1458998741.083, 'Label':'walking' },
{'Begin': 1458998741.083, 'End':1458998769.803, 'Label':'walking' },
{'Begin': 1458998769.803, 'End':1458998800.468, 'Label':'walking' },
{'Begin': 1458998800.468, 'End':1458998830.908, 'Label':'running' },
{'Begin': 1458998830.908, 'End':1458998859.548, 'Label':'running' },
{'Begin': 1458998859.548, 'End':1458998890.286, 'Label':'running' },
{'Begin': 1458998890.286, 'End':1458998921.288, 'Label':'running' },
{'Begin': 1458998921.288, 'End':1458998952.361, 'Label':'running' },
{'Begin': 1458998952.361, 'End':1458998980.371, 'Label':'running' },

#Matthew 200
{'Begin': 1458999053.379, 'End':1458999080.268, 'Label':'walking' },
{'Begin': 1458999080.268, 'End':1458999109.819, 'Label':'walking' },
{'Begin': 1458999109.819, 'End':1458999140.422, 'Label':'walking' },
{'Begin': 1458999140.422, 'End':1458999169.748, 'Label':'running' },
{'Begin': 1458999169.748, 'End':1458999201.157, 'Label':'running' },
{'Begin': 1458999201.157, 'End':1458999230.449, 'Label':'running' },
{'Begin': 1458999230.449, 'End':1458999262.104, 'Label':'running' },

#no person test - 5mph 18 seconds to increase
#[['Begin', 1458999505.319], ['End', 1458999560.049]]

# Two Treadmill Tests Christian T2 Anna T3, then T4, then T5
{'Begin': 1458999740.647, 'End':1458999262.104, 'Label':'running' },

#Incline test, 4mph 5% 7.5% 10% 12.5% 15% 17.5% incline
{'Begin': 1459000246.131, 'End':1459000525.981, 'Label':'running' }]
device.generateAllFeaturesToARFF(labels, 50000, device.getLength())

device.initdata(devices[2])
labels = [
{'Begin': 1458999785.053, 'End': 1458999868.831, 'Label':'running'}]
device.generateAllFeaturesToARFF(labels, 50000, device.getLength())



device.initdata(devices[3])
labels = [
{'Begin': 1459000051.865, 'End': 1459000134.03, 'Label':'running'}]
device.generateAllFeaturesToARFF(labels, 50000, device.getLength())

