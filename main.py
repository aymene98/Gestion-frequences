import os
from os import listdir 

# Cette partie concerne l'execution du code de la partie COP pour tout 
# les fichiers de données qui sont dans le dossier ./donnee/cop
# dans cette partie on utilise la bibliothèque pycsp3 
# donc il est important de l'installer
"""path = "./donnees/donnees_cop"
files = [f for f in listdir(path)]
print(len(files))
for file in files:
    commande = "python3 cop.py -data='"+path+"/"+file + "' -solve -variant=m1"
    os.system(commande)
    commande = "python3 cop.py -data='"+path+"/"+file + "' -solve -variant=m2"
    os.system(commande)
    commande = "python3 cop.py -data='"+path+"/"+file + "' -solve -variant=m3"
    os.system(commande)"""

# Cette partie concerne l'execution du code de la partie WCSP pour tout 
# les fichiers de données qui sont dans le dossier ./donnee/wcsp

# creation des fichiers CFN
# IMPORTANT : This step uses the pytoulbar2 library; Make sure to install it before hand 
# This step is optional if you already have the .cfn files 
# for our case we have already generated the cfn files 
# and they are in the directory /output/CFN
"""path = "./donnees/donnees_wcsp" # path to the directory of the json files
files = [f for f in listdir(path)]
for index, file in enumerate(files):
    if file.endswith('.json'):
        commande_create = "python3 create_cfn.py --name='"+path+"/"+file+"'"
        os.system(commande_create)
        print('CFN file for the file ', file, ' was created')"""
        
# IMPORTANT : This step uses the pytoulbar2 library to solve the instances; 
# Make sure to install it before hand 
path = "./output/CFN" # path to the directory of the cfn files 
files = [f for f in listdir(path)]
for index, file in enumerate(files):
    if file.endswith('.cfn'):
        commande_solve = "python3 toulbar2.py -p='"+path+"/"+file+"'"
        # si on veut afficher la solution trouver on utilise cette commande
        #commande_solve = "python3 toulbar2.py -p='"+path+"/"+file+"' -ps=True"
        os.system(commande_solve)