import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

import nltk
# Below line is just needed once for the first-time run to download 'punkt'. Once, downloaded successfully then this line can commented.
# Plus, this line may not work from PyCharm if you are running behind Proxy Server; either disconnect VPN (if any) or add Proxy Server to PyCharm Settings.
# nltk.download('punkt')

import random
import numpy as np
import pandas as pd
import pickle
import json
import tensorflow as tf

from nltk.stem.lancaster import LancasterStemmer

from flask import Flask, jsonify, request
from flask_cors import CORS

lancasterStemmer = LancasterStemmer()

data = pickle.load(open("conversations-data.pkl", "rb"))
words = data['words']
classes = data['classes']


def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [lancasterStemmer.stem(sentence_word.lower()) for sentence_word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bag_of_words(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)

    # bag of words
    bag = [0] * len(words)
    for sentence_word in sentence_words:
        for index, word in enumerate(words):
            if word == sentence_word:
                bag[index] = 1
                if show_details:
                    print("FOUND in Bag: %s" % word)

    return (np.array(bag))


# Use pickle to load in the pre-trained model
global graph
# graph = tf.get_default_graph()
graph = tf.compat.v1.get_default_graph()

with open('conversations-model.pkl', 'rb') as model_file:
    conversation_model = pickle.load(model_file)


with open('intents.json') as json_data:
    intents_dict = json.load(json_data)
intents = intents_dict["intents"]


converationApp = Flask(__name__)
CORS(converationApp)

@converationApp.route("/converse", methods=['POST'])
def converse():
    ERROR_THRESHOLD = 0.25

    sentence = request.json['sentence']

    # generate probabilities from the model
    input_data = pd.DataFrame([bag_of_words(sentence, words)], dtype=float, index=['input'])
    results = conversation_model.predict([input_data])[0]

    # filter out predictions below a threshold
    results = [[index, result] for index, result in enumerate(results) if result > ERROR_THRESHOLD]

    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)

    conversation_intents = []
    for result in results:
        conversation_intents.append({"intent": classes[result[0]], "probability": str(result[1])})

    response = ''
    for intent in intents:
        if intent["tag"] == conversation_intents[0]["intent"]:
            responses = intent["responses"]
            index = random.randint(0, (len(responses) - 1))
            response = responses[index]
            print("Response: ", response)

    response_json = {
        'intent': conversation_intents[0]["intent"],
        'probability': conversation_intents[0]["probability"],
        'response': response
    }
    json_response_payload = json.dumps(response_json, indent=4)

    # json_response_payload = jsonify(conversation_intents)

    print("JSON Response Payload:\n", json_response_payload)
    return json_response_payload


# Running REST interface at Port=5001
if __name__ == "__main__":
#    converse()
    converationApp.run(debug=False, host='0.0.0.0', port=5001, threaded=False)