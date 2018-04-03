# http://scikit-learn.org/stable/tutorial/basic/tutorial.html

import matplotlib.pyplot as plt
# MacOS rendering problem fix: https://stackoverflow.com/questions/29433824/unable-to-import-matplotlib-pyplot-as-plt-in-virtualenv#comment64137123_35107136
import numpy as np
# import pickle
from sklearn import datasets
from sklearn import svm
from sklearn.externals import joblib

print('\n\n\n*** numpy ***\n\n\n')
a = np.arange(15).reshape(3, 5)
print('np.arange(15).reshape(3, 5):\n', a)

print('')

zeros = np.zeros((10, 2))
print('np.zeros((10, 2))\n', zeros)

print('\n\n\n*** sklearn ***\n\n\n')
iris = datasets.load_iris()
digits = datasets.load_digits()
print('datasets must be in (n_samples, n_features) shape.')
print('Shape of original digit images (cannot be consumed by scikit learn):', digits.images.shape)
# Need to flatten the 8x8 image into a vactor 64 length.
print('Shape of digits dataset that can be consumed by scikitlearn:', digits.data.shape)
# print('digits descriptor:', digits.DESCR)

clf = svm.SVC(gamma=0.001, C=100.)
# fit == learn
clf.fit(digits.data[:-1], digits.target[:-1])

# predict values based of previous training
x = clf.predict(digits.data[-1:])
print('Predict the value of the last digit:', x)

# Can save (serialize) model data via pickle.
# s = pickle.dumps(clf)
# but this seems not recommended,
# instead user their to-file serializer...
joblib.dump(clf, 'saved-classifier.digits.pkl')
