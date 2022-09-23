from ast import Break
from audioop import reverse
from email import message
import random
import json
import pickle
from unittest import result
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow import keras
from keras.models import load_model

import chatbotHelpers

lemmatizer = WordNetLemmatizer()
op = open('chatbot/intents.json')
intents = json.load(op)

words = pickle.load(open('chatbot/words.pkl', 'rb'))
classes = pickle.load(open('chatbot/classes.pkl', 'rb'))
model = load_model('chatbot/chatbot_model.h5')

def cleanUpSentence(sentence):
    sentenceWrods = nltk.word_tokenize(sentence)
    sentenceWrods = [lemmatizer.lemmatize(word) for word in sentenceWrods]
    return sentenceWrods


def bagOfWords(sentence):
    sentenceWrods = cleanUpSentence(sentence)
    bag = [0] * len(words)
    for w in sentenceWrods:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)
    

def predictClasses(sentence):
    bow = bagOfWords(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    
    results.sort(key=lambda x: x[1], reverse = True)
    returnList = []
    for r in results:
        returnList.append({'intent':classes[r[0]], 'probability':str(r[1])})
        
    return returnList

def getResponse(intentList, intentJson):
    tag = intentList[0]['intent']
    listOfIntents = intentJson['intents']
    # print(listOfIntents)
    for i in listOfIntents:
        if tag == 'jam':
            result = chatbotHelpers.GetHours()
            break
        if tag == 'umur':
            result = chatbotHelpers.GetNoesaAge()
            break
        if tag == "hari":
            result = chatbotHelpers.GetDay()
            break
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result



while True:
    print('the bot is running...')
    message = input('INPUT : ')
    ints = predictClasses(message)
    res = getResponse(ints, intents)
    print('BOT SAYS : ',  res)