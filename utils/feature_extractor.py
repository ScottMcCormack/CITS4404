import os
import pickle
import numpy as np
import re

# run this script with no arguments in the folder with all the cpickle files.
# will create a file called data.txt if it doesn't exist already, otherwise will overwrite it

data_dir = os.path.join('..', 'data', 'DCASE')
meta_path = os.path.join(data_dir, 'meta.txt')
dirs_to_eval = ['evaluator', 'feature_extractor']

# Load the meta file and parse the file
files = {}
with open(meta_path, 'r') as metaFile:
    for line in metaFile:
        line = line.split('\t')[0:2]
        name = re.search(r'/(.+)\.', line[0]).group()[1:-1]
        clss = line[1]
        files[name] = clss

output = '' # Output to be passed to the
count = 0 # Count the number of processed cpickle files

# Walk through the parent directory and load all the .cpickle files that are found
for dirName, subdirList, fileList in os.walk(data_dir):
    for filename in fileList:
        if filename.endswith('.cpickle'):
            count += 1
            nameId = re.sub(r'\.cpickle', '', filename)  # get file name
            pickle_data = pickle.load(open(os.path.join(dirName, filename), 'rb'))
            feat_data = np.array(pickle_data['feat'][0])

            instanceFeatures = ''
            for i in feat_data.transpose():
                for j in np.array_split(i, 4):
                    instanceFeatures += str(np.mean(j)) + '\t'
                    instanceFeatures += str(np.std(j)) + '\t'

            output += instanceFeatures + files[nameId] + '\n'

# Write the file out to the parent folder where it sourced the cpickle files from
filename_out = os.path.join(data_dir, 'data_{0}_all.txt'.format(count))

with open(filename_out, 'w') as saveFile:
    saveFile.write(output)
