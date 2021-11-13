import os, signal
from os import listdir 

path = "./output/log-m1"
files = [f for f in listdir(path)]
print(len(files))
for file in files[:1]:
    if file.endswith('.xml'):
        name  = path + '/' + file
        commande = "timeout 5m java -jar choco-parsers-4.10.7-jar-with-dependencies.jar " + name
        os.system(commande)
    
path = "./output/log-m2"
files = [f for f in listdir(path)]
print(len(files))
for file in files[:1]:
    if file.endswith('.xml'):
        name  = path + '/' + file
        commande = "timeout 5m java -jar choco-parsers-4.10.7-jar-with-dependencies.jar " + name
        os.system(commande)
    
path = "./output/log-m3"
files = [f for f in listdir(path)]
print(len(files))
for file in files[:1]:
    if file.endswith('.xml'):
        name  = path + '/' + file
        commande = "timeout 5m java -jar choco-parsers-4.10.7-jar-with-dependencies.jar " + name
        os.system(commande)
