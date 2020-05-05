import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from numpy.linalg import inv
from scipy.spatial.distance import pdist, squareform, cdist
import scipy
import tensorflow_hub as hub

# Suppress warnings 
import warnings
warnings.filterwarnings('ignore')

sample_submission = pd.read_csv("file/sample_submission.csv")
testData = pd.read_csv("file/test_cleaned.csv")
trainData = pd.read_csv("file/train_cleaned.csv")

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

#parametri migliori trovati nel file findModello.py
gamma = 2.075
C = 1.5
lambd = 1/C

j=0

for a in trainData["target"]:
    if (a == 0):
        trainData["target"][j]=-1
        
    j = j +1


X = train_vectors

dist = squareform(pdist(X, 'euclidean'))
Q = scipy.exp(-gamma*(dist ** 2))

eye = lambd*np.eye(7613)
ainv = inv(Q+ eye)

alpha = np.dot(ainv,trainData["target"])

Xf = test_vectors

distanza = cdist(Xf,X, 'euclidean')
square = np.square(distanza)

print("Predictions computation:")
f = np.dot(scipy.exp(-gamma*square), alpha)
predizioni = f

j=0

for a in f:
    if (a < 0):
        predizioni[j] = 0
    else:
        predizioni[j] = 1
        
    j = j +1

#creazione del target file per la submission
sample_submission["target"] = predizioni
sample_submission.to_csv("file/submission.csv", index=False)