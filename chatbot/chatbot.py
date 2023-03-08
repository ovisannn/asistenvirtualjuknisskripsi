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
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


from tensorflow import keras
from keras.models import load_model


lemmatizer = WordNetLemmatizer()
op = open('chatbot/intents.json')
intents = json.load(op)
factory = StemmerFactory()
stemmer = factory.create_stemmer()

words = pickle.load(open('chatbot/words.pkl', 'rb'))
classes = pickle.load(open('chatbot/classes.pkl', 'rb'))
model = load_model('chatbot/chatbot_model.h5')

def cleaningUpExpression(sentence):
    cleanSentence = sentence
    removeWordsList = [
        "apa",
        "mengapa",
        "sih",
        "apasih",
        "tolong",
        "jelaskan",
        "bagaimana",
        "diampu",
        "memegang",
        "sebutkan",
        "itu"
    ]
    for i in removeWordsList:
        if i in sentence:
            # print('true')
            cleanSentence= cleanSentence.replace(i, '')
    #menghillangkan kata apa apasih sih mengapa dsb
    # print('func cleaning() :'+cleanSentence)
    return cleanSentence

def cleanUpSentence(sentence):
    sentenceWrods1 = cleaningUpExpression(sentence)
    sentenceWrods = nltk.word_tokenize(sentenceWrods1)
    # print(sentence)
    print(sentenceWrods)
    sentenceWrods = [lemmatizer.lemmatize(word) for word in sentenceWrods] #en
    print(sentenceWrods)
    sentenceWrods = [stemmer.stem(word) for word in sentenceWrods] #indo
    print(sentenceWrods)
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
    sentence = sentence.lower()
    bow = bagOfWords(sentence)
    # print(bow)
    res = model.predict(np.array([bow]))[0]
    # ERROR_THRESHOLD = 0.92
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # print(results[0][1])
    # if results[0][1] < ERROR_THRESHOLD:
    #     return {'intent': '0', 'probability': ''}
    results.sort(key=lambda x: x[1], reverse = True)
    returnList = []
    for r in results:
        returnList.append({'intent':classes[r[0]], 'probability':str(r[1])})
    # print(returnList)
    return returnList

def getResponse(intentList, intentJson):
    print(intentList[0]['probability'])
    ERROR_THRESHOLD = 0.80
    if float(intentList[0]['probability'])< ERROR_THRESHOLD:
        return "Mohon maaf masukan tidak dikenali"
    tag = intentList[0]['intent']
    listOfIntents = intentJson['intents']
    # print(tag)
    for i in listOfIntents:
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