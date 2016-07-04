import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import csv
import operator
import numpy as np

# Definisanje FUNKCIJA potrebnih za izvodjenje algoritma

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

# Funkcija "unutarOpsega" provjerava da li je rijec unutar definisanog opsega
def unutarOpsega(x11,x12,y11,y12,word,dictionary):
    opseg = vratiOpseg(word,dictionary)
    if opseg>1:
        # Ako je unutar opsega vrati 1
        if y11>=(opseg-0.5) and y11<(opseg+0.5):
            return 1
        else:
            return 0
    elif opseg==1:
        # Ako je unutar opsega vrati 1
        if y11>=(opseg-0.5) and y11<(opseg+1.5):
            return 1
        else:
            return 0
    else:
        return 0

# prisilnaKorekcija
def prisilnaKorekcija(dictionary,list_sorted):
    print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
    k = 0.1
    key = list_sorted[len(list_sorted)-1][0]
    preklapanje_rijeci = "True"

    x11 = dictionary[key][0]
    x12 = dictionary[key][1]
    y11 = dictionary[key][2]
    y12 = dictionary[key][3]
    f = dictionary[key][4]

    opseg = vratiOpseg(key,dictionary)
    if opseg!=1:
        opsegY1 = opseg-0.5
        opsegY2 = opseg+0.5
    else:
        opsegY1 = opseg-0.5
        opsegY2 = opseg+1.5

    dictionary[key] = 0.1, 0.1+(x12-x11), opsegY1+0.1, opsegY1+0.1+(y12-y11),f
    overlap = 0
    for key1,values1 in dictionary.iteritems():
        if (key1!=key and preklapanje(dictionary[key][0],dictionary[key][1],dictionary[key][2],dictionary[key][3],dictionary[key1][0],dictionary[key1][1],dictionary[key1][2],dictionary[key1][3])==1):
            overlap = overlap+1
    if overlap!=0:
        preklapanje_rijeci = "True"
    else:
        preklapanje_rijeci = "False"

    if preklapanje_rijeci == "True":
        while preklapanje_rijeci == "True":
            if y12+k < opsegY2 and x12<10:
                dictionary[key] = dictionary[key][0],dictionary[key][1],dictionary[key][2]+k,dictionary[key][3]+k,f
                overlap = 0
                for key1,values1 in dictionary.iteritems():
                    if key1!=key:
                        if (preklapanje(dictionary[key][0],dictionary[key][1],dictionary[key][2],dictionary[key][3],dictionary[key1][0],dictionary[key1][1],dictionary[key1][2],dictionary[key1][3])==1):
                            overlap = overlap+1
                if overlap!=0:
                    preklapanje_rijeci="True"
                else:
                    preklapanje_rijeci="False"

            elif y12+k>=opsegY2 and x12+k<10:
                dictionary[key] = dictionary[key][0]+k,dictionary[key][1]+k,opsegY1+0.1,opsegY1+0.1+(y12-y11),f
                overlap = 0
                for key1,values1 in dictionary.iteritems():
                    if key1!=key:
                        if (preklapanje(dictionary[key][0],dictionary[key][1],dictionary[key][2],dictionary[key][3],dictionary[key1][0],dictionary[key1][1],dictionary[key1][2],dictionary[key1][3])==1):
                            overlap = overlap+1
                if overlap!=0:
                    preklapanje_rijeci="True"
                else:
                    preklapanje_rijeci="False"
                    
            # Odradio citavu turu i nije bilo slobodnog prostora, pa prelazimo na novi algoritam
            
            elif x12+k>=10:
                out = 0
                for key1,values1 in dictionary.iteritems():
                    if (key1[0]-k)<=0:
                        out = out+1
                if out==0:
                    dictionary[key] = 0.1, 0.1+(x12-x11), opsegY1+0.1, opsegY1+0.1+(y12-y11),f
                    for key1, values1 in dictionary.iteritems():
                        if key1!=key:
                            dictionary[key1] = dictionary[0]-k,dictionary[1]-k,dictionary[2],dictionary[3],dictionary[4]
                else:
                    out1 = 0
                    for key1, values1 in dictionary.iteritems():
                        if key1!=key:
                            if (key1[2]-k)<=0:
                                out1 = out1+1
                    if out1==0:
                        dictionary[key] = 0.1, 0.1+(x12-x11), opsegY1+0.1, opsegY1+0.1+(y12-y11),f
                        for key1,values1 in dictionary.iteritems():
                            if key1!=key:
                                dictionary[key1] = dictionary[0],dictionary[1],dictionary[2]-k,dictionary[3]-k,dictionary[4]
                    else:
                        preklapanje_rijeci="False"

            else:
                preklapanje_rijeci = "False"
            
            
    
    return dictionary


# Funkcija "provjeraPutanje1" prima korigovane vrijednosti koordinata rijeci
# i provjerava da li su zadovoljeni kriteriji korigovane pozicije rijeci
# KRITERIJI: 1. Izlazak iz okvira 2. Izlazak iz opsega 3. Novo preklapanje
# 4. Greska
def provjeraPutanje1(x11,x12,y11,y12,word1,word2,dictionary):
    overlap = 0
    # Provjeravamo da li je unutar okvira (K1)
    if (unutarOkvira(x11,x12,y11,y12)==0):
        overlap = overlap+1
    # Provjeravamo da li je unutar opsega (K2)
    if (unutarOpsega(x11,x12,y11,y12,word1,dictionary)==0):
        overlap = overlap+1
    # Provjeravamo da li dolazi do novog preklapanja (K3)
    for key,values in dictionary.iteritems():
        if (key!=word1 and key!=word2):
            if (preklapanje(x11,x12,y11,y12,dictionary[key][0],dictionary[key][1],dictionary[key][2],dictionary[key][3])==1):
                overlap = overlap+1
    if (overlap!=0):
        return 1 # Korekcija ne ispunjava jedan od prva tri kriterija
    else:
        return 0 # Korekcija ispunjava sva tri kriterija

