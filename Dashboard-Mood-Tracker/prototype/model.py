import json
import pandas as pd
import re
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

with open("dashboard_prototype/static/mood.json") as data_file:
    data = json.load(data_file)["data"][0]

data = pd.DataFrame(data)
data["title"] = data["title"].apply(lambda x: re.sub('[^a-zA-Z\s]', '', x.lower()))

vectorizer = CountVectorizer()
vectorizer.fit(data["title"])
sparse = vectorizer.transform(data["title"])
df = pd.DataFrame(sparse.toarray(), columns=vectorizer.get_feature_names())

X = df
y = data["rating"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf = RandomForestClassifier()
rf.fit(X_train, y_train)

pickle.dump(vectorizer, open("dashboard_prototype/static/language_model.sav", 'wb'))
pickle.dump(rf, open("dashboard_prototype/static/ml_model.sav", 'wb'))
