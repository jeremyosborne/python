"""Build a language detector model

The goal of this exercise is to train a linear classifier on text features
that represent sequences of up to 3 consecutive characters to recognize natural
languages with short character sequences as 'fingerprints'.

Pre-requisite:

```
python data/languages/fetch_data
```

Feed downloaded data in with

```
python language_detection.py data/languages/short_paragraphs
```

"""
# Author: Olivier Grisel <olivier.grisel@ensta.org>
# License: Simplified BSD

import sys

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Perceptron
from sklearn.pipeline import Pipeline
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn import metrics


# The training data folder must be passed as first argument
languages_data_folder = sys.argv[1]

# http://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_files.html
# Individual samples are assumed to be files stored a two levels folder structure:
# short_paragraphs/<language_code>
# For us, the language code will become the category.
dataset = load_files(languages_data_folder)

# Debug
# print('dataset:')
# print(dataset)

# Split the dataset in training and test set.
# see: # see: http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
# X, y notation seems to be common notation.
docs_train, docs_test, y_train, y_test = train_test_split(
    # Arrays to split and organize are vararg
    dataset.data,
    dataset.target,
    # Options are kwarg
    test_size=0.5  # Proportion of data we want to work with
)

# Debug
# print('docs_train:')
# print(docs_train)
# print('docs_train[1]:', docs_train[1])
# print('type(docs_train):', type(docs_train))
# print(y_train)
# print('y_train[1]:', y_train[1])
# print('type(docs_train):', type(docs_train))
# print('type(y_train):', type(y_train))

# TASK: Build a vectorizer that splits strings into sequence of 1 to 3
# characters instead of word tokens
# see: http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
# tfidf_matrix = TfidfVectorizer(
#     # Train below.
#     # input=docs_train,
#     # I believe this will fulfill the task above...
#     ngram_range=(1, 3)
# )
# Debug
# print('tfidf_matrix:')
# print(tfidf_matrix)
# From the solution after double checking
vectorizer = TfidfVectorizer(
    ngram_range=(1, 3),
    analyzer='char',
    use_idf=False
)

# TASK: Build a vectorizer / classifier pipeline using the previous analyzer.
# The pipeline instance should be stored in a variable named clf.
# see: http://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html
clf = Pipeline([
    ('vec', vectorizer),
    # see: http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Perceptron.html
    ('clf', Perceptron(tol=1000)),
])

# TASK: Fit the pipeline on the training set
# see: http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html#sklearn.feature_extraction.text.TfidfVectorizer.fit
clf.fit(docs_train, y_train)

# TASK: Predict the outcome on the testing set in a variable named y_predicted
y_predicted = clf.predict(docs_test)

# Print the classification report
print(metrics.classification_report(
    y_test,
    y_predicted,
    target_names=dataset.target_names
))

# Plot the confusion matrix
cm = metrics.confusion_matrix(y_test, y_predicted)
print(cm)

# import matplotlib.pyplot as plt
# plt.matshow(cm, cmap=plt.cm.jet)
# plt.show()

# Predict the result on some short new sentences:
sentences = [
    u'This is a language detection test.',
    u'Ceci est un test de d\xe9tection de la langue.',
    u'Dies ist ein Test, um die Sprache zu erkennen.',
]
predicted = clf.predict(sentences)

for s, p in zip(sentences, predicted):
    print(u'The language of "%s" is "%s"' % (s, dataset.target_names[p]))
