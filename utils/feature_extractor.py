import os
import pickle
import numpy as np
import re

# run this script with no arguments in the folder with all the cpickle files.
# will create a file called data.txt if it doesn't exist already, otherwise will overwrite it

files = {}
with open('meta.txt', 'r') as metaFile:
    for line in metaFile:
        line = line.split('\t')[0:2]
        name = re.search(r'/(.+)\.', line[0]).group()[1:-1]
        clss = line[1]
        files[name] = clss

allFeats = ''
for filename in os.listdir('.'):
    if filename.endswith('.cpickle'):
        # get file name
        nameId = re.sub(r'\.cpickle', '', filename)

        data = pickle.load(open(filename, 'rb'))

        data = np.array(data['feat'][0])

        instanceFeatures = ''
        for feature in range(0, 40):
            featureSlices = data[:, feature]
            instanceFeatures += str(np.mean(featureSlices)) + '\t'
            instanceFeatures += str(np.std(featureSlices)) + '\t'
            if feature == 39:
                instanceFeatures += files[nameId] + '\n'

            # print(instanceFeatures)
    allFeats += instanceFeatures
print(allFeats)

with open('data.txt', 'w') as saveFile:
    saveFile.write(allFeats)
