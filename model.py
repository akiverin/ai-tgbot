# coding: utf-8
import nltk
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from config import BOT_CONFIG, GIFTS
import random
from datetime import datetime

X_text = []
y = []

for intent, intent_data in BOT_CONFIG['intents'].items():
    for example in intent_data['examples']:
        X_text.append(example)
        y.append(intent)

vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(3, 3))
X = vectorizer.fit_transform(X_text)
clf = LinearSVC()
clf.fit(X, y)

def clear_phrase(phrase):
    phrase = phrase.lower()
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя- '
    result = ''.join(symbol for symbol in phrase if symbol in alphabet)
    return result.strip()

def classify_intent(replica):
    replica = clear_phrase(replica)
    intent = clf.predict(vectorizer.transform([replica]))[0]
    for example in BOT_CONFIG['intents'][intent]['examples']:
        example = clear_phrase(example)
        distance = nltk.edit_distance(replica, example)
        if example and distance / len(example) <= 0.5:
            return intent

def get_random_gift():
    gift = random.choice(GIFTS)
    response = f"🎁 {gift['name']} \n{gift['image']}"
    return response

def get_current_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

def get_answer_by_intent(intent):
    if intent in BOT_CONFIG['intents']:
        if intent == 'gift':
            return get_random_gift()
        if intent == 'time':
            return get_current_time()
        responses = BOT_CONFIG['intents'][intent]['responses']
        if responses:
            return random.choice(responses)

def update_model():
    global X_text, y, vectorizer, clf
    X_text = []
    y = []

    for intent, intent_data in BOT_CONFIG['intents'].items():
        for example in intent_data['examples']:
            X_text.append(example)
            y.append(intent)

    vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(3, 3))
    X = vectorizer.fit_transform(X_text)
    clf = LinearSVC()
    clf.fit(X, y)
