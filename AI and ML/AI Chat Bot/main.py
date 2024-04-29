import nltk
import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import pickle
import os
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()
nltk.download('punkt')

with open("intents.json") as file:
    data = json.load(file)

if os.path.exists("data.pickle"):
    with open("data.pickle", "rb") as f:
        words, labels, docs_x, docs_y, training, output = pickle.load(f)

else:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            w = nltk.word_tokenize(pattern)
            words.extend(w)
            docs_x.append(w)
            docs_y.append(intent["tag"])
        
        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    labels = sorted(labels)

    training, output = [], []
    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []
        doc = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in doc:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, docs_x, docs_y, training, output), f)

tf.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

if os.path.exists("model.tflearn"):
    model.load("model.tflearn")
else:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")

def bag_of_words(sentence, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(sentence)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for s in s_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    
    return np.array(bag)

def chat():
    print("Start chatting! Type quit to stop.")

    responses = []
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        results = model.predict([bag_of_words(user_input, words)])
        results_index = np.argmax(results)
        tag = labels[results_index]
        
        if results[results_index] >= 0.7:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']      

            print(f"Bootleg AI: {random.choice(responses)}\n")
        else:
            print("I'm sorry, I didn't understand your question. Please try again.\n")

chat()