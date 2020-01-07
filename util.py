import nltk

# Liest eine CSV-Datei mit Sätzen und Labeln (0 negativ, 1 positiv) ein
def read_csv(file):
    sentences = []
    labels = []

    with open(file, "r") as f:
        # Jede Zeile der Datei einlesen
        for line in f.readlines():
            # Zeile in zwei Teile spalten (durch Tab getrennt)
            splitted = line.split('\t')
            # Den Satzteil und das Score jeweils an die entsprechende Liste anhängen
            sentences.append(splitted[0])
            # Das Label muss zu einer Zahl konvertiert werden
            labels.append(float(splitted[1]))
    # Beide Listen zurückgeben
    return (sentences, labels)

# Erstellt eine Liste von Bag-Of-Words-Vektoren für eine Liste von Sätzen.
def create_bag_of_words(sentences, vocabulary):
    result = []
    for s in sentences:
# Erstelle Liste mit nullen
# Die Liste ist so lang wie es Einträge im Vokuabular gibt (plus 1 für die 0)
# Jedes Listenelement entspricht der Anzahl der Token für die ID an dieser Position
        v = [0]*(len(vocabulary)+1)
        for token in nltk.tokenize.word_tokenize(s):
            token = token.lower()
# Unbekannte Wörter bekommen die ID 0
            identifier = 0
            if token in vocabulary:
# Schlage die ID für bekannte Wörter im Vokabular nach
                identifier = vocabulary[token]
# Erhöhe die Anzahl der Wörter mit dieser ID um 1
            v[identifier] = v[identifier] + 1
# Hänge den Bag-Of-Word Vektor für diesen Satz an das Ergebnis an
        result.append(v)
# Gebe die Bag-Of-Word Vektoren als Liste zurück
    return result
