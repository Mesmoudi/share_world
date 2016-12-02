# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 20:19:02 2014

@author: Noëline LEVI ALVARES
@licence: 
"""
import csv
from collections import defaultdict
from math import log
"""
import xml.etree.ElementTree as ET
tree = ET.parse('testMOOC.xml')
root = tree.getroot()


def infoInt(t):
    if (t == "{http://purl.org/dc/elements/1.1/}title") or (t == "{http://purl.org/dc/elements/1.1/}creator") or (t == "{http://purl.org/dc/elements/1.1/}date") or (t == "{http://purl.org/dc/elements/1.1/}description") or (t == "{http://purl.org/dc/elements/1.1/}language"):
        return(1)
    else:
        return(0)

listR = root[2]  # correspond au tag "ListRecords"
listG = []

for child in listR:
    if (child.tag == '{http://www.openarchives.org/OAI/2.0/}record'):
        article = child[1][0]  # correspond au tag "oai_dc:dc"
        # print ("Nv article: ", article.tag)
        listC = []
        for item in article:
            # print (item.tag)
            # print(item.text)
            if infoInt(item.tag) == 1:
                listC.append([item.tag, item.text])
        listG.append(listC)

# print("\n", "Liste générale:", listG)


file = open("articles.csv", "w")
fileW = csv.writer(file, lineterminator='\n')
fileW.writerow(["Index","Titre","Auteur","Description","Année de publication","Langue"])

n = 1
for l in listG:
    title = ""
    author = ""
    des = ""
    year = ""
    lg = ""
    for tup in l:
        if tup[0] == '{http://purl.org/dc/elements/1.1/}title':
            title = tup[1]
            # print("titre: ", title)
        elif tup[0] == '{http://purl.org/dc/elements/1.1/}creator':
            author += tup[1]
            author += " "
            # print("author: ", author)
        elif tup[0] == '{http://purl.org/dc/elements/1.1/}description':
            des = tup[1]
            # print("Description: ", des)
        elif tup[0] == '{http://purl.org/dc/elements/1.1/}date':
            year = tup[1]
            # print("Année: ", year)
        elif tup[0] == '{http://purl.org/dc/elements/1.1/}language':
            lg = tup[1]
            # print("Langue: ", lg)
    if (lg == 'eng') or (lg == 'en'):
        # print([n,title,author,des,year,lg])
        fileW.writerow([n,title,author,des,year,lg])
        n += 1

