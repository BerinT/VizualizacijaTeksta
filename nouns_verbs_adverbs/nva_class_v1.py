import nltk
from nltk import word_tokenize, pos_tag

with open('ngram.txt','r') as f:
    data = f.read().replace('\n', '')
    data
nouns = [token for token, pos in pos_tag(word_tokenize(data)) if pos.startswith('N')]
print nouns
verbs = [token for token, pos in pos_tag(word_tokenize(data)) if pos.startswith('V')]
print verbs
adverbs = [token for token, pos in pos_tag(word_tokenize(data)) if pos.startswith('R')]
print adverbs

i = 0
new_file = open("nouns_cln.txt","w")
while i<len(nouns):
    new_file.write(str(nouns[i]) + '\n')
    i = i+1
new_file.close()

j = 0
new_file = open("verbs_cln.txt","w")
while j<len(verbs):
    new_file.write(str(verbs[j]) + '\n')
    j = j+1
new_file.close()

k = 0
new_file = open("adverbs_cln.txt","w")
while k<len(adverbs):
    new_file.write(str(adverbs[k]) + '\n')
    k = k+1
new_file.close()
