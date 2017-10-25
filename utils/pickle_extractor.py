import sys
import pickle
import numpy as np

input = sys.argv

data = pickle.load(open(input[1], 'r'))

# print pickle keys
for i in data:
    print(i)
    print('\n')

# print features and details
features = np.array(data['feat'])
print(features.shape)
for i in range(0, 40):
    print('feature', i, 'range:', min(features[0, :, i]), max(features[0, :, i]), 'mean', np.mean(features[0, :, i]),
          'stdDev', np.std(features[0, :, i]))
    print('\n')

# print pickle metadata
for i in data['meta']:
    print(i)
    if i == 'parameters':
        for j in data['meta'][i]:
            print(' ', j)
            print('   ', data['meta'][i][j])
    else:
        print(data['meta'][i])
    print('\n')
