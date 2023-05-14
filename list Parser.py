# -*- coding: utf-8 -*-
"""
Created on Mon May  1 10:47:22 2023

@author: Arlana Davis
"""
import re
from os import walk

class gameList:
    name: str
    lis: str
    listType: str
    detachments: list()
    faction: list()
    subfaction: ()
    subfaction: str
    units: dict()
        
    def __init__(self, lis, typ, name):
        self.name = name
        self.lis = lis
        self.detachments = list()
        self.faction = list()
        self.subfaction = str()
        self.units = dict()
        self.listType = typ

def determineType(lis):
    if "HQ1" in lis:
        return "40001";
    if "battlescribe" in lis:
        return "bs";
    return "other"

def determineDetachments (subject):
   if subject.listType == "40001":
       if "Arks of Omen" in subject.lis:
           subject.detachments.append("arks")
       if "Detachment" in subject.lis:
           res = [i.start() for i in re.finditer("Detachment", subject.lis)]
           for i in res:
               ii = i-2
               detachmentType = ""
               while(subject.lis[ii] != " "):
                   detachmentType+= subject.lis[ii]
                   ii-=1
               subject.detachments.append(detachmentType[::-1])
   else:
       if "Detachment" in subject.lis:
           res = [i.start() for i in re.finditer("Detachment", subject.lis)]
           for i in res:
               if subject.lis[i+11] != "C":
                   ii = i-2
                   detachmentType = ""
                   while(subject.lis[ii] != " "):
                       detachmentType+= subject.lis[ii]
                       ii-=1
                   if detachmentType == "nemO":
                        subject.detachments.append("arks")
                   else: 
                       subject.detachments.append(detachmentType[::-1])
    
def determineFaction(subject):
    
    if subject.listType == "40001":
        index  = subject.lis.index("Factions")
        subject.faction = ""
        i = index+15
        while (subject.lis[i] != "," and subject.lis[i] != "-" and subject.lis[i] != '\n'):
            subject.faction += subject.lis[i]
            i+=1
    else:
        index  = subject.lis.index("Detachment")
        subject.faction = ""
        i = index+12
        while (subject.lis[i] != "," and subject.lis[i] != "-" and subject.lis[i] != '\n' and subject.lis[i] != ')'):
            subject.faction += subject.lis[i]
            i+=1
    if subject.faction == "Imperium " or subject.faction == "Aeldari " or subject.faction == "Chaos ":
        subject.faction = ""
        i+=2
        while (subject.lis[i] != "," and subject.lis[i] != "-" and subject.lis[i] != '\n' and subject.lis[i] != ')'):
            subject.faction += subject.lis[i]
            i+=1
    if subject.faction == "Tyranids " and subject.lis.contains("Cult Creed"):
        subject.faction = "Genestealer Cults"
    return subject
        