# Funkcija "provjeraPutanje2" provjerava validnost kriterija za drugu rijec
# KRITERIJI: 1. Izlazak iz okvira 2. Izlazak iz opsega 3. Novo preklapanje
# 4. Greska
# Bitna su nam prva dva kriterija, K3 ovisi od slucaja
def provjeraPutanje2(x21,x22,y21,y22,word1,word2,dictionary):
    overlap1 = 0
    overlap2 = 0
    # Provjeravamo da li je unutar okvira (K1):
    if (unutarOkvira(x21,x22,y21,y22)==0):
        overlap1 = overlap1+1
    # Provjeravamo da li je unutar opsega (K2):
    if (unutarOpsega(x21,x22,y21,y22,word2,dictionary)==0):
        overlap1 = overlap1+1
    # Provjeravamo da li se rijec vec preklapa s nekom drugom rijeci a da to nije prva
    for key,values in dictionary.iteritems():
        if(key!=word1 and key!=word2):
            if (preklapanje(dictionary[word2][0],dictionary[word2][1],dictionary[word2][2],dictionary[word2][3],dictionary[key][0],dictionary[key][1],dictionary[key][2],dictionary[key][3])==1):
                overlap2 = overlap2+1
    # Ako nije bilo ranijeg preklapanja sa nekom drugom rijeci
    if (overlap2==0):
        for key,values in dictionary.iteritems():
            if (key!=word1 and key!=word2):
                if (preklapanje(x21,x22,y21,y22,dictionary[key][0],dictionary[key][1],dictionary[key][2],dictionary[key][3])==1):
                    overlap1 = overlap1+1
        if (overlap1!=0):
            return 1 # Korekcija ne ispunjava sve kriterije
        else:
            return 0 # Korekcija ispunjava sve kriterije
    else :
        if (overlap1!=0):
            return 1 # Korekcija ne ispunjava sve kriterije
        else:
            return 0 # Korekcija ispunjava sve kriterije

