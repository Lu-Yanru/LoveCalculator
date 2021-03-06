#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import nltk
#import nltk.corpus.reader.tagged as tagged
#import nltk.tag.hmm as hmm
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import dill
#from os.path import exists
import util
from tensorflow.keras.models import load_model
from random import randint
import chatbot

# load sentiment analysis model
vocabulary = dill.load(open("vocabulary2.dat", "rb"))
model = load_model("classifier2.h5")

print("Hi, I am your love pharmacist. It seems like you've found love. Let me give you the best recipe that I have at hand. Just answer to my questions.\n")
user = "new"

# Calculate the sum of the ASCII-value of a string of letters
def name_value(name):
    value = 0
    for c in name:
        value += ord(c)
    return value % 100 + 1

while user != "":
    #user = nltk.word_tokenize(user)
    #user_tagged = pos_model.tag(user)
    if (re.match("(n|N)ew",user)): # Random element: calculate a value according to the name of the user.
            user = input("Please tell me your name and your partner's name:\n")
            names = []
            for name in user.split():
                name = name.strip()
                names.append(name)
            if (len(names)>=2): # Error protection
                love_name_value = (name_value(names[0])+name_value(names[1]))/2
            else:
                print("Too many names baby. Please pick one to be your true love.")
                user = "new"
                continue
            print(love_name_value)


    # Another random element: favourite colour
    ## Feed in values of colours -> separate file so that you can change the values of the colours without changing the programme code
    colour, index = util.read_csv('colours.txt')
    user = input("What's your favourite colour?\n")
    counter = 0
    for i in colour:
        if ( user == i):
            love_colour0 = index[counter]
            counter = counter + 1
        else:
            love_colour0 = randint(1,9)

    user = input("What's your partner's favourite colour?\n")
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


    # Main element: Sentiment analysis according to the input of the user
    user = input("Please describe your partner:\n")
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
    print(love_partner) # control


    #after description of the partner
    user = input("Please describe your personal experience and feelings about your relationship:\n")
    # sentiment analysis (similar to imdb)
    sents = nltk.sent_tokenize(user)
    sum_relationship = 0
    x = util.create_bag_of_words(sents, vocabulary)
    y = model.predict(x)
    for i in range(0, len(y)):
        sum_relationship += y[i]
    love_relationship = sum_relationship/len(y)
    print(love_relationship) # Control, Calculate average sentiment of all the input sentences, should be comment out before launched


    # results of calculation
    love_index = love_name_value*0.05 + love_colour* 0.05 + love_partner*0.3 + love_relationship*100*0.6
    print(love_index) # Control
    if (love_index>=1 and love_index<=20):
        print("Between you freeze like hell.")
    elif(love_index>=21 and love_index<=40):
        print("You two are like cat and dog.")
    elif (love_index>=41 and love_index<=60):
        print("Here boredness is programmed beforehand.")
    elif (love_index>=61 and love_index<=80):
        print("There is sparkle between you.")
    elif(love_index>=81 and love_index<=100):
        print("This is true love.")


    #After the two inputs, give feedback according to the value of love_index
    print("Here is a love potion specially made for you:")
    if (love_index < 10):
        print("Outlook good, just ask them out on a date!")
    elif (love_index >= 20):
        print("Just give up already!")
    elif (love_index >= 40):
        print ("This escalated quickly")
    elif (love_index >= 60):
        print("Come on chap, get your hopes up and ask them to be yours")
    elif (love_index >= 90):
        print("You are clearly meant to be together...just marry already!")


    # chatbot function, that answers questions about relationship
    user = input("You came to me because you seem to have questions about your relationship. Now ask.\n")
    while user != "":
        res = chatbot.chatbot_response(user)
        user = input(res + "\n")

    user = input("Type in 'new' to start a new test, or else press enter to end the test.\n")

print("Thank you for your visit and hope to see you soon!")
