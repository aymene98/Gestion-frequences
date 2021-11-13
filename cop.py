from pycsp3 import *

stations = data[0]
regions = data[1]
interferences = data[2]
liaisons = data[3]

domains = []
station_per_region = {}
for station in stations:
    domains.append([station[3], station[4]])
    if station[1] not in station_per_region.keys():
        station_per_region[station[1]] = []
    station_per_region[station[1]].append(station[0])

delta_station = [info[2] for info in stations]
    
emition = VarArray(size=len(stations), dom=lambda i : domains[i][0])
reception = VarArray(size=len(stations), dom=lambda i : domains[i][1])

#print([emition[i] for i in station_per_region[1]].extend([reception[i] for i in station_per_region[1]]))

satisfy(
    #difference de frequence emition et reception
    [abs(emition[i]-reception[i]) == delta_station[i] for i in range(len(delta_station))],

    # emition = reception dans les deux cotés
    [emition[liaisons[i][0]]==reception[liaisons[i][1]] for i in range(len(liaisons))],
    [emition[liaisons[i][1]]==reception[liaisons[i][0]] for i in range(len(liaisons))],

    # Gestion des interferances
    [abs(emition[interferences[i][1]]-reception[interferences[i][0]]) >= interferences[i][2] for i in range(len(interferences))],
    [abs(emition[interferences[i][0]]-reception[interferences[i][1]]) >= interferences[i][2] for i in range(len(interferences))],
    
    [abs(emition[interferences[i][1]]-emition[interferences[i][0]]) >= interferences[i][2] for i in range(len(interferences))],
    [abs(reception[interferences[i][0]]-reception[interferences[i][1]]) >= interferences[i][2] for i in range(len(interferences))],

    # Nombre maximale de frequences par region 
    [NValues([emition[i] for i in station_per_region[key]] + [reception[i] for i in station_per_region[key]]) <= regions[key] for key in station_per_region.keys()],
)

frequences = []
for key in station_per_region.keys():
    frequences += [emition[i] for i in station_per_region[key]]
    frequences += [reception[i] for i in station_per_region[key]]
    
if variant("m1") or not variant():
    minimize(
        # nombre de frequences utilisées
        NValues(frequences)
    )
elif variant("m2"):
    minimize(
        # Utiliser les fréquences les plus basses
        Maximum(frequences)
    )
elif variant("m3"):
    minimize(
        # Minimiser la largeur de la bande de fréquences utilisées
        Maximum(frequences)- Minimum(frequences)
    )