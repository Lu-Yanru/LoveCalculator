#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import nltk
#import nltk.corpus.reader.tagged as tagged
#import nltk.tag.hmm as hmm
import dill
#from os.path import exists
import util
from tensorflow.keras.models import load_model
from random import randint

# load sentiment analysis model
vocabulary = dill.load(open("vocabulary2.dat", "rb"))
model = load_model("classifier2.h5")

print("Herzlich willkommen, du bist hier genau richtig. Ich bin der schlauste LoveCalculator in der Welt und kann die Zukunft von dir und deinem Partner/deiner Partnerin vorhersagen.\n")
user = "neu"

def name_value(name):
    value = 0
    for c in name:
        value += ord(c) # Berechne die Summe von den Ascii-Werten von einer Zeichenkette
    return value % 100 + 1

while user != "":
    #user = nltk.word_tokenize(user)
    #user_tagged = pos_model.tag(user)
    if (re.match("(n|N)eu",user)): # Zufallselement: berechne einen Wert nach den Namen von den Nutzern
            user = input("Gib bitte deinen Namen und den Namen von deinem Partner / deiner Partnerin ein:\n")
            names = []
            for name in user.split():
                name = name.strip()
                names.append(name)
            love_name_value = (name_value(names[0])+name_value(names[1]))/2
            print(love_name_value)

    # Another random element: favourite colour
    ## Colour training
    colour, index = util.read_csv('colours.txt')
    love_colour0 = 0
    user = input("What's your favourite colour?")
    counter = 0
    for i in colour:
        if ( user == i):
            love_colour0 = index[counter]
            counter = counter + 1
        else:
            love_colour0 = randint(1,9)


    love_colour1 = 0
    user = input("What's your partner's favourite colour?")
    counters = 0
    for i in colour:
        if ( user == i):
            love_colour1 = index[counters]
            counters = counter + 1
        else:
            love_colour1 = randint(1,9)

    love_colour = (love_colour0 + love_colour1)/2
    if (love_colour < 3):
        print("You two are extremely different. Your couple's colour is icy as it can get: platinum")
    elif(love_colour<=5):
        print("You grow and understand each other. Your couple's colour is gold.")
    elif(love_colour > 5):
        print("Your energies are interesting when combined, your couple's colour is amethyst.")
    elif(love_colour > 10):
        print("You both are destined to be together, your colour is royal blue.")
    elif(love_colour > 15):
        print("Your love is true, your colour is burgundy.")

    user = input("Beschreib bitte deinen Partner / deine Partnerin kurz:\n") # Hauptelement: Sentiment analysis nach Angabe der Nutzer
    # every positive word count as some positive point and every negative word as some negative points
    user = nltk.word_tokenize(user)
    words,labels = util.read_csv("AFINN-111.txt")
    counter = 0
    sum_partner = 0
    for i in words:
        for j in user:
            if re.match(i, j):
                sum_partner += labels[counter]
        counter += 1
    love_partner = sum_partner/len(user) # calculate the average sentiment of the whole input
    print(love_partner)

    #nach der Beschreibung vom Partner
    user = input("Beschreib bitte deine persönliche Empfindung von eurer Beziehung: \n")
    # sentiment analysis (similar to imdb)
    sents = nltk.sent_tokenize(user)
    sum_relationship = 0
    x = util.create_bag_of_words(sents, vocabulary)
    y = model.predict(x)
    for i in range(0, len(y)):
        sum_relationship += y[i]
    love_relationship = sum_relationship/len(y)
    print(love_relationship) # Calculate average sentiment of all the input sentences, should be comment out before launched

    # results of calculation
    love_index = love_name_value*0.05 + love_color*0.05 + love_partner*0.3 + love_relationship*100*0.6
    if (love_index>=1 and love_index<=20):
        print("Bei euch beiden gefriert die Hölle.")
    elif(love_index>=21 and love_index<=40):
        print("Ihr seid wie Hund und Katze.")
    elif (love_index>=41 and love_index<=60):
        print("Da ist Langweile vorprogrammiert.")
    elif (love_index>=61 and love_index<=80):
        print("Bei euch beiden sprühen die Funken.")
    elif(love_index>=81 and love_index<=100):
        print("Das ist wahre Liebe.")

    #nach beiden Angaben gibt man Vorschläge
    user = input("Möchtest du Vorschläge von mir bekommen?\n") # Rückgabe je nach Ergebnis von der Berechnung oben
    if (re.search("((j|J)a)|((g|G)ern)", user)):
        if (love_index > 20):
            print("Outlook good, just ask them out on a date!")
        elif (love_index < 10):
            print("Just give up already!")
        elif (love_index == 50):
            print ("This escalated quickly")
        elif (love_index > 60):
            print("Come on chap, get your hopes up and ask them to be yours")
        elif (love_index > 90):
            print("You are clearly meant to be together...just marry already!")
        user = input("Tipp 'neu' ein, um einen neuen Test zu starten. Ansonsten drück die Enter-Taste, um den Test zu beenden.\n")
    else:
        break

print("Vielen Dank für deinen Besuch und auf Wiedersehen!")
