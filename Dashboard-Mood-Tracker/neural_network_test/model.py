import json
import pandas as pd
import re
import string
import numpy as np
import pickle
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.utils import class_weight
from keras.preprocessing.text import Tokenizer
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout

with open("mood.json") as data_file:
    data = json.load(data_file)["data"][0]

data = pd.DataFrame(data)


def clean_doc(doc):
    # split into tokens by whitespace
    tokens = doc.split()
    # prepare regex for char filtering
    re_punc = re.compile('[%s]' % re.escape(string.punctuation))
    # remove punctuation
    tokens = [re_punc.sub('', w) for w in tokens]
    # remove remaining non-alphabetical tokens
    tokens = [word for word in tokens if word.isalpha()]
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if w not in stop_words]
    # filter out short tokens
    tokens = [word for word in tokens if len(word) > 1]
    # make tokens lower case
    tokens = [word.lower() for word in tokens]
    return tokens


data["rating"] = data["rating"].apply(lambda x: int(float(x)))
data["alltext"] = data["title"].map(str) + data["text"]
data["alltext"] = data["alltext"].apply(lambda x: clean_doc(x))

X_train, X_test, y_train, y_test = train_test_split(data["alltext"], data["rating"], test_size=0.2, random_state=42)
class_weight = class_weight.compute_class_weight("balanced", np.unique(y_train), y_train)

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)

with open('tokenizer.pickle', "wb") as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

train_docs = tokenizer.texts_to_matrix(X_train, mode="binary")
test_docs = tokenizer.texts_to_matrix(X_test, mode="binary")

n_words = test_docs.shape[1]

model = Sequential()
model.add(Dense(50, input_shape=(n_words,), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(6, activation="softmax"))
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
model.fit(train_docs, y_train, epochs=10, verbose=2, class_weight=class_weight)

pred_labels = to_categorical(model.predict_classes(test_docs, verbose=0))
true_labels = y_test

TP = np.sum(np.logical_and(pred_labels == 1, true_labels == 1))
TN = np.sum(np.logical_and(pred_labels == 0, true_labels == 0))
FP = np.sum(np.logical_and(pred_labels == 1, true_labels == 0))
FN = np.sum(np.logical_and(pred_labels == 0, true_labels == 1))

accuracy = (TP + TN) / (TP + TN + FP + FN)
precision = TP / (TP + FP)
recall = TP / (TP + FN)
F1 = 2 * ((precision * recall) / (precision + recall))

print("Accuracy: ", accuracy)
print("Precision: ", precision)
print("Recall: ", recall)
print("F1-score: ", F1 )

# Serialize model to json

model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)

model.save_weights("model.h5")
print("Saved model to disk.")

