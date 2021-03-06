import pandas as pd
import numpy as np
import pickle
import csv
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn import preprocessing

dataframe = pd.read_csv('./datasets/records_4000.tsv', sep='\t')
dataframe['genre'] = dataframe['genre'].str[:-1]
dataframe = dataframe.drop(['track_id'], axis = 1)

# Format of genre is "Rap\n" with the return character
def create_train_validation_test(df, genre):

    #One hot encode the key and drop the original key
    one_hot_key = pd.get_dummies(df['key'])
    df = df.drop(['key'], axis=1)
    newcols = list(df.columns)
    df = pd.concat([df, one_hot_key], axis=1)
    for keyn in range(12):
        newcols.append('key_' + str(keyn))
    df.columns = newcols

    df = df.fillna(0)
    # 4000 songs from genre
    df_genre = df.loc[df['genre'] == genre]

    # 4000 songs from not genre
    df_non_genre = df.loc[df['genre'] != genre].sample(n=4000)
    df_non_genre['genre'] = 'nongenre'

    # Divide pop rock into train and test
    train_genre, test_genre = train_test_split(df_genre, test_size=0.2)

    # Divide non pop rock into train and test
    train_non_genre, test_non_genre = train_test_split(df_non_genre, test_size = 0.2)

    # Combine pop-rock and non-poprock into train/test
    train = train_genre.append(train_non_genre)
    test = test_genre.append(test_non_genre)

    train, validation = train_test_split(train, test_size=0.2)

    min_max_scaler = preprocessing.MinMaxScaler()
    # training, validation, and test data
    X_train = train.drop(['genre'], axis = 1)
    y_train = train[['genre']]
    X_train = min_max_scaler.fit_transform(X_train)

    X_validation = validation.drop(['genre'], axis = 1)
    y_validation = validation[['genre']]
    X_validation = min_max_scaler.fit_transform(X_validation)

    X_test = test.drop(['genre'], axis = 1)
    X_test = min_max_scaler.fit_transform(X_test)

    y_test = test[['genre']]

    return X_train, y_train, X_validation, y_validation, X_test, y_test


X_train, y_train, X_validation, y_validation, X_test, y_test = create_train_validation_test(dataframe, 'Jazz')

# param_grid = [
#   {'C': [0.03, 0.1, 0.3, 1, 2], 'kernel': ['linear']},
#   {'C': [0.03, 0.1, 0.3, 1, 2], 'gamma': [3.0, 1.0, 0.3, 0.1, 0.03], 'kernel': ['rbf']},
#  ]
#
# scores = ['accuracy', 'precision_micro', 'recall_micro', 'f1_micro']
# for score in scores:
#     print("# Tuning hyper-parameters for %s" % score)
#     print()
#
#     clf = GridSearchCV(SVC(), param_grid, cv=5,
#                        scoring=score)
#     print('gjg')
#     labels = y_train['genre']
#     clf.fit(X_train, labels)
#
#     print("Best parameters set found on development set:")
#     print()
#     print(clf.best_params_)
#     print()
#     print("Grid scores on development set:")
#     print()
#     means = clf.cv_results_['mean_test_score']
#     stds = clf.cv_results_['std_test_score']
#     for mean, std, params in zip(means, stds, clf.cv_results_['params']):
#         print("%0.3f (+/-%0.03f) for %r"
#               % (mean, std * 2, params))
#     print()
#
#     print("Detailed classification report:")
#     print()
#     print("The model is trained on the full development set.")
#     print("The scores are computed on the full evaluation set.")
#     print()
#     y_true, y_pred = y_test, clf.predict(X_test)
#     print(classification_report(y_true, y_pred))
#     print()
#     print(accuracy_score(y_true, y_pred))

print("rbf 0.1")
clf = svm.SVC(kernel='rbf', C=0.1, gamma = 0.3).fit(X_train, y_train)
scores = clf.score(X_test, y_test)
print(scores)

print("rbf 0.3")
clf = svm.SVC(kernel='rbf', C=0.3, gamma = 0.3).fit(X_train, y_train)
scores = clf.score(X_test, y_test)
print(scores)

print("rbf 1")
clf = svm.SVC(kernel='rbf', C=1, gamma = 0.3).fit(X_train, y_train)
scores = clf.score(X_test, y_test)
print(scores)

print("rbf 3")
clf = svm.SVC(kernel='rbf', C=3, gamma = 0.3).fit(X_train, y_train)
scores = clf.score(X_test, y_test)
print(scores)

print("rbf 10")
clf = svm.SVC(kernel='rbf', C=10, gamma = 0.3).fit(X_train, y_train)
scores = clf.score(X_test, y_test)
print(scores)

print("\n")

print("linear 0.01")
clf = svm.SVC(kernel='linear', C=.01).fit(X_train, y_train)
scores = clf.score(X_test, y_test)
print(scores)

print("linear 0.03")
clf = svm.SVC(kernel='linear', C=0.03).fit(X_train, y_train)
scores = clf.score(X_test, y_test)
print(scores)

print("linear 0.1")
clf = svm.SVC(kernel='linear', C=0.1).fit(X_train, y_train)
scores = clf.score(X_test, y_test)
print(scores)

print("linear 0.3")
clf = svm.SVC(kernel='linear', C=0.3).fit(X_train, y_train)
scores = clf.score(X_test, y_test)
print(scores)

print("linear 1")
clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
scores = clf.score(X_test, y_test)
print(scores)

print("linear 3")
clf = svm.SVC(kernel='linear', C=3).fit(X_train, y_train)
scores = clf.score(X_test, y_test)
print(scores)

print("linear 10")
clf = svm.SVC(kernel='linear', C=10).fit(X_train, y_train)
scores = clf.score(X_test, y_test)
print(scores)