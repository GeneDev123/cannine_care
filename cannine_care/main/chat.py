import json
import random
import numpy as np
import nltk
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import SGD

def initialize_static_chatbot_requirements(model_dir, intents_dir):
  model = load_model(model_dir, compile=False)
  sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
  model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])
  
  with open(intents_dir) as file:
    data = json.load(file)

  words = []
  classes = []
  documents = []
  ignore_chars = ["?", "!", ".", ","]
  lemmatizer = WordNetLemmatizer()

  for intent in data["intents"]:
    for pattern in intent["patterns"]:
      words_list = nltk.word_tokenize(pattern)
      words.extend(words_list)
      documents.append((words_list, intent["tag"]))
      if intent["tag"] not in classes:
        classes.append(intent["tag"])

  words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_chars]
  words = sorted(list(set(words)))
  classes = sorted(list(set(classes)))

  return {
    'model': model,
    'data': data,
    'words': words,
    'ignore_chars': ignore_chars,
    'lemmatizer': lemmatizer,
    'classes': classes,
  }

def predict_class(sentence, model, words, ignore_chars, lemmatizer, classes):
  p = bow(sentence, words, ignore_chars, lemmatizer, show_details=False)
  res = model.predict(np.array([p]))[0]
  ERROR_THRESHOLD = 0.30
  results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
  results.sort(key=lambda x: x[1], reverse=True)
  return_list = []
  for r in results:
    return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
  return return_list

def get_response(intents_list, intents_json):
  no_answer = ["Sorry, I do not understand", "Sorry, can you elaborate?", "Sorry, can you give more information?"]
  try:
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
      if i ['tag'] == tag:
        result = random.choice(i['responses'])
        break
    return result
  except:
    result = random.choice(no_answer)
    return result

def clean_up_sentence(sentence, ignore_chars, lemmatizer):
  words_list = nltk.word_tokenize(sentence)
  words_list = [lemmatizer.lemmatize(word.lower()) for word in words_list if word not in ignore_chars]
  return words_list

def bow(sentence, words, ignore_chars, lemmatizer, show_details=True):
  sentence_words = clean_up_sentence(sentence, ignore_chars, lemmatizer)
  bag = [0] * len(words)
  for s in sentence_words:
    for i, word in enumerate(words):
      if word == s:
        bag[i] = 1
        if show_details:
          print(f"Found in bag: {word}")
  return np.array(bag)