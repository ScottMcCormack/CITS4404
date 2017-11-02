import os
import pickle
import numpy as np
import re

data_dir = os.path.join('..', 'data', 'DCASE') # Parent directory containing '*.cpickle' files
meta_path = os.path.join(data_dir, 'meta.txt') # Path to the 'meta.txt' file

# Runtime params
num_segments = 4


# Load the meta file and parse the file
files = {}
with open(meta_path, 'r') as metaFile:
    for line in metaFile:
        line = line.split('\t')[0:2]
        name = re.search(r'/(.+)\.', line[0]).group()[1:-1]
        clss = line[1]
        files[name] = clss

training_output = '' # Output for the training data
testing_output = ''
testing_to_training_ratio = 1
count = 0 # Count the number of processed cpickle files

# 1.  Walk through the parent directory
# 2.  Load all the .cpickle files that are found
for dirName, subdirList, fileList in os.walk(data_dir):
    for filename in fileList:
        if filename.endswith('.cpickle'):
            count += 1
            nameId = re.sub(r'\.cpickle', '', filename)  # get file name
            pickle_data = pickle.load(open(os.path.join(dirName, filename), 'rb'))
            feat_data = np.array(pickle_data['feat'][0])

            # Create features by splitting and taking the mean and std
            instanceFeatures = ''
            for i in feat_data.transpose():
                for j in np.array_split(i, num_segments):
                    instanceFeatures += str(np.mean(j)) + '\t'
                    instanceFeatures += str(np.std(j)) + '\t'

            # Add the output to either training or testing data
            training_output += instanceFeatures + files[nameId] + '\n'

# 3.  Subdivide the cpickle files

# Write the file out to the parent folder where it sourced the cpickle files from
filename_out = os.path.join(data_dir, 'data_{0}_all.txt'.format(count))

with open(filename_out, 'w') as saveFile:
    saveFile.write(training_output)
