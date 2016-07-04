import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import csv
import operator
import numpy as np

dictionary2 = np.load('dictionary2_1.npy').item()
dictionary_sp = np.load('dictionary_sp_rezerva.npy').item()

# Funkcija "preklapanje" provjerava postojanje preklapanja izmedju dvije rijeci
def preklapanje(x11,x12,y11,y12,x21,x22,y21,y22):
    if ((((x11<=x22) and (x22<=x12)) or ((x11<=x21) and (x21<=x12))) and
        (((y11<=y21) and (y21<=y12)) or ((y11<=y22) and (y22<=y12)))):
        return 1
    elif ((((x11<=x22) and (x22<=x12)) or ((x11<=x21) and (x21<=x12))) and
          ((y11>=y21) and (y12<=y22))):
        return 1
    elif ((((x11>=x21) and (x12<=x22)) or ((x11<=x21) and (x12>=x22))) and
          (((y11>=y21) and (y12<=y22)) or ((y11<=y21) and (y12>=y22)))):
        return 1
    else:
        return 0

# Funkcija "unutarOkvira" provjerava da li je rijec unutar definisanog okvira
def unutarOkvira(x11,x12,y11,y12):
    if ((x12>=10.0) or (x11<=0) or (y12>=10.0) or (y11<=0)):
        print "Rijec izlazi izvan okvira."
        return 0
    else:
        return 1

# Funkcija "vratiOpseg" je funkcija koja vraca opseg unutar kojeg rijec mora biti
def vratiOpseg(word,dictionary):
    if dictionary[word][2]>=8.5:
        return 9
    elif dictionary[word][2]>=7.5 and dictionary[word][2]<8.5:
        return 8
    elif dictionary[word][2]>=6.5 and dictionary[word][2]<7.5:
        return 7
    elif dictionary[word][2]>=5.5 and dictionary[word][2]<6.5:
        return 6
    elif dictionary[word][2]>=4.5 and dictionary[word][2]<5.5:
        return 5
    elif dictionary[word][2]>=3.5 and dictionary[word][2]<4.5:
        return 4
    elif dictionary[word][2]>=2.5 and dictionary[word][2]<3.5:
        return 3
    elif dictionary[word][2]>=0.5 and dictionary[word][2]<2.5:
        return 1
    else:
        return 0

