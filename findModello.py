import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

sample_submission = pd.read_csv("file/sample_submission.csv")
testData = pd.read_csv("file/test_cleaned.csv")
trainData = pd.read_csv("file/train_cleaned.csv")

from sklearn.model_selection import GridSearchCV

from sklearn.metrics import f1_score
from sklearn.metrics import a

import tensorflow_hub as hub
import tensorflow as tf

#elimino i duplicati in trainDati
trainData = trainData.drop_duplicates().reset_index(drop=True)

#carichiamo il codificatore universale di frasi
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

#trasformiamo i dataset in numeri
X_train_embeddings = embed(trainData['text'])
X_test_embeddings = embed(testData['text'])

#creo le matrici
train_vectors = X_train_embeddings.numpy()
test_vectors = X_test_embeddings.numpy()

#creo una partizione per la cross validation
from sklearn.model_selection import ShuffleSplit
cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=123)

#Logistic Regression
from sklearn.linear_model import LogisticRegression

parameters = [{'C': [1,1.5,2]}]        
lr = LogisticRegression(class_weight = 'balanced')
LogisticRegression = GridSearchCV(lr, parameters, scoring="f1", cv=cv)

LogisticRegression.fit(train_vectors, trainData["target"]) 

pred = LogisticRegression.predict(train_vectors)

print("Logistic Regression accuracy train score: ",accuracy_score(trainData["target"], pred))
print("Logistic Regression f1 score:", LogisticRegression.best_score_)
print("Logistic Regression best params:", LogisticRegression.best_params_,"\n")

#SVM 
from sklearn.svm import SVC

parameters = [{'kernel': ['linear'], 'C': [0.1,1,10]},
              {'kernel': ['rbf'], 'C': [0.1,2,10], 'gamma' :[0.1,2,10]}] #best rbf, C = 1.5, gamma = 2

SVM = SVC(random_state = 55)
SVMClassifier = GridSearchCV(SVM, parameters, scoring="f1", cv=cv, n_jobs=-1)

SVMClassifier.fit(train_vectors, trainData["target"])

pred = SVMClassifier.predict(train_vectors)

print("SVM accuracy train score: ",accuracy_score(trainData["target"], pred))
print("SVM f1 score:", SVMClassifier.best_score_)
print("SVM best params:", SVMClassifier.best_params_,"\n")

#KNN
from sklearn.neighbors import KNeighborsClassifier

parameters = [{'n_neighbors': [21, 25]}]
neigh = KNeighborsClassifier()
knnModel = GridSearchCV(neigh, parameters, scoring="f1", cv=cv, n_jobs=-1)

knnModel.fit(train_vectors, trainData["target"]) 

pred = knnModel.predict(train_vectors)

print("KNN accuracy train score: ",accuracy_score(trainData["target"], pred))
print("KNN f1 score:", knnModel.best_score_)
print("KNN best params:", knnModel.best_params_ ,"\n")

#Perceptron
from sklearn.linear_model import Perceptron

parameters = [{'class_weight': [None, 'balanced']}]
p = Perceptron()
perceptron = GridSearchCV(p, parameters, scoring="f1", cv=cv, n_jobs=-1)

perceptron.fit(train_vectors, trainData["target"]) 

pred = perceptron.predict(train_vectors)

print("Perceptron accuracy train score: ",accuracy_score(trainData["target"], pred))
print("Perceptron f1 score:", perceptron.best_score_)
print("Perceptron best params:", perceptron.best_params_ ,"\n")

#scelta del modello migliore
models = [knnModel, SVMClassifier,LogisticRegression,perceptron]

scoreMax = 0
for model in models:
    if(model.best_score_ > scoreMax):
        scoreMax = model.best_score_
        modelloMigliore = model


print("Best model: ", modelloMigliore.best_estimator_,"\n")

#creazione del target file per la submission
sample_submission["target"] = modelloMigliore.best_estimator_.predict(test_vectors)
sample_submission.to_csv("file/submission.csv", index=False)

#calcolo della confusion matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

X_train, X_test, y_train, y_test = train_test_split(train_vectors, trainData["target"], test_size=0.2)

modelloMigliore.best_estimator_.fit(X_train, y_train) 

results = confusion_matrix(y_test, modelloMigliore.best_estimator_.predict(X_test)) 
  
print ('Confusion Matrix :')
print(results) 