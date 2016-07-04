import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import csv
import random

#f = open("nouns_cln_edt_v1.txt","rU")
f = open("verbs_cln_edt_v1.txt","rU")
text = f.read()
f.close()

words = list(text.split())
lower_words = []
i = 0
for word in words:
    lower_words.append(word.lower())


#new_file1 = open("nouns.csv","w")
new_file1 = open("verbs.csv","w")

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


