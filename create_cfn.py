from pytoulbar2 import *
import json, itertools, argparse

# 1000 is the upper bound (we set it as equal to TOP)
myCFN = pytoulbar2.CFN(1000)

parser = argparse.ArgumentParser(description='Get file name to generate .CFN file.')
parser.add_argument('-n','--name', help='Name of the json file to parse', required=True)
args = vars(parser.parse_args())

file_name = args['name']
f = open(file_name)
data = json.load(f)

top_value = 1000 # cost for hard constraint
molle_value = 5 # cost for not so hard contraints

# creation des variables et leurs domaines de definition
for i in range(0,len(data["stations"])):
    emeteur_name = 'E'+str(i)
    recepteur_name = 'R'+str(i)
    myCFN.AddVariable(emeteur_name, ["f"+str(i) for i in data["stations"][i]['emetteur']])
    myCFN.AddVariable(recepteur_name, ["f"+str(i) for i in data["stations"][i]['recepteur']])

# creation de liste pour les information utiles pour les contraintes
delta_station=[]
for station in data["stations"]:
    delta_station.append(station["delta"])

liaison_station = []
for liaison in data["liaisons"]:
    liaison_station.append( (liaison["x"], liaison["y"]) )

interferences_station = []
for interference in data["interferences"]:
    interferences_station.append((interference["x"], interference["y"], interference["Delta"]))

# creation des contraintes
# contrainte sur le delta dans une station => contrainte dure
for i in range(0,len(data["stations"])):
    emeteur_name, recepteur_name = 'E'+str(i), 'R'+str(i)
    diff = []
    # boucle de produit scalaire des valeurs des domaines des definitions
    for combinaison in itertools.product(myCFN.Variables[emeteur_name], myCFN.Variables[recepteur_name]):
        if abs(int(combinaison[0][1:])-int(combinaison[1][1:])) == delta_station[i]:
            diff.append(0) # pas de violation de la contrainte
        else:
            diff.append(top_value) # violation de la contrainte
    myCFN.AddFunction(scope=[emeteur_name, recepteur_name], costs=diff)

# contrainte emition == reception => contrainte dure
for (s1, s2) in liaison_station:
    #print(s1, s2)
    emeteur_name, recepteur_name = 'E'+str(s1), 'R'+str(s2)
    diff = []
    for combinaison in itertools.product(myCFN.Variables[emeteur_name], myCFN.Variables[recepteur_name]):
        if combinaison[0]==combinaison[1] :
            diff.append(0)
        else:
            diff.append(top_value)
    myCFN.AddFunction(scope=[emeteur_name, recepteur_name], costs=diff)
    
    emeteur_name, recepteur_name = 'E'+str(s2), 'R'+str(s1)
    diff = []
    for combinaison in itertools.product(myCFN.Variables[emeteur_name], myCFN.Variables[recepteur_name]):
        if combinaison[0]==combinaison[1] :
            diff.append(0)
        else:
            diff.append(top_value)
    myCFN.AddFunction(scope=[emeteur_name, recepteur_name], costs=diff)

# contrainte interference => contrainte molle
for (s1, s2, delta) in interferences_station:
    emeteur_name, recepteur_name = 'E'+str(s1), 'R'+str(s2)
    diff = []
    for combinaison in itertools.product(myCFN.Variables[emeteur_name], myCFN.Variables[recepteur_name]):
        if abs(int(combinaison[0][1:])-int(combinaison[1][1:])) >= delta:
            diff.append(0)
        else:
            diff.append(molle_value)
    myCFN.AddFunction(scope=[emeteur_name, recepteur_name], costs=diff)
    
    emeteur_name, recepteur_name = 'E'+str(s2), 'R'+str(s1)
    diff = []
    for combinaison in itertools.product(myCFN.Variables[emeteur_name], myCFN.Variables[recepteur_name]):
        if abs(int(combinaison[0][1:])-int(combinaison[1][1:])) >= delta:
            diff.append(0)
        else:
            diff.append(molle_value)
    myCFN.AddFunction(scope=[emeteur_name, recepteur_name], costs=diff)

    emeteur_name, recepteur_name = 'E'+str(s1), 'E'+str(s2)
    diff = []
    for combinaison in itertools.product(myCFN.Variables[emeteur_name], myCFN.Variables[recepteur_name]):
        if abs(int(combinaison[0][1:])-int(combinaison[1][1:])) >= delta:
            diff.append(0)
        else:
            diff.append(molle_value)
    myCFN.AddFunction(scope=[emeteur_name, recepteur_name], costs=diff)

    emeteur_name, recepteur_name = 'R'+str(s1), 'R'+str(s2)
    diff = []
    for combinaison in itertools.product(myCFN.Variables[emeteur_name], myCFN.Variables[recepteur_name]):
        if abs(int(combinaison[0][1:])-int(combinaison[1][1:])) >= delta:
            diff.append(0)
        else:
            diff.append(molle_value)
    myCFN.AddFunction(scope=[emeteur_name, recepteur_name], costs=diff)

# creating du nom du fichier CFN
name = file_name.split('/')[-1].split('.')[0] + '.cfn'
path = './output/CFN/'
sol = myCFN.Dump(path+name) # sauvegarde du fichier CFN 
# on pourait juste changer l'extession dans le nom du fichier à .wcsp et avoir un fichier xcsp