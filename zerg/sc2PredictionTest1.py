# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 18:45:11 2018

@author: User
"""

import pandas as pd

enemyBuildings = pd.read_csv("C:/Users/User/Documents/EnemyBuildingAmounts.csv")
weights = pd.read_csv("C:/Users/User/Documents/EnemyBuildingWeights.csv")
chance = pd.read_csv("C:/Users/User/Documents/enemyStratChance.txt", sep="\t")


def predictEnemy(enemyBuildings, weights, chance):
    agressiveExpansion = 0
    turtling = 0
    rush = 0
    straightToAir = 0
    groundAttack = 0
    biggestChance = 0
    
#Set chance matrix based off weights and quantity of each building type.
    chance["Chance"] += int(enemyBuildings["Nexus"][:1])*weights["Nexus"]
    chance["Chance"] += int(enemyBuildings["Gateway"][:1])*weights["Gateway"]
    chance["Chance"] += int(enemyBuildings["CC"][:1])*weights["CC"]
    chance["Chance"] += int(enemyBuildings["StarGate"][:1])*weights["StarGate"]
    chance["Chance"] += int(enemyBuildings["FleetBeacon"][:1])*weights["FleetBeacon"]
    chance["Chance"] += int(enemyBuildings["RoboticsFacility"][:1])*weights["RoboticsFacility"]
    chance["Chance"] += int(enemyBuildings["RoboticsBay"][:1])*weights["RoboticsBay"]
    chance["Chance"] += int(enemyBuildings["TwilightCouncil"][:1])*weights["TwilightCouncil"]
    chance["Chance"] += int(enemyBuildings["TemplarArchives"][:1])*weights["TemplarArchives"]
    chance["Chance"] += int(enemyBuildings["DarkShrine"][:1])*weights["DarkShrine"]
    chance["Chance"] += int(enemyBuildings["PC"][:1])*weights["PC"]
    
#Set mode chance as ints    
    agressiveExpansion = int(chance["Chance"][:1])
    turtling = int(chance["Chance"][1:2])
    rush = int(chance["Chance"][2:3])
    straightToAir = int(chance["Chance"][3:4])
    groundAttack = int(chance["Chance"][4:5])
    
#Compare chance values
    if biggestChance < agressiveExpansion:
        biggestChance = int(chance["Chance"][:1])
    if biggestChance < turtling:
        biggestChance = int(chance["Chance"][1:2])
    if biggestChance < rush:
        biggestChance = int(chance["Chance"][2:3])
    if biggestChance < straightToAir:
        biggestChance = int(chance["Chance"][3:4])
    if biggestChance < groundAttack:
        biggestChance = int(chance["Chance"][4:5])
       
#Return stuff
    if agressiveExpansion == biggestChance:
        biggestChance = "agressiveExpansion"
    if turtling == biggestChance:
        biggestChance = "turtling"
    if rush == biggestChance:
        biggestChance = "rush"
    if straightToAir == biggestChance:
        biggestChance = "straightToAir"
    if groundAttack == biggestChance:
        biggestChance = "groundAttack"
        
    return biggestChance
        
    
    
    
    
    
    
    
print(predictEnemy(enemyBuildings, weights, chance))