def determineSubfaction(subject):
    subfaction = ""
    temp = ""
    index = 0
    if subject.listType == "40001":
        if subject.faction == "Adeptus Astartes ":
            index = subject.lis.index("Adeptus Astartes")
            index+=19
            while subject.lis[index] != "," and subject.lis[index] != "\n" and subject.lis[index] != "\n" :
                subfaction+=subject.lis[index]
                temp = subfaction
                index+=1
        index = subject.lis.index("==")
        index+=2
        while (subject.lis[index] != "=" and subject.lis[index] != "\n"):
            subfaction+=subject.lis[index]
            index+=1
        subfaction = subfaction.replace("Arks of Omen", "")
        subfaction = subfaction.replace("Patrol Detachment", "")
        subfaction = subfaction.replace("Battalion Detachment", "")
        subfaction = subfaction.replace("Outrider Detachment", "")
        subfaction = subfaction.replace("Vanguard Detachment", "")
        subfaction = subfaction.replace("Spearhead Detachment", "")
        subfaction = subfaction.replace("Brigade Detachment", "")
        subfaction = subfaction.replace("Supreme Command Detachment", "")
        subfaction = subfaction.replace("Super-Heavy Auxiliary Detachment", "")
        subfaction = subfaction.replace("Super-Heavy Detachment", "")
        temp = temp.replace("\n", "")
        temp2 = subfaction.count(temp)
        subfaction = subfaction.replace("\n", "")
        if  temp2 > 1:
            subfaction = subfaction.replace(temp, "", 1)
    else:
        #imperium
        if subject.faction == "Adeptus Astartes ":
            index = subject.lis.index("**Chapter Selector**")
            index+=21
            while subject.lis[index] != "," and subject.lis[index] != "\n" :
                index+=1
                subfaction+=subject.lis[index]
        if subject.faction == "Adeptus Custodes":
            index = subject.lis.index("Shield Host")
            index+=30
            while subject.lis[index] != "," and subject.lis[index] != "\n" :
                index+=1
                subfaction+=subject.lis[index]
        if subject.faction == "Adeptus Mechanicus":
            index = subject.lis.index("Forge World Choice: ")
            print(subject.name, index, "something should be here mech")
            index+=19
            while subject.lis[index] != "\n":
                index+=1
                subfaction+=subject.lis[index]
        if subject.faction == "Adepta Sororitas":
            index = subject.lis.index("Order Convictions: ")
            index+=18
            while subject.lis[index] != "," and subject.lis[index] != "\n" :
                index+=1
                subfaction+=subject.lis[index]
        if subject.faction == "Astra Militarum":
            index = subject.lis.index("Regimental Doctrine: ")
            index+=20
            while subject.lis[index] != "," and subject.lis[index] != "\n" :
                index+=1
                subfaction+=subject.lis[index]
        if subject.faction == "Imperial Knights":
            index = subject.lis.index("Questor Allegiance: ")
            index+=19
            while subject.lis[index] != "," and subject.lis[index] != "\n" :
                index+=1
                subfaction+=subject.lis[index]
        if subject.faction == "Grey Knights":
            index = subject.lis.index("Brotherhood: ")
            index+=12
            while subject.lis[index] != "," and subject.lis[index] != "\n" :
                index+=1
                subfaction+=subject.lis[index]
        #chaos
        if subject.faction == "Chaos Knights":
            index = subject.lis.index("House")
            while subject.lis[index] != "," and subject.lis[index] != "\n" :
                index+=1
                subfaction+=subject.lis[index]
        if subject.faction == "World Eaters":
            if subject.lis[index].contains("Disciples of The Red Angel"):
                subfaction = "Disciples of The Red Angel"
            else:
                subfaction = "World Eaters"
        if subject.faction == "Death Guard":
            index = subject.lis.index("Plague Company: ")
            index+=15
            while subject.lis[index] != "," and subject.lis[index] != "\n" :
                index+=1
                subfaction+=subject.lis[index]
        if subject.faction == "Thousand Sons":
            index = subject.lis.index("Cults of the Legion: ")
            index+=20
            while subject.lis[index] != "," and subject.lis[index] != "\n":
                index+=1
                subfaction+=subject.lis[index]
        if subject.faction == "Chaos Space Marines":
            index = subject.lis.index("Legion: ")
            index+=7
            while subject.lis[index] != "," and subject.lis[index] != "\n":
                index+=1
                subfaction+=subject.lis[index]
        if subject.faction == "Daemons":
            index = subject.lis.index("Chaos Allegiance: ")
            index+=17
            while subject.lis[index] != "," and subject.lis[index] != "\n":
                index+=1
                subfaction+=subject.lis[index]
        #xenos
        if subject.faction == "Necrons":
            index = subject.lis.index("Dynasty Choice: ")
            index+=15
            while subject.lis[index] != "," and subject.lis[index] != "\n":
                index+=1
                subfaction+=subject.lis[index]
        if subject.faction == "Leagues of Votann":
            index = subject.lis.index("League: ")
            index+=7
            while subject.lis[index] != "," and subject.lis[index] != "\n":
                index+=1
                subfaction+=subject.lis[index]
        if subject.faction == "Tyranids":
            index = subject.lis.index("Hive Fleet: ")
            index+=11
            while subject.lis[index] != "," and subject.lis[index] != "\n":
                index+=1
                subfaction+=subject.lis[index]
        if subject.faction == "Genestealer Cults":
            index = subject.lis.index("Cult Creed: ")
            index+=11
            while subject.lis[index] != "," and subject.lis[index] != "\n":
                index+=1
                subfaction+=subject.lis[index]    
        if subject.faction == "T'au Empire":
            index = subject.lis.index("Sept Choice: ")
            index+=12
            while subject.lis[index] != "," and subject.lis[index] != "\n":
                index+=1
                subfaction+=subject.lis[index]
        if subject.faction == "Orks":
            index = subject.lis.index("Clan Kultur: ")
            index+=12
            while subject.lis[index] != "," and subject.lis[index] != "\n":
                index+=1
                subfaction+=subject.lis[index]
        if subject.faction == "Harlequins":
            index = subject.lis.index("Saedath Characterisation: ")
            index+=26
            while subject.lis[index] != "," and subject.lis[index] != "\n":
                index+=1
                subfaction+=subject.lis[index]
    subfaction.strip()
    subfaction = subfaction.replace("\n", "")
    return subfaction
        
    
#def parseList():
subject = []
mypath = input("Please enter the directory of the list files: ")
f = []
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    break

for i in range(len(f)):
    lis = open((mypath+f[i]), "r").read()
    subject.append(gameList(lis, determineType(lis), f[i]))
    determineDetachments(subject[i])
    subject[i] = determineFaction(subject[i])
    subject[i].subfaction = determineSubfaction(subject[i])

for i in range(len(subject)):
    print(subject[i].name, "/", end="")
    #for ii in range(len(subject[i].detachments)-1):
    ii=0
    print("", subject[i].detachments[ii], "/", subject[i].faction, "/", subject[i].subfaction, end="")
    print("")
input("press enter to continue")


#return subject

#main
#parseList()