import numpy as np
from sklearn import metrics
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Limiting data to 4 newsgroup categories.
categories = ['alt.atheism', 'soc.religion.christian',
              'comp.graphics', 'sci.med']

twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)

print("")
print("Example data from the news set.")
print("\n".join(twenty_train.data[0].split("\n")[:3]))
print(twenty_train.target_names[twenty_train.target[0]])

print("Index and count words.")
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train.data)

print("Does 'algorithm' exist in our vocabulary:", count_vect.vocabulary_.get(u'algorithm'))

print("")
print("Term Frequency times Inverse Document Frequency")
print("(getting rid of words that probably aren't helpful)")
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
print("Shape of data post tf-idf transform", X_train_tfidf.shape)

clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)

print("Classify some new (and fake) documents against our educated bot.")
fake_docs_new = ['God is love', 'OpenGL on the GPU is fast']
X_new_counts = count_vect.transform(fake_docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)
predicted = clf.predict(X_new_tfidf)
for doc, category in zip(fake_docs_new, predicted):
    print('%r => %s' % (doc, twenty_train.target_names[category]))

print("Make the processing easier by building a Pipeline.")
text_clf = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', MultinomialNB()),
])
print("Training the model pipeline")
text_clf.fit(twenty_train.data, twenty_train.target)

print("Evaluating accuracy of our model")
twenty_test = fetch_20newsgroups(subset='test', categories=categories, shuffle=True, random_state=42)
docs_test = twenty_test.data
predicted = text_clf.predict(docs_test)
print("How accurate is our model?", np.mean(predicted == twenty_test.target))

print("Get better accuracy")
text_clf = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=5, tol=None)),
])
text_clf.fit(twenty_train.data, twenty_train.target)
predicted = text_clf.predict(docs_test)
print("Updated accuracy", np.mean(predicted == twenty_test.target))

print("Get some metrics")
print("Classification report\n", metrics.classification_report(twenty_test.target, predicted, target_names=twenty_test.target_names))
print("Confusion matrix\n", metrics.confusion_matrix(twenty_test.target, predicted))
