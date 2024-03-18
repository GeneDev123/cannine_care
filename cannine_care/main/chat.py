import json
import random
import numpy as np
import nltk
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import datetime

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
  no_answer = ["Sorry, I'm not sure what you mean about dogs.", 
    "I'm not sure I understand your question about dogs.",
    "Could you provide more details about dogs?"]
  try:
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
      if i ['tag'] == tag:
        result = random.choice(i['responses'])
        break
    print(result)
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

def train_model(intents_dir):
  nltk.download("punkt")
  nltk.download("wordnet")

  with open(intents_dir) as file:
    data = json.load(file)

  words = []
  classes = []
  documents = []
  ignore_chars = ["?", "!", ".", ","]
  lemmatizer = WordNetLemmatizer()

  for intent in data["intents"]:
    for pattern in intent["patterns"]:
      # Tokenize and lemmatize words
      words_list = nltk.word_tokenize(pattern)
      words.extend(words_list)
      documents.append((words_list, intent["tag"]))
      if intent["tag"] not in classes:
        classes.append(intent["tag"])

  # Lemmatize and remove duplicates
  words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_chars]
  words = sorted(list(set(words)))

  # Sort classes
  classes = sorted(list(set(classes)))

  # Create training data
  training_data = []
  output_empty = [0] * len(classes)
  for document in documents:
    bag = []
    pattern_words = document[0]
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    for word in words:
      bag.append(1) if word in pattern_words else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1

    training_data.append((bag, output_row))

  random.shuffle(training_data)
  X_train = np.array([data[0] for data in training_data])
  y_train = np.array([data[1] for data in training_data])
  # training_data = np.array(training_data)

  # Neural Network architecture
  model = Sequential()
  model.add(Dense(120, input_shape=(len(X_train[0]),), activation="relu"))
  model.add(Dropout(0.5))
  model.add(Dense(64, activation="relu"))
  model.add(Dropout(0.5))
  model.add(Dense(len(y_train[0]), activation="softmax"))

  # Compile the model
  sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
  model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

  # Train the model
  model.fit(np.array(X_train), np.array(y_train), epochs=40, batch_size=10, verbose=1)

  # Save the model
  current_datetime = datetime.datetime.now()
  formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
  model_name = f"./main/chatbot-models/chatbot_{formatted_datetime}.h5"
  model.save(model_name)

  X_test = np.array([data[0] for data in training_data])
  y_test = np.array([data[1] for data in training_data])
  y_pred = model.predict(X_test)
  y_pred_classes = np.argmax(y_pred, axis=1)
  y_true = np.argmax(y_test, axis=1)

  accuracy = accuracy_score(y_true, y_pred_classes)
  precision = precision_score(y_true, y_pred_classes, average='weighted')
  recall = recall_score(y_true, y_pred_classes, average='weighted')
  f1 = f1_score(y_true, y_pred_classes, average='weighted')
  confusion_mat = confusion_matrix(y_true, y_pred_classes)

  target_names = [classes[i] for i in range(len(classes))]
  report = classification_report(y_true, y_pred_classes, target_names=target_names)
  
  print("============")
  print(accuracy)
  print(precision)
  print(recall)
  print(f1)  
  print(type(confusion_mat))
  # print(report)
  print("============")

  returnOutput = {
    "accuracy": str(round(accuracy, 4) * 100) + "%",
    "precision": str(round(precision, 4) * 100) + "%",
    "recall": str(round(recall, 4) * 100) + "%",
    "f1Score": str(round(f1, 4) * 100) + "%",
    "report": report,
    "confusionMat": confusion_mat.tolist(),
  }

  return returnOutput