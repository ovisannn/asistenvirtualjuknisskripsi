from copyreg import pickle
import json
import random
import json
import pickle
from xml.dom.minidom import Document
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

import nltk
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# from tensorflow.keras.models import Sequential
import tensorflow
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

import time
# from symbol import factor

start = time.time()
lemmatizer = WordNetLemmatizer()
op = open('chatbot/intents.json', encoding="utf8")
intents = json.load(op)
# print(intents)
factory = StemmerFactory()
stemmer = factory.create_stemmer()

words = []
classes = []
documents = []
ignoreLetters = ['?', '!', '.', '.']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        wordList = nltk.word_tokenize(pattern)
        words.extend(wordList)
        documents.append((wordList, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
            
# print(documents)
words = [lemmatizer.lemmatize(word) for word in words if word not in ignoreLetters] #en
# words = [stemmer.stem(word) for word in words if word not in ignoreLetters] #indo
wrodds = sorted(set(words))
# print(words)

classes = sorted(set(classes))
# print(classes)

pickle.dump(words, open('chatbot/words.pkl', 'wb'))
pickle.dump(classes, open('chatbot/classes.pkl', 'wb'))

training = []
outputEmpty = [0] * len(classes)


for document in documents:
    # print(document)
    bag = []
    wordPatterns = document[0]
    wordPatterns = [lemmatizer.lemmatize(word.lower()) for word in wordPatterns]
    for word in words:
        bag.append(1) if word in wordPatterns else bag.append(0)
    
    outputRow = list(outputEmpty)
    outputRow[classes.index(document[1])] = 1
    training.append([bag, outputRow])

# print(training)
random.shuffle(training)
training = np.array(training, dtype='object')

trainX = list(training[:, 0])
trainY = list(training[:, 1])


model = Sequential()
model.add(Dense(len(trainX[0]), input_shape =(len(trainX[0]), ), activation='relu')) #128 256 512 1024 2048
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu')) #64 128 256 512 1024 2048
model.add(Dropout(0.5))
model.add(Dense(len(trainY[0]), activation='softmax'))


# sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
# sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.8, nesterov=True)
# sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.7, nesterov=True)
# sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.6, nesterov=True)
sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.5, nesterov=True)
# sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.4, nesterov=True)
# sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.3, nesterov=True)
# sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.2, nesterov=True)
# sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.1, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])


hist = model.fit(np.array(trainX), np.array(trainY), epochs= 1000, batch_size= 5, verbose= 1)
model.save('chatbot/chatbot_model.h5', hist)

model.summary()

end = time.time()

print(end-start)
# print(hist.history)
# loss_train = hist.history['loss']
acc = hist.history['accuracy']
epochs = range(0,1000)
# plt.plot(epochs, loss_train, 'g', label='Training loss')
plt.plot(epochs, acc, 'r', label ='training accuracy')
# plt.title('Training loss')
plt.title('Training accuracy')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()