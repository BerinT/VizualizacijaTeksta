import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import csv
import random

# Pocetna obrada teksta -> izbacivanje priloga, zareza, ...


f = open("text_v4.txt","rU")
lines = f.readlines()
f.close()
doc = ""

for line in lines:
    doc = doc+line

tokens = nltk.word_tokenize(doc)
text = nltk.Text(tokens)
word = stopwords.words('english')
new_text = [w for w in text if (w.lower() not in word) and (len(w.lower())>3) and (str(w.lower())).isalpha()]

new_file = open("text_cleaned_v1.txt", "w")
for item in new_text:
    new_file.write(str(item) + " ")
new_file.close()



f = open("text_cleaned_v1.txt","rU")
text = f.read()
f.close()

words = list(text.split())
lower_words = []
i = 0
for word in words:
    lower_words.append(word.lower())


new_file1 = open("text_rdy_v6.csv","w")

pomocna_lista = []
for word in lower_words:
    if pomocna_lista.count(word)<1:
        pomocna_lista.append(word)
        # PRETPOSTAVKA: izvrseno skaliranje na frekvenciju (1-9)
        count = lower_words.count(word) # frekvencija ponavljanja rijeci
        if count > 2:
            line = str(word) + "," + str(random.uniform(0.5,9)) + "," +str(random.uniform(count-0.5,count+0.5)) + "," + str(lower_words.count(word)) + "\n"
        else:
            line = str(word) + "," + str(random.uniform(0.5,9)) + "," +str(random.uniform(0.5,2.5)) + "," + str(lower_words.count(word)) + "\n"
        new_file1.write(line)
new_file1.close()