# Funckija "idealnaPutanja" vraca idealnu putanju za pomjeranje rijeci
# Parametri koje prima su koordinate rijeci, rijeci i rjecnik
def idealnaPutanja(x11,x12,y11,y12,x21,x22,y21,y22,word1,word2,dictionary):
    # Koeficijent pomjeranja k
    k = 0.1

    # Preklapanje 1. vrste
    if ((x11<=x21 and x12>=x21) and (y11<=y22 and y12>=y22)):
        # Preklapanje 1.1.
        if(provjeraPutanje1(x11-k,x12-k,y11,y12,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21+k,x22+k,y21,y22,word1,word2,dictionary)==0):
                return "L-R"
            elif(provjeraPutanje2(x21+k,x22+k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "L-RD"
            elif(provjeraPutanje2(x21,x22,y21-k,y22-k,word1,word2,dictionary)==0):
                return "L-D"
            elif(provjeraPutanje2(x21-k,x22-k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "L-LD"
            elif(provjeraPutanje2(x21+k,x22+k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "L-RU"
            else:
                return "L"
        # Preklapanje 1.2.
        elif(provjeraPutanje1(x11-k,x12-k,y11+k,y12+k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21+k,x22+k,y21,y22,word1,word2,dictionary)==0):
                return "LU-R"
            elif(provjeraPutanje2(x21+k,x22+k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "LU-RD"
            elif(provjeraPutanje2(x21,x22,y21-k,y22-k,word1,word2,dictionary)==0):
                return "LU-D"
            elif(provjeraPutanje2(x21-k,x22-k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "LU-LD"
            elif(provjeraPutanje2(x21+k,x22+k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "LU-RU"
            else:
                return "LU"
        # Preklapanje 1.3.
        elif(provjeraPutanje1(x11,x12,y11+k,y12+k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21+k,x22+k,y21,y22,word1,word2,dictionary)==0):
                return "U-R"
            elif(provjeraPutanje2(x21+k,x22+k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "U-RD"
            elif(provjeraPutanje2(x21,x22,y21-k,y22-k,word1,word2,dictionary)==0):
                return "U-D"
            elif(provjeraPutanje2(x21-k,x22-k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "U-LD"
            elif(provjeraPutanje2(x21+k,x22+k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "U-RU"
            else:
                return "U"
        # Preklapanje 1.4.
        elif(provjeraPutanje1(x11+k,x12+k,y11+k,y12+k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21+k,x22+k,y21,y22,word1,word2,dictionary)==0):
                return "RU-R"
            elif(provjeraPutanje2(x21+k,x22+k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "RU-RD"
            elif(provjeraPutanje2(x21,x22,y21-k,y22-k,word1,word2,dictionary)==0):
                return "RU-D"
            elif(provjeraPutanje2(x21-k,x22-k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "RU-LD"
            else:
                return "RU"
        # Preklapanje 1.5.
        elif(provjeraPutanje1(x11-k,x12-k,y11-k,y12-k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21+k,x22+k,y21,y22,word1,word2,dictionary)==0):
                return "RD-R"
            elif(provjeraPutanje2(x21+k,x22+k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "RD-RD"
            elif(provjeraPutanje2(x21,x22,y21-k,y22-k,word1,word2,dictionary)==0):
                return "RD-D"
            elif(provjeraPutanje2(x21+k,x22+k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "RD-RU"
            else:
                return "RD"
        # Nema korekcije
        else:
            return "NO"
            
    # Preklapanje 2. vrste
    elif ((x11<=x22 and x12>=x22) and (y11<=y22 and y12>=y22)):
        # Preklapanje 2.1.
        if(provjeraPutanje1(x11+k,x12+k,y11,y12,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21-k,x22-k,y21,y22,word1,word2,dictionary)==0):
                return "R-L"
            elif(provjeraPutanje2(x21-k,x22-k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "R-LD"
            elif(provjeraPutanje2(x21,x22,y21-k,y22-k,word1,word2,dictionary)==0):
                return "R-D"
            elif(provjeraPutanje2(x21+k,x22+k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "R-RD"
            elif(provjeraPutanje2(x21-k,x22-k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "R-LU"
            else:
                return "R"
        # Preklapanje 2.2.
        elif(provjeraPutanje1(x11+k,x12+k,y11+k,y12+k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21-k,x22-k,y21,y22,word1,word2,dictionary)==0):
                return "RU-L"
            elif(provjeraPutanje2(x21-k,x22-k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "RU-LD"
            elif(provjeraPutanje2(x21,x22,y21-k,y22-k,word1,word2,dictionary)==0):
                return "RU-D"
            elif(provjeraPutanje2(x21+k,x22+k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "RU-RD"
            elif(provjeraPutanje2(x21-k,x22-k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "RU-LU"
            else:
                return "RU"
        # Preklapanje 2.3.
        elif(provjeraPutanje1(x11+k,x12+k,y11,y12,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21-k,x22-k,y21,y22,word1,word2,dictionary)==0):
                return "U-L"
            elif(provjeraPutanje2(x21-k,x22-k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "U-LD"
            elif(provjeraPutanje2(x21,x22,y21-k,y22-k,word1,word2,dictionary)==0):
                return "U-D"
            elif(provjeraPutanje2(x21+k,x22+k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "U-RD"
            elif(provjeraPutanje2(x21-k,x22-k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "U-LU"
            else:
                return "U"
        # Preklapanje 2.4.
        elif(provjeraPutanje1(x11-k,x12-k,y11+k,y12+k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21-k,x22-k,y21,y22,word1,word2,dictionary)==0):
                return "LU-L"
            elif(provjeraPutanje2(x21-k,x22-k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "LU-LD"
            elif(provjeraPutanje2(x21,x22,y21-k,y22-k,word1,word2,dictionary)==0):
                return "LU-D"
            elif(provjeraPutanje2(x21+k,x22+k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "LU-RD"
            else:
                return "LU"
        # Preklapanje 2.5.
        elif(provjeraPutanje1(x11+k,x12+k,y11-k,y12-k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21-k,x22-k,y21,y22,word1,word2,dictionary)==0):
                return "RD-L"
            elif(provjeraPutanje2(x21-k,x22-k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "RD-LD"
            elif(provjeraPutanje2(x21,x22,y21-k,y22-k,word1,word2,dictionary)==0):
                return "RD-D"
            elif(provjeraPutanje2(x21-k,x22-k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "RD-LU"
            else:
                return "RD"
        # Nema korekcije
        else:
            return "NO"
            
    # Preklapanje 3. vrste
    elif((x11<=x21 and x12>=x21) and (y11<=y21 and y12>=y21)):
        # Preklapanje 3.1.
        if(provjeraPutanje1(x11-k,x12-k,y11,y12,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21+k,x22+k,y21,y22,word1,word2,dictionary)==0):
                return "L-R"
            elif(provjeraPutanje2(x21+k,x22+k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "L-RU"
            elif(provjeraPutanje2(x21,x22,y21+k,y22+k,word1,word2,dictionary)==0):
                return "L-U"
            elif(provjeraPutanje2(x21-k,x22-k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "L-LU"
            elif(provjeraPutanje2(x21+k,x22+k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "L-RD"
            else:
                return "L"
        # Preklapanje 3.2.
        elif(provjeraPutanje1(x11-k,x12-k,y11-k,y12-k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21+k,x22+k,y21,y22,word1,word2,dictionary)==0):
                return "LD-R"
            elif(provjeraPutanje2(x21+k,x22+k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "LD-RU"
            elif(provjeraPutanje2(x21,x22,y21+k,y22+k,word1,word2,dictionary)==0):
                return "LD-U"
            elif(provjeraPutanje2(x21-k,x22-k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "LD-LU"
            elif(provjeraPutanje2(x21+k,x22+k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "LD-RD"
            else:
                return "LD"
        # Preklapanje 3.3.
        elif(provjeraPutanje1(x11,x12,y11-k,y12-k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21+k,x22+k,y21,y22,word1,word2,dictionary)==0):
                return "D-R"
            elif(provjeraPutanje2(x21+k,x22+k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "D-RU"
            elif(provjeraPutanje2(x21,x22,y21+k,y22+k,word1,word2,dictionary)==0):
                return "D-U"
            elif(provjeraPutanje2(x21-k,x22-k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "D-LU"
            elif(provjeraPutanje2(x21+k,x22+k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "D-RD"
            else:
                return "D"
        # Preklapanje 3.4.
        elif(provjeraPutanje1(x11+k,x12+k,y11-k,y12-k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21+k,x22+k,y21,y22,word1,word2,dictionary)==0):
                return "RD-R"
            elif(provjeraPutanje2(x21+k,x22+k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "RD-RU"
            elif(provjeraPutanje2(x21,x22,y21+k,y22+k,word1,word2,dictionary)==0):
                return "RD-U"
            elif(provjeraPutanje2(x21-k,x22-k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "RD-LU"
            else:
                return "RD"
        # Preklapanje 3.5.
        elif(provjeraPutanje1(x11-k,x12-k,y11+k,y12+k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21+k,x22+k,y21,y22,word1,word2,dictionary)==0):
                return "LU-R"
            elif(provjeraPutanje2(x21+k,x22+k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "LU-RU"
            elif(provjeraPutanje2(x21,x22,y21+k,y22+k,word1,word2,dictionary)==0):
                return "LU-U"
            elif(provjeraPutanje2(x21+k,x22+k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "LU-RD"
            else:
                return "LU"
        # Nema korekcije
        else:
            return "NO"
            
    # Preklapanje 4. vrste
    elif((x11<=x22 and x12>=x22) and (y11<=y21 and y12>=y21)):
        # Preklapanje 4.1.
        if(provjeraPutanje1(x11+k,x12+k,y11,y12,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21-k,x22-k,y21,y22,word1,word2,dictionary)==0):
                return "R-L"
            elif(provjeraPutanje2(x21-k,x22-k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "R-LU"
            elif(provjeraPutanje2(x21,x22,y21+k,y22+k,word1,word2,dictionary)==0):
                return "R-U"
            elif(provjeraPutanje2(x21+k,x22+k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "R-RU"
            elif(provjeraPutanje2(x21-k,x22-k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "R-LD"
            else:
                return "R"
        # Preklapanje 4.2.
        elif(provjeraPutanje1(x11+k,x12+k,y11-k,y12-k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21-k,x22-k,y21,y22,word1,word2,dictionary)==0):
                return "RD-L"
            elif(provjeraPutanje2(x21-k,x22-k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "RD-LU"
            elif(provjeraPutanje2(x21,x22,y21+k,y22+k,word1,word2,dictionary)==0):
                return "RD-U"
            elif(provjeraPutanje2(x21+k,x22+k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "RD-RU"
            elif(provjeraPutanje2(x21-k,x22-k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "RD-LD"
            else:
                return "RD"
        # Preklapanje 4.3.
        elif(provjeraPutanje1(x11,x12,y11-k,y12-k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21-k,x22-k,y21,y22,word1,word2,dictionary)==0):
                return "D-L"
            elif(provjeraPutanje2(x21-k,x22-k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "D-LU"
            elif(provjeraPutanje2(x21,x22,y21+k,y22+k,word1,word2,dictionary)==0):
                return "D-U"
            elif(provjeraPutanje2(x21+k,x22+k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "D-RU"
            elif(provjeraPutanje2(x21-k,x22-k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "D-LD"
            else:
                return "D"
        # Preklapanje 4.4.
        elif(provjeraPutanje1(x11-k,x12-k,y11-k,y12-k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21-k,x22-k,y21,y22,word1,word2,dictionary)==0):
                return "LD-L"
            elif(provjeraPutanje2(x21-k,x22-k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "LD-LU"
            elif(provjeraPutanje2(x21,x22,y21+k,y22+k,word1,word2,dictionary)==0):
                return "LD-U"
            elif(provjeraPutanje2(x21+k,x22+k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "LD-RU"
            else:
                return "LD"
        # Preklapanje 4.5.
        elif(provjeraPutanje1(x11+k,x12+k,y11+k,y12+k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21-k,x22-k,y21,y22,word1,word2,dictionary)==0):
                return "RU-L"
            elif(provjeraPutanje2(x21-k,x22-k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "RU-LU"
            elif(provjeraPutanje2(x21,x22,y21+k,y22+k,word1,word2,dictionary)==0):
                return "RU-U"
            elif(provjeraPutanje2(x21-k,x22-k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "RU-LD"
            else:
                return "RU"
        # Nema korekcije
        else:
            return "NO"

    # Preklapanje 5. vrste
    elif((x11>=x21 and x12<=x22) and (y11<=y21 and y12>=y21)):
        # Preklapanje 5.1.
        if(provjeraPutanje1(x11,x12,y11-k,y12-k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21,x22,y21+k,y22+k,word1,word2,dictionary)==0):
                return "D-U"
            elif(provjeraPutanje2(x21+k,x22+k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "D-RU"
            elif(provjeraPutanje2(x21-k,x22-k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "D-LU"
            else:
                return "D"
        # Preklapanje 5.2.
        elif(provjeraPutanje1(x11-k,x12-k,y11-k,y12-k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21+k,x22+k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "LD-RU"
            elif(provjeraPutanje2(x21,x22,y21+k,y22+k,word1,word2,dictionary)==0):
                return "LD-U"
            elif(provjeraPutanje2(x21-k,x22-k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "LD-LU"
            else:
                return "LD"
        # Preklapanje 5.3.
        elif(provjeraPutanje1(x11+k,x12+k,y11-k,y12-k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21-k,x22-k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "RD-LU"
            elif(provjeraPutanje2(x21,x22,y21+k,y22+k,word1,word2,dictionary)==0):
                return "RD-U"
            elif(provjeraPutanje2(x21+k,x22+k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "RD-RU"
            else:
                return "RD"
        # Nema korekcije
        else:
            print "Nema idealne putanje."
            return "NO"
            
    # Preklapanje 5'. vrste
    elif((x11<=x21 and x12>=x22) and (y11>=y21 and y11<=y22)):
        # Preklapanje 5.1.'
        if(provjeraPutanje1(x11,x12,y11+k,y12+k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21,x22,y21-k,y22-k,word1,word2,dictionary)==0):
                return "U-D"
            elif(provjeraPutanje2(x21-k,x22-k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "U-LD"
            elif(provjeraPutanje2(x21+k,x22+k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "U-RD"
            else:
                return "U"
        # Preklapanje 5.2.'
        elif(provjeraPutanje1(x11-k,x12-k,y11+k,y12+k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21+k,x22+k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "LU-RD"
            elif(provjeraPutanje2(x21,x22,y21-k,y22-k,word1,word2,dictionary)==0):
                return "LU-D"
            elif(provjeraPutanje2(x21-k,x22-k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "LU-LD"
            else:
                return "LU"
        # Preklapanje 5.3.'
        elif(provjeraPutanje1(x11+k,x12+k,y11+k,y12+k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21-k,x22-k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "RU-LD"
            elif(provjeraPutanje2(x21,x22,y21-k,y22-k,word1,word2,dictionary)==0):
                return "RU-D"
            elif(provjeraPutanje2(x21+k,x22+k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "RU-RD"
            else:
                return "RU"
        # Nema korekcije
        else:
            return "NO"

    # Preklapanje 6. vrste
    elif((x11>=x21 and x12<=x22) and (y11>=y21 and y11<=y22)):
        # Preklapanje 6.1.
        if(provjeraPutanje1(x11,x12,y11+k,y12+k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21,x22,y21-k,y22-k,word1,word2,dictionary)==0):
                return "U-D"
            elif(provjeraPutanje2(x21-k,x22-k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "U-LD"
            elif(provjeraPutanje2(x21+k,x22+k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "U-RD"
            else:
                return "U"
        # Preklapanje 6.2.
        elif(provjeraPutanje1(x11-k,x12-k,y11+k,y12+k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21+k,x22+k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "LU-RD"
            elif(provjeraPutanje2(x21,x22,y21-k,y22-k,word1,word2,dictionary)==0):
                return "LU-D"
            elif(provjeraPutanje2(x21-k,x22-k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "LU-LD"
            else:
                return "LU"
        # Preklapanje 6.3.
        elif(provjeraPutanje1(x11+k,x12+k,y11+k,y12+k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21-k,x22-k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "RU-LD"
            elif(provjeraPutanje2(x21,x22,y21-k,y22-k,word1,word2,dictionary)==0):
                return "RU-D"
            elif(provjeraPutanje2(x21+k,x22+k,y21-k,y22-k,word1,word2,dictionary)==0):
                return "RU-RD"
            else:
                return "RU"
        # Nema korekcije
        else:
            return "NO"

    # Preklapanje 6.' vrste
    elif((x11<=x21 and x12>=x22) and (y11<=y21 and y12>=y21)):
        # Preklapanje 6.1.'
        if(provjeraPutanje1(x11,x12,y11-k,y12-k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21,x22,y21+k,y22+k,word1,word2,dictionary)==0):
                return "D-U"
            elif(provjeraPutanje2(x21+k,x22+k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "D-RU"
            elif(provjeraPutanje2(x21-k,x22-k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "D-LU"
            else:
                return "D"
        # Preklapanje 6.2.'
        elif(provjeraPutanje1(x11-k,x12-k,y11-k,y12-k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21+k,x22+k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "LD-RU"
            elif(provjeraPutanje2(x21,x22,y21+k,y22+k,word1,word2,dictionary)==0):
                return "LD-U"
            elif(provjeraPutanje2(x21-k,x22-k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "LD-LU"
            else:
                return "LD"
        # Preklapanje 6.3.'
        elif(provjeraPutanje1(x11+k,x12+k,y11-k,y12-k,word1,word2,dictionary)==0):
            if(provjeraPutanje2(x21-k,x22-k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "RD-LU"
            elif(provjeraPutanje2(x21,x22,y21+k,y22+k,word1,word2,dictionary)==0):
                return "RD-U"
            elif(provjeraPutanje2(x21+k,x22+k,y21+k,y22+k,word1,word2,dictionary)==0):
                return "RD-RU"
            else:
                return "RD"
        # Nema korekcije
        else:
            return "NO"

    # Nije pronadjeno preklapanje nijedne vrste
    else:
        return "NO"


        
# ALGORITAM -> definisanje i pripremanje vrijednosti

fig,ax = plt.subplots()
fig.suptitle('Vizualizacija (nouns) prije korekcije sa pravougaonim granicama')
plt.xlabel('X-osa')
plt.ylabel('Frekvencija pojavljivanja rijeci')
r = fig.canvas.get_renderer()
reader = csv.reader(open('nouns.csv'))

# Rjecnik "dictionarystart" cuva kupi rijeci iz .csv fajla kao kljuceve
# i dodjeljuje im 3 vrijednosti (x1,y1 i frekvenciju)
dictionarystart = {}
for row in reader:
    key = row[0]
    if key in dictionarystart:
        pass
    dictionarystart[key] = row[1:]

# Definisemo ose grafike
ax.set_xlim([0,10])
ax.set_ylim([0,10])
ax.autoscale_view(False,False,False)

aspectratio = 1.0
ratio_default=(ax.get_xlim()[1]-ax.get_xlim()[0])/(ax.get_ylim()[1]-ax.get_ylim()[0])
ax.set_aspect(ratio_default*aspectratio)


# Rjecnik "dictionary1" kao kljuceve koristi rijeci a vrijednosti koje
# im dodjeljuju su sirina i visina svake rijeci, te frekvencija.
dictionary1 = {}
for key,values in dictionarystart.iteritems():
    ax.text(values[0],values[1],key,
            bbox=dict(facecolor='none',edgecolor='red',pad=1.0))
    
    t = plt.text(values[0],values[1],key,
            bbox=dict(facecolor='none',edgecolor='red',pad=1.0))
    bb = t.get_window_extent(renderer=r)
    
    if key in dictionary1:
        pass
    # Pretvaramo piksele u cm.
    dictionary1[key]= bb.width*0.026458333, bb.height*0.026458333, float(values[2])

# print dictionary1

# Rjecnik "dictionary2" kao kljuceve koristi rijeci a vrijednosti koje
# im dodjeljuje su koordinate x1,x2,y1,y2, te frekvencija.
dictionary2 = {}
for key,values in dictionary1.iteritems():
    if key in dictionary2:
        pass
    dictionary2[key] = float(dictionarystart[key][0]), float(dictionarystart[key][0])+float(dictionary1[key][0]), float(dictionarystart[key][1]), float(dictionarystart[key][1])+float(dictionary1[key][1]), dictionary1[key][2]
dictionary_sp = dict(dictionary2)
# print dictionary2
# plt.show()

# ALGORITAM -> izvrsavanje algoritma

i = 1
k = 0.1
overlapMIN = 100
keyMIN = ""
putanja = ""
dictionary_overlap = {}
n = 12
dif_keyMIN = ""
dictionary_temp = {}

# Radnju ponavljamo n (promjenljivo) puta, kako bismo ostvarili sto bolji
# rezultat
x = 0
r = 0
while x<=n:

    x = x+1
    
    if (x==11 and r<5):
        r = r+1
        for key3,values in dictionary2.iteritems():
            overlap = 0
            for key4,values in dictionary2.iteritems():
                if key3!=key4:
                    if (preklapanje(dictionary2[key][0],dictionary2[key][1],dictionary2[key][2],dictionary2[key][3],dictionary2[key1][0],dictionary2[key1][1],dictionary2[key1][2],dictionary2[key1][3])==1):
                        overlap = overlap+1
        if overlap!=0:
            dictionary_temp = dict(prisilnaKorekcija(dictionary2,list_sorted))
            dictionary2 = dict(dictionary_temp)
            x = 1
    

    # Prolazimo kroz rjecnik "dictionary2" kako bismo odredili koliko se puta
    # koja rijec preklapa
    for key,values in dictionary2.iteritems():
        overlap = 0
        # Odmah provjeravamo da li neka rijec se nalazi van okvira
        # x2 koordinata
        if (dictionary2[key][1]>=10.0):
            razlika = dictionary2[key][1]-9.9
            dictionary2[key] = dictionary2[key][0]-razlika,dictionary2[key][1]-razlika,dictionary2[key][2],dictionary2[key][3],dictionary2[key][4]
        # x1 koordinata
        if ((dictionary2[key][0]<=0)):
            razlika = abs(0.1-dictionary2[key][0])
            dictionary2[key] = dictionary2[key][0]+razlika,dictionary2[key][1]+razlika,dictionary2[key][2],dictionary2[key][3],dictionary2[key][4]
        # y2 koordinata
        if ((dictionary2[key][3]>=10.0)):
            razlika = dictionary2[key][3]-9
            dictionary2[key] = dictionary2[key][0],dictionary2[key][1],dictionary2[key][2]-razlika,dictionary2[key][3]-razlika,dictionary2[key][4]
        # y1 koordinata
        if ((dictionary2[key][2]<=0)):
            razlika = abs(0.1-dictionary2[key][2])
            dictionary2[key] = dictionary2[key][0],dictionary2[key][1],dictionary2[key][2]+razlika,dictionary2[key][3]+razlika,dictionary2[key][4]

        for key1,values1 in dictionary2.iteritems():
            if key1!=key:
                # Uslov za preklapanje
                if (preklapanje(dictionary2[key][0],dictionary2[key][1],dictionary2[key][2],dictionary2[key][3],dictionary2[key1][0],dictionary2[key1][1],dictionary2[key1][2],dictionary2[key1][3])==1):
                    overlap = overlap+1
        dictionary_overlap[key] = overlap

        # Ako smo odredili broj preklapanja za citav rjecnik, onda vrsimo sortiranje
        if i==len(dictionary2):
            # Sortiranje unutar liste sa kljucem (rijec) i brojem preklapanja
            list_sorted = sorted(dictionary_overlap.items(), key=operator.itemgetter(1))
            # Prolazimo kroz listu i rjesavamo problem
            for word in list_sorted:
                if word[1]>0:
                    keyMIN = word[0]
                    # Pronalazimo sa kojom rijeci se preklapa, te korigujemo
                    for key2,values2 in dictionary2.iteritems():
                        if (preklapanje(dictionary2[keyMIN][0],dictionary2[keyMIN][1],dictionary2[keyMIN][2],dictionary2[keyMIN][3],dictionary2[key2][0],dictionary2[key2][1],dictionary2[key2][2],dictionary2[key2][3])==1):
                            # nasli smo preklanje, sada vrsimo korekciju
                            putanja = idealnaPutanja(dictionary2[keyMIN][0],dictionary2[keyMIN][1],dictionary2[keyMIN][2],dictionary2[keyMIN][3],dictionary2[key2][0],dictionary2[key2][1],dictionary2[key2][2],dictionary2[key2][3],keyMIN,key2,dictionary2)
                            if putanja == "NO":
                                print "Ne postoji putanja bez postizanja nove kolizije."
                            else:
                                if putanja[0] == "D":
                                    dictionary2[keyMIN] = dictionary2[keyMIN][0],dictionary2[keyMIN][1],dictionary2[keyMIN][2]-k,dictionary2[keyMIN][3]-k, dictionary2[keyMIN][4]
                                elif putanja[0] == "L":
                                    dictionary2[keyMIN] = dictionary2[keyMIN][0]-k,dictionary2[keyMIN][1]-k,dictionary2[keyMIN][2],dictionary2[keyMIN][3], dictionary2[keyMIN][4]
                                elif putanja[0] == "U":
                                    dictionary2[keyMIN] = dictionary2[keyMIN][0],dictionary2[keyMIN][1],dictionary2[keyMIN][2]+k,dictionary2[keyMIN][3]+k, dictionary2[keyMIN][4]
                                elif putanja[0] == "R":
                                    dictionary2[keyMIN] = dictionary2[keyMIN][0]+k,dictionary2[keyMIN][1]+k,dictionary2[keyMIN][2],dictionary2[keyMIN][3], dictionary2[keyMIN][4]
                                if (len(putanja)==2 and putanja[1]!="-"):
                                    if putanja[1] == "D":
                                        dictionary2[keyMIN] = dictionary2[keyMIN][0],dictionary2[keyMIN][1],dictionary2[keyMIN][2]-k,dictionary2[keyMIN][3]-k, dictionary2[keyMIN][4]
                                    elif putanja[1] == "L":
                                        dictionary2[keyMIN] = dictionary2[keyMIN][0]-k,dictionary2[keyMIN][1]-k,dictionary2[keyMIN][2],dictionary2[keyMIN][3], dictionary2[keyMIN][4]
                                    elif putanja[1] == "U":
                                        dictionary2[keyMIN] = dictionary2[keyMIN][0],dictionary2[keyMIN][1],dictionary2[keyMIN][2]+k,dictionary2[keyMIN][3]+k, dictionary2[keyMIN][4]
                                    elif putanja[1] == "R":
                                        dictionary2[keyMIN] = dictionary2[keyMIN][0]+k,dictionary2[keyMIN][1]+k,dictionary2[keyMIN][2],dictionary2[keyMIN][3], dictionary2[keyMIN][4]

                                        
                                if (len(putanja)==3 and putanja[1]=="-"):
                                    if putanja[2] == "D":
                                        dictionary2[key2] = dictionary2[key2][0],dictionary2[key2][1],dictionary2[key2][2]-k,dictionary2[key2][3]-k, dictionary2[key2][4]
                                    elif putanja[2] == "L":
                                        dictionary2[key2] = dictionary2[key2][0]-k,dictionary2[key2][1]-k,dictionary2[key2][2],dictionary2[key2][3], dictionary2[key2][4]
                                    elif putanja[2] == "U":
                                        dictionary2[key2] = dictionary2[key2][0],dictionary2[key2][1],dictionary2[key2][2]+k,dictionary2[key2][3]+k, dictionary2[key2][4]
                                    elif putanja[2] == "R":
                                        dictionary2[key2] = dictionary2[key2][0]+k,dictionary2[key2][1]+k,dictionary2[key2][2],dictionary2[key2][3], dictionary2[key2][4]
                                if (len(putanja)==4 and putanja[1]=="-"):
                                    if putanja[2] == "D":
                                        dictionary2[key2] = dictionary2[key2][0],dictionary2[key2][1],dictionary2[key2][2]-k,dictionary2[key2][3]-k, dictionary2[key2][4]
                                    elif putanja[2] == "L":
                                        dictionary2[key2] = dictionary2[key2][0]-k,dictionary2[key2][1]-k,dictionary2[key2][2],dictionary2[key2][3], dictionary2[key2][4]
                                    elif putanja[2] == "U":
                                        dictionary2[key2] = dictionary2[key2][0],dictionary2[key2][1],dictionary2[key2][2]+k,dictionary2[key2][3]+k, dictionary2[key2][4]
                                    elif putanja[2] == "R":
                                        dictionary2[key2] = dictionary2[key2][0]+k,dictionary2[key2][1]+k,dictionary2[key2][2],dictionary2[key2][3], dictionary2[key2][4]
                                    if putanja[3] == "D":
                                        dictionary2[key2] = dictionary2[key2][0],dictionary2[key2][1],dictionary2[key2][2]-k,dictionary2[key2][3]-k, dictionary2[key2][4]
                                    elif putanja[3] == "L":
                                        dictionary2[key2] = dictionary2[key2][0]-k,dictionary2[key2][1]-k,dictionary2[key2][2],dictionary2[key2][3], dictionary2[key2][4]
                                    elif putanja[3] == "U":
                                        dictionary2[key2] = dictionary2[key2][0],dictionary2[key2][1],dictionary2[key2][2]+k,dictionary2[key2][3]+k, dictionary2[key2][4]
                                    elif putanja[3] == "R":
                                        dictionary2[key2] = dictionary2[key2][0]+k,dictionary2[key2][1]+k,dictionary2[key2][2],dictionary2[key2][3], dictionary2[key2][4]
                                if (len(putanja)==4 and putanja[2]=="-"):
                                    if putanja[1] == "D":
                                        dictionary2[keyMIN] = dictionary2[keyMIN][0],dictionary2[keyMIN][1],dictionary2[keyMIN][2]-k,dictionary2[keyMIN][3]-k, dictionary2[keyMIN][4]
                                    elif putanja[1] == "L":
                                        dictionary2[keyMIN] = dictionary2[keyMIN][0]-k,dictionary2[keyMIN][1]-k,dictionary2[keyMIN][2],dictionary2[keyMIN][3], dictionary2[keyMIN][4]
                                    elif putanja[1] == "U":
                                        dictionary2[keyMIN] = dictionary2[keyMIN][0],dictionary2[keyMIN][1],dictionary2[keyMIN][2]+k,dictionary2[keyMIN][3]+k, dictionary2[keyMIN][4]
                                    elif putanja[1] == "R":
                                        dictionary2[keyMIN] = dictionary2[keyMIN][0]+k,dictionary2[keyMIN][1]+k,dictionary2[keyMIN][2],dictionary2[keyMIN][3], dictionary2[keyMIN][4]
                                    if putanja[3] == "D":
                                        dictionary2[key2] = dictionary2[key2][0],dictionary2[key2][1],dictionary2[key2][2]-k,dictionary2[key2][3]-k, dictionary2[key2][4]
                                    elif putanja[3] == "L":
                                        dictionary2[key2] = dictionary2[key2][0]-k,dictionary2[key2][1]-k,dictionary2[key2][2],dictionary2[key2][3], dictionary2[key2][4]
                                    elif putanja[3] == "U":
                                        dictionary2[key2] = dictionary2[key2][0],dictionary2[key2][1],dictionary2[key2][2]+k,dictionary2[key2][3]+k, dictionary2[key2][4]
                                    elif putanja[3] == "R":
                                        dictionary2[key2] = dictionary2[key2][0]+k,dictionary2[key2][1]+k,dictionary2[key2][2],dictionary2[key2][3], dictionary2[key2][4]
                                if(len(putanja)==5):
                                    if putanja[1] == "D":
                                        dictionary2[keyMIN] = dictionary2[keyMIN][0],dictionary2[keyMIN][1],dictionary2[keyMIN][2]-k,dictionary2[keyMIN][3]-k, dictionary2[keyMIN][4]
                                    elif putanja[1] == "L":
                                        dictionary2[keyMIN] = dictionary2[keyMIN][0]-k,dictionary2[keyMIN][1]-k,dictionary2[keyMIN][2],dictionary2[keyMIN][3], dictionary2[keyMIN][4]
                                    elif putanja[1] == "U":
                                        dictionary2[keyMIN] = dictionary2[keyMIN][0],dictionary2[keyMIN][1],dictionary2[keyMIN][2]+k,dictionary2[keyMIN][3]+k, dictionary2[keyMIN][4]
                                    elif putanja[1] == "R":
                                        dictionary2[keyMIN] = dictionary2[keyMIN][0]+k,dictionary2[keyMIN][1]+k,dictionary2[keyMIN][2],dictionary2[keyMIN][3], dictionary2[keyMIN][4]
                                    if putanja[3] == "D":
                                        dictionary2[key2] = dictionary2[key2][0],dictionary2[key2][1],dictionary2[key2][2]-k,dictionary2[key2][3]-k, dictionary2[key2][4]
                                    elif putanja[3] == "L":
                                        dictionary2[key2] = dictionary2[key2][0]-k,dictionary2[key2][1]-k,dictionary2[key2][2],dictionary2[key2][3], dictionary2[key2][4]
                                    elif putanja[3] == "U":
                                        dictionary2[key2] = dictionary2[key2][0],dictionary2[key2][1],dictionary2[key2][2]+k,dictionary2[key2][3]+k, dictionary2[key2][4]
                                    elif putanja[3] == "R":
                                        dictionary2[key2] = dictionary2[key2][0]+k,dictionary2[key2][1]+k,dictionary2[key2][2],dictionary2[key2][3], dictionary2[key2][4]
                                    if putanja[4] == "D":
                                        dictionary2[key2] = dictionary2[key2][0],dictionary2[key2][1],dictionary2[key2][2]-k,dictionary2[key2][3]-k, dictionary2[key2][4]
                                    elif putanja[4] == "L":
                                        dictionary2[key2] = dictionary2[key2][0]-k,dictionary2[key2][1]-k,dictionary2[key2][2],dictionary2[key2][3], dictionary2[key2][4]
                                    elif putanja[4] == "U":
                                        dictionary2[key2] = dictionary2[key2][0],dictionary2[key2][1],dictionary2[key2][2]+k,dictionary2[key2][3]+k, dictionary2[key2][4]
                                    elif putanja[4] == "R":
                                        dictionary2[key2] = dictionary2[key2][0]+k,dictionary2[key2][1]+k,dictionary2[key2][2],dictionary2[key2][3], dictionary2[key2][4]
        else:
            i = i+1

fig1, ax1 = plt.subplots()
fig1.suptitle('Vizualizacija (nouns) nakon korekcije')
plt.xlabel('X-osa')
plt.ylabel('Frekvencija pojavljivanja rijeci')
fig2, ax2 = plt.subplots()
fig2.suptitle('Vizualizacija (nouns) prije korekcije')
plt.xlabel('X-osa')
plt.ylabel('Frekvencija pojavljivanja rijeci')

for key,values in dictionary2.iteritems():
    ax1.text(values[0],values[2],key)
for key,values in dictionarystart.iteritems():
    ax2.text(values[0],values[1],key)

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


# Upisivanje dictionary2 u .npy file
np.save('dictionary2_rezerva_nouns.npy', dictionary2)
# Upisivanje
np.save('dictionary_sp_rezerva_nouns.npy', dictionary_sp)

plt.show()