file.close()
"""

#  création d'1 liste de listes des descriptions et leur index inscrites ds le fichier csv
fileR = open("articles.csv", "r")
fileRR = csv.reader(fileR)
nb_doc = 0
description_IndexList = []
for row in fileRR:
    if (len(row) > 0) and (nb_doc != 0) and (nb_doc != 3) and (nb_doc != 4) and (nb_doc != 42):
        if (row[3] != ''):
            # print("Nouvel des : ",row[3])
            description_IndexList.append([row[3], nb_doc])
    nb_doc += 1
# print("Final string: ", description_IndexList)
fileR.close()


#  #enlever ponctuation
import string
punct = set(string.punctuation)
punct.add('"')
# print(punct)

#  création d'1 liste de listes des descriptions sans ponctuation et leur index
desInd_sansPunct = []
for tup in description_IndexList:
    for i in punct:
        tup[0] = tup[0].replace(i, '')
    desInd_sansPunct.append([tup[0].split(), tup[1]])
# print("Liste de liste des mots des différentes descriptions : ", desInd_sansPunct)

#  # Att : enlever research, result, also, overall
import nltk
from nltk.corpus import stopwords

stopW = set(stopwords.words('english'))
index = 0
wordsLLF = []  # liste de listes des mots de chaque descriptions
finalWordList = []  # liste  globale des mots ac doublons de toutes les descriptions
table_MotIndex = []  # table comportant cq mot (même doublons) ac l'index du document duquel il provient
for tup in desInd_sansPunct:
    newliste = []
    for word in tup[0]:
        if (word.lower() not in stopW):   # on supprime les mots ordinaires
            if(word.lower not in newliste):  #on supprime les doublons ds wordsLLF
                newliste.append(word.lower())  # on met tt en minuscule
                table_MotIndex.append([word.lower(), tup[1]])
            finalWordList = finalWordList + [word.lower()]
    wordsLLF.append(newliste)
    # finalWordList = finalWordList + newliste
# print("Liste finale : ", finalWordList)
# print("Liste de liste finale: ", wordsLLF)
# print("Liste index: ", table_MotIndex)

#  #création dico ac nb occurences de cq mot
ocL = {}.fromkeys(set(finalWordList), 0)
for valeur in finalWordList:
    ocL[valeur] += 1
# print(ocL)

#link_list = [[mooc,study][mooc,participant]...] => sert à former liens ds Gephi
link_list = []
# création matrix de coocurences de chaque paires de mots
def cooccurence_matrix_corpus(corpus,liste):
    # corpus = liste de liste de mots contenu ds 1 description --> faire cette liste!
    matrix = defaultdict(lambda: defaultdict(int))
    for description in corpus:
        for i in range(len(description)-1):
            for j in range(i+1, len(description)):
                word1 = description[i]
                word2 = description[j]
                liste.append([word1, word2])
                matrix[word1][word2] += 1
                matrix[word2][word1] += 1
    return matrix

co_ocM = cooccurence_matrix_corpus(wordsLLF, link_list)
# print(co_ocM)


fileL = open("links.csv", "w")
fileLW = csv.writer(fileL, lineterminator='\n')  # ne pas oublier lineterminator, sans quoi on a des lignes vides
fileLW.writerow(["Source", "Target"])
for tup in link_list:
    fileLW.writerow([tup[0], tup[1]])
fileL.close()


# création du dico de coocurence de chaque mot (moyenne des coocurences d'avec les autres mots)
co_ocL = {}.fromkeys(set(finalWordList), 0)
for valeur in set(finalWordList):
    nb_w = len(set(finalWordList))
    somme = 0
    for key, value in co_ocM[valeur].items():
        somme += value
    if nb_w != 0:
        co_ocL[valeur] = somme/nb_w
# print(co_ocL)


def iJacquart_matrix_corpus(corpus):
    # corpus = liste globale de tous les mots (sans doublons)
    matrix = defaultdict(lambda: defaultdict(float))
    for i in range(len(corpus)-1):
        for j in range(i+1, len(corpus)):
            word1 = corpus[i]
            word2 = corpus[j]
            co_ocr = co_ocM[word1][word2]
            sum_ocr = ocL[word1] + ocL[word2]
            matrix[word1][word2] = co_ocr/sum_ocr
            matrix[word2][word1] = co_ocr/sum_ocr
    return matrix

iJM = iJacquart_matrix_corpus(list(set(finalWordList)))

# création du dico de l'indice de Jacquart de chaque mot
iJL = {}.fromkeys(set(finalWordList), 0)
for valeur in set(finalWordList):
    nb_w = len(set(finalWordList))
    somme = 0
    for key, value in iJM[valeur].items():
        somme += value
    if nb_w != 0:
        iJL[valeur] = somme/nb_w
# print(iJL)


# renvoie un dico contenant le nb de doc contenant le mot word
def nombre_doc_contenant(word, corpus):
    n = 0
    for liste in corpus:
        if (word in liste):
            n += 1
    return n

# dico contenant chaque mot avec le nombre de doc le contenant
nb_doc_mot = {}.fromkeys(set(finalWordList), 0)
for word in set(finalWordList):
    nb_doc_mot[word] = nombre_doc_contenant(word, wordsLLF)
# print("Nombre de doc par mots: ", nb_doc_mot)

# dico contenant Inverse document frequency de chaque mot
idf = {}.fromkeys(set(finalWordList), 0)
for word in set(finalWordList):
    idf[word] = log((nb_doc - 1) / nb_doc_mot[word])
# print("idf par mots: ", idf)

tf = {}.fromkeys(set(finalWordList), 0)
for word in set(finalWordList):
    tf[word] = ocL[word]/len(finalWordList)
# print("tf par mots: ", tf)

tfidf = {}.fromkeys(set(finalWordList), 0)
for word in set(finalWordList):
    tfidf[word] = idf[word]*tf[word]
# print("tfidf par mots: ", tf)


#  #création du fichier de statistiques
fileS = open("wordStat.csv", "w")
fileSW = csv.writer(fileS, lineterminator='\n')  # ne pas oublier lineterminator, sans quoi on a des lignes vides
fileSW.writerow(["Mot", "Nb occurences", "Nb Co-occurences", "Indice de Jacquart", "Term frequency", "Inverse doc freq", "TF-IDF"])
for word in set(finalWordList):
    fileSW.writerow([word, ocL[word], co_ocL[word], iJL[word], tf[word], idf[word], tfidf[word]])
fileS.close()


#  #création du fichier d'index de chaque mot
fileIndex = open("wordsIndex.csv", "w")
fileIndexW = csv.writer(fileIndex, lineterminator='\n')  # ne pas oublier lineterminator, sans quoi on a des lignes vides
fileIndexW.writerow(["Mot", "Index"])
for tup in table_MotIndex:
    fileIndexW.writerow([tup[0], tup[1]])
fileIndex.close()


# création du fichier ordonné des mots selon tfidf
dataF = open('wordStat.csv', "r")
data = csv.reader(dataF)
l = 0
sortedlist = []
for row in data:
    if (l == 0):
        header = row
    else:
        line = row
        line[1] = float(line[1])  # mettre int si itemgetter = 1
        sortedlist.append(line)
    l += 1
import operator
sortedlist.sort(key=operator.itemgetter(6), reverse=True)
# print(sortedlist)
dataF.close()


fileOrdered = open("wordsOrd.csv", "w")
fileOrderedW = csv.writer(fileOrdered, lineterminator='\n')  # ne pas oublier lineterminator, sans quoi on a des lignes vides
fileOrderedW.writerow(header)
for row in sortedlist:
    fileOrderedW.writerow(row)
fileOrdered.close()

# réduction du fichier ordonné par seulement les 100 mots et l'indice intéressant
j = 0
liste100 = []  # liste des 100 mots retenus
fileOrdered = open("100wordsOrd.csv", "w")
fileOrderedW = csv.writer(fileOrdered, lineterminator='\n')  # ne pas oublier lineterminator, sans quoi on a des lignes vides
fileOrderedW.writerow(["Word", "TF-IDF"])
for row in sortedlist:  # on ne prend que 100 mots sur la totalité
    if (j < 100):
        fileOrderedW.writerow([row[0], row[6]])
        liste100 += [row[0]]
    else:
        break
    j += 1
fileOrdered.close()

# création du fichier de coocurences des 100 mots
co_occurenceListe100 = []
for i in range(len(liste100)-1):
        for j in range(i+1, len(liste100)):
            word1 = liste100[i]
            word2 = liste100[j]
            coo = co_ocM[word1][word2]
            co_occurenceListe100.append([word1, word2, coo])

fileLink = open("100links.csv", "w")
fileLinkW = csv.writer(fileLink, lineterminator='\n')  # ne pas oublier lineterminator, sans quoi on a des lignes vides
fileLinkW.writerow(["Source", "Target", "Co-occurence"])
for row in co_occurenceListe100:  
    fileLinkW.writerow(row)
fileLink.close()