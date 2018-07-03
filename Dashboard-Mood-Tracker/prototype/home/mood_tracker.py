import re
import pickle


def mood_tracker(mood):

    mood_list = list()
    mood_list.append(mood)
    mood_processed = [re.sub('[^a-zA-Z\s]', '', mood.lower()) for mood in mood_list]

    with open("home/static/language_model.sav", 'rb') as language_model:
        vectorizer = pickle.load(language_model)

    mood_transformed = vectorizer.transform(mood_processed)

    with open("home/static/ml_model.sav", 'rb') as ml_model:
        rf = pickle.load(ml_model)

    return int(float(rf.predict(mood_transformed)[0]))