k = 0.01
# "n" broj ponavljanja algoritma
n = 10
i = 0
j = 1
while i<n: 
    for key,values in dictionary2.iteritems():
        if k == 0.01:
        #if vratiOpseg(key,dictionary2)==1 or vratiOpseg(key,dictionary2)==3:
            if (dictionary2[key][0]-dictionary_sp[key][0])<0:
                kolizija = 0
                vanOkvira = 1
                while kolizija == 0 and dictionary2[key][0]<dictionary_sp[key][0] and vanOkvira == 1:
                    vanOkvira = unutarOkvira(dictionary2[key][0]+k, dictionary2[key][1]+k, dictionary2[key][2], dictionary2[key][3])
                    brojac = 0
                    g = 0
                    d = 0
                    for key1,values1 in dictionary2.iteritems():
                        if key1!=key:
                            kolizija = preklapanje(dictionary2[key][0]+k, dictionary2[key][1]+k, dictionary2[key][2], dictionary2[key][3], dictionary2[key1][0],dictionary2[key1][1],dictionary2[key1][2],dictionary2[key1][3])
                            if kolizija == 1 and (dictionary2[key][2]<=dictionary2[key1][3] and dictionary2[key][3]>dictionary2[key1][3]):
                                kolizija = preklapanje(dictionary2[key][0]+k, dictionary2[key][1]+k, dictionary2[key][2]+k, dictionary2[key][3]+k, dictionary2[key1][0],dictionary2[key1][1],dictionary2[key1][2],dictionary2[key1][3])
                                if kolizija == 0:
                                    g = 1
                            elif kolizija == 1 and (dictionary2[key][2]<=dictionary2[key1][2] and dictionary2[key][3]>dictionary2[key1][2]):
                                kolizija = preklapanje(dictionary2[key][0]+k, dictionary2[key][1]+k, dictionary2[key][2]-k, dictionary2[key][3]-k, dictionary2[key1][0],dictionary2[key1][1],dictionary2[key1][2],dictionary2[key1][3])
                                if kolizija == 0:
                                    d = 1
                            if kolizija == 1:
                                brojac = brojac + 1
                    if brojac == 0 and vanOkvira==1 and g==0 and d==0:
                        dictionary2[key] = dictionary2[key][0]+k, dictionary2[key][1]+k,dictionary2[key][2],dictionary2[key][3],dictionary2[key][4]
                    elif brojac==0 and vanOkvira==1 and g==1:
                        dictionary2[key] = dictionary2[key][0]+k, dictionary2[key][1]+k,dictionary2[key][2]+k,dictionary2[key][3]+k,dictionary2[key][4]
                    elif brojac==0 and vanOkvira==1 and d==1:
                        dictionary2[key] = dictionary2[key][0]+k, dictionary2[key][1]+k,dictionary2[key][2]-k,dictionary2[key][3]-k,dictionary2[key][4]
                    elif brojac != 0:
                        kolizija = 1

            elif (dictionary2[key][0]-dictionary_sp[key][0])>0:
                kolizija = 0
                vanOkvira = 1
                while kolizija == 0 and dictionary2[key][0]>dictionary_sp[key][0] and vanOkvira == 1:
                    vanOkvira = unutarOkvira(dictionary2[key][0]-k, dictionary2[key][1]-k, dictionary2[key][2], dictionary2[key][3])
                    brojac = 0
                    g = 0
                    d = 0
                    for key1,values1 in dictionary2.iteritems():
                        if key1!=key:
                            kolizija = preklapanje(dictionary2[key][0]-k, dictionary2[key][1]-k, dictionary2[key][2], dictionary2[key][3], dictionary2[key1][0],dictionary2[key1][1],dictionary2[key1][2],dictionary2[key1][3])
                            if kolizija == 1 and (dictionary2[key][2]<=dictionary2[key1][3] and dictionary2[key][3]>dictionary2[key1][3]):
                                kolizija = preklapanje(dictionary2[key][0]-k, dictionary2[key][1]-k, dictionary2[key][2]+k, dictionary2[key][3]+k, dictionary2[key1][0],dictionary2[key1][1],dictionary2[key1][2],dictionary2[key1][3])
                                if kolizija == 0:
                                    g = 1
                            elif kolizija == 1 and (dictionary2[key][2]<=dictionary2[key1][2] and dictionary2[key][3]>dictionary2[key1][2]):
                                kolizija = preklapanje(dictionary2[key][0]-k, dictionary2[key][1]-k, dictionary2[key][2]-k, dictionary2[key][3]-k, dictionary2[key1][0],dictionary2[key1][1],dictionary2[key1][2],dictionary2[key1][3])
                                if kolizija == 0:
                                    d = 1
                            if kolizija == 1:
                                brojac = brojac + 1
                    if brojac == 0 and vanOkvira==1 and g==0 and d==0:
                        dictionary2[key] = dictionary2[key][0]-k, dictionary2[key][1]-k,dictionary2[key][2],dictionary2[key][3],dictionary2[key][4]
                    elif brojac==0 and vanOkvira==1 and g==1:
                        dictionary2[key] = dictionary2[key][0]-k, dictionary2[key][1]-k,dictionary2[key][2]+k,dictionary2[key][3]+k,dictionary2[key][4]
                    elif brojac==0 and vanOkvira==1 and d==1:
                        dictionary2[key] = dictionary2[key][0]-k, dictionary2[key][1]-k,dictionary2[key][2]-k,dictionary2[key][3]-k,dictionary2[key][4]
                    elif brojac != 0:
                        kolizija = 1
    i = i+1

# Formiramo rjecnik "dictionary_error" za pohranjivanje unesene greske po x i y osi
dictionary_error = {}
x_avr = 0
y_avr = 0
for key,values in dictionary2.iteritems():
    if key in dictionary_error:
        pass
    dictionary_error[key] = abs(dictionary2[key][0]-dictionary_sp[key][0]), abs(dictionary2[key][2]-dictionary_sp[key][2])
    x_avr = x_avr + abs(dictionary2[key][0]-dictionary_sp[key][0])
    y_avr = y_avr + abs(dictionary2[key][2]-dictionary_sp[key][2])

# Prosjecna greska po x i y osi nakon izvrsenja algoritma
x_avr = x_avr/len(dictionary2)
y_avr = y_avr/len(dictionary2)


fig1, ax1 = plt.subplots()
fig1.suptitle('Vizualizacija (noun phrases) nakon korekcije')
plt.xlabel('X-osa')
plt.ylabel('Frekvencija pojavljivanja rijeci')
fig2, ax2 = plt.subplots()
fig2.suptitle('Vizualizacija (noun phrases) prije korekcije')
plt.xlabel('X-osa')
plt.ylabel('Frekvencija pojavljivanja rijeci')
aspectratio = 1.0
for key,values in dictionary2.iteritems():
    ax1.text(values[0],values[2],key,size=8.0)
for key,values in dictionary_sp.iteritems():
    ax2.text(values[0],values[2],key,size=8.0)

ax1.set_xlim([0, 10])
ax1.set_ylim([0, 10])
ax1.autoscale_view(False, False, False)

ax2.set_xlim([0, 10])
ax2.set_ylim([0, 10])
ax2.autoscale_view(False, False, False)

ratio_default1=(ax1.get_xlim()[1]-ax1.get_xlim()[0])/(ax1.get_ylim()[1]-ax1.get_ylim()[0])
ax1.set_aspect(ratio_default1*aspectratio)
ratio_default2=(ax2.get_xlim()[1]-ax2.get_xlim()[0])/(ax2.get_ylim()[1]-ax2.get_ylim()[0])
ax2.set_aspect(ratio_default2*aspectratio)

plt.show()
