import numpy as np
from sklearn import metrics
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import time

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

print("Make our classifier better by trying different parameters within a range of posibilities.")
grid_search_start_time = time.monotonic()
gs_clf_parameters = {
    # Rubber duck: a brief scan of the docs doesn't seem to use this string notation in any of the examples,
    # but I assume the double underbar has special meaning as a separator between pipeline dictionary and
    # labeled parameter that can be tweaked in the text_clf pipeline, e.g. 'vect__ngram_range' means
    # try out vect with ngram_range paramteres between the values of (1, 1) and (1, 2).
    'vect__ngram_range': [(1, 1), (1, 2)],
    'tfidf__use_idf': (True, False),
    'clf__alpha': (1e-2, 1e-3),
}
gs_clf = GridSearchCV(text_clf, gs_clf_parameters, n_jobs=-1)
print("Classifying with a smaller subset of data because this example is made for learn by procedure.")
gs_clf = gs_clf.fit(twenty_train.data[:400], twenty_train.target[:400])
print("The tuned classifier can now predict. Tuning took %f seconds." % (time.monotonic() - grid_search_start_time))
predicted_target_name_index = gs_clf.predict(['God is love'])[0]
print("We predict 'God is love' to belong to group: '%s'" % twenty_train.target_names[predicted_target_name_index])

print("")
print("The best score withour gs_clf tuned classifier is:", gs_clf.best_score_)
print("The tuned parameters used to achieve this score are:")
for param_name in sorted(gs_clf_parameters.keys()):
    print("%s: %r" % (param_name, gs_clf.best_params_[param_name]))
