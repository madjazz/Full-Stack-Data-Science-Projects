import pickle
import re
import string
from nltk.corpus import stopwords
from keras.models import model_from_json

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


def mood_tracker(mood):
    # Process input mood
    mood_list = list()
    mood_list.append(mood)
    mood_processed = [clean_doc(entry) for entry in mood_list]
    # Tokenize input mood
    with open("tokenizer.pickle", "rb") as handle:
        tokenizer = pickle.load(handle)
    mood_encoded = tokenizer.texts_to_matrix(mood_processed, mode="binary")
    # Load Keras model
    with open("model.json", "r") as json_model:
        model = json_model.read()
    model = model_from_json(model)
    model.load_weights("model.h5")
    return int(model.predict_classes(mood_encoded, verbose=0)[0])
