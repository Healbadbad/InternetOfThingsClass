from sklearn.ensemble import RandomForestClassifier

data = open("Ground_Truth_data\\03_27_16\\data.txt")
feats = data.readline().split(",")

data = []
targets = []


while True:
	line = data.readline()
	if line == '':
		break
	line = line.split(",")
	for k in range(len(line)):
		if feats[k].contains()

