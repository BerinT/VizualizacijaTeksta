# Izdvajanje imenica, glagola, pridjeva i noun phrases

from textblob import TextBlob
import nltk

f = open("ngram.txt","rU")
lines = f.readlines()
f.close()
doc = ""

for line in lines:
    doc = doc+line

blob = TextBlob(doc)
noun_phrases = blob.noun_phrases
print(noun_phrases)

i = 0
new_file = open("ngram_cln.txt", "w")
while i<len(noun_phrases):
    new_file.write(str(noun_phrases[i]) + '\n')
    i = i+1
new_file.close()
