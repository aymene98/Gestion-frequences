import os, time
from os import listdir 

path = "./output/log-m1"
files = [f for f in listdir(path)]
print(len(files))
for file in files:
    if file.endswith('.xml'):
        name  = path + '/' + file
        commande = "timeout 30s java -jar choco-parsers-4.10.7-jar-with-dependencies.jar " + name
        start = time.time()
        os.system(commande)
        print('\n',file, ' time:', time.time()-start)
    
path = "./output/log-m2"
files = [f for f in listdir(path)]
print(len(files))
for file in files:
    if file.endswith('.xml'):
        name  = path + '/' + file
        commande = "timeout 30s java -jar choco-parsers-4.10.7-jar-with-dependencies.jar " + name
        start = time.time()
        os.system(commande)
        print('\n',file, ' time:', time.time()-start)
    
path = "./output/log-m3"
files = [f for f in listdir(path)]
print(len(files))
for file in files:
    if file.endswith('.xml'):
        name  = path + '/' + file
        commande = "timeout 30s java -jar choco-parsers-4.10.7-jar-with-dependencies.jar " + name
        start = time.time()
        os.system(commande)
        print('\n',file, ' time:', time.time()-start)
