from pytoulbar2 import *
import json, sys, os
import itertools
import argparse
import pprint
import time

t0 = time.time()

pp = pprint.PrettyPrinter(indent=4)

myCFN = pytoulbar2.CFN(1000)

parser = argparse.ArgumentParser(description='Get file name to generate .CFN file.')
parser.add_argument('-n','--name', help='Name of the json file to parse', required=True)
parser.add_argument('-p',"--print_sol", type=bool, default=False,help="Print the problem's solution if found.")
args = vars(parser.parse_args())

file_name = args['name']
print_sol = args['print_sol']
f = open(file_name)
data = json.load(f)

top_value = 1000
molle_value = 5

# Creation de l'en-tete

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
# contrainte sur une station => contrainte dure
for i in range(0,len(data["stations"])):
    emeteur_name, recepteur_name = 'E'+str(i), 'R'+str(i)
    diff = []
    # boucle de produit scalaire des valeurs
    for combinaison in itertools.product(myCFN.Variables[emeteur_name], myCFN.Variables[recepteur_name]):
        if abs(int(combinaison[0][1:])-int(combinaison[1][1:])) == delta_station[i]:
            diff.append(0)
        else:
            diff.append(top_value)
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


name = file_name.split('/')[-1].split('.')[0] + '.cfn'
path = './output/CFN/'
sol = myCFN.Dump(path+name)