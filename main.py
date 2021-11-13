import os
from os import listdir 

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

# creating the CFN files
# IMPORTANT : This step uses the pytoulbar2 library; Make sure to install it before hand 
# This step is optional if you already have the .cfn files
"""path = "./donnees/donnees_wcsp" # path to the directory of the json files
files = [f for f in listdir(path)]
for index, file in enumerate(files):
    if file.endswith('.json'):
        commande_create = "python3 create_cfn.py --name='"+path+"/"+file+"'"
        os.system(commande_create)"""
        
# IMPORTANT : This step uses the pytoulbar2 library; Make sure to install it before hand 
path = "./output/CFN" # path to the directory of the cfn files 
files = [f for f in listdir(path)]
for index, file in enumerate(files):
    if file.endswith('.cfn'):
        commande_solve = "python3 toulbar2.py -p='"+path+"/"+file+"'"
        # si tu veux afficher la solution trouver utilise cette commande
        #commande_solve = "python3 toulbar2.py -p='"+path+"/"+file+"' -ps=True"
        #print(commande)
        os.system(commande_solve)