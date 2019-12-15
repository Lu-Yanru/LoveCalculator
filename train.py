import util
import dill

# CSV Datei einlesen
sentences, y = util.read_csv("sentiment.txt")

# Aufspalten in Training und Testmengen
# 75% der Daten zum Training, 25% zum Testen
split_position = int(len(sentences) * 0.75)
# Trainingsdaten
sentences_train = sentences[:split_position]
y_train = y[:split_position]
# Testdaten
sentences_test = sentences[split_position:]
y_test = y[split_position:]

# Erstelle Vokabular aus den Traningsdaten 
# und transformiere alle Sätze in Bag-Of-Words Vektoren
vocabulary = util.create_vocabulary(sentences_train)
x_train = util.create_bag_of_words(sentences_train, vocabulary)
x_test = util.create_bag_of_words(sentences_test, vocabulary)

from tensorflow.keras.models import Sequential
from tensorflow.keras import layers

# Definiere ein Neuronales Netz mit einem Bag-Of-Words Vektor als Eingabe
# einem Hidden Layer und einer Ausgabe
model = Sequential()
model.add(layers.Dense(10, input_dim=len(x_train[0]), activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

# Muss einmal "kompiliert" werden
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
print(model.summary())

# "fit" trainiert das Modell auf den gegebenen Daten
model.fit(x_train, y_train, epochs=20, validation_data=(x_test, y_test), batch_size=10)
model.save("classifier2.h5")
# Auch das Vokabular abspeichern, sonst können wir keine neuen Vektoren erstellen
dill.dump(vocabulary, open("vocabulary2.dat", "wb"))