# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 14:33:37 2018

@author: User
"""
import pandas as pd
import numpy as np
import random as rd
#all the functions 



#Build buildings 
def buildBuilding(BuildingName, Quantity):
    #Select worker
    #Convert into building in valid location
    return
    
#Build units
def buildUnits(UnitName, Quantity):
    #Select larva
    #build imput unit
    return
    


#Create control group
def makeControlGroup(UnitsForControlGroup):
    #Select the correct amount of the targeted units
    #Set them to a control group
    return


 
#Move control group    
def moveControlGroup(controlGroup, moveType, absoluteX, absoluteY):
    #Select control group
    #Select move type
    #Move units
    return
    


#My buildings
def myBuildings():
    #Make/update 2d array of all building types, how many of each building, absX, & absY
    return mybuildings




#Enemy buildings
def enemyBuildings():
    #Make/update 2d array of all enemy buildings, how many of each building, absX, & absY
    return enemyBuildings




#Enemy units 
def enemyUnits():
    #Make/update 2d array of all enemy units, type, quantity, location
    return enemyUnits




#Expand
def expand():
    #Builds new hatchery and queen and drones
    return




def buildOrder(myStrat, gameStage, enemyUnits):
    
    if gameStage == "Start":
        print("Build Order:   Start" + "\n" + "12: drone" + "\n" + "13: drone" + "\n" + "14: Spawning Pool" + 
                  "\n" + "13: drone" + "\n" + "14: overlord" + "\n" + "14: Extractor" + "\n" + "13: drone"
                  + "\n" + "14: drone" + "\n" + "15: zergling*2")
    
    if gameStage == "Opener":
        if myStrat == 'Harass':
            print("Build Order:   Opener - Harass" + "\n" + "16: drone" + "\n" + "17: drone" + "\n" + "18: drone" + 
                  "\n" + "19: queen" + "\n" + "21: Roach Warren" + "\n" + "20: overlord" + "\n" + 
                  "20: overlord" + "\n" + "20: roach*7" + "\n" + "34: Hatchery")
    
        if myStrat == 'Rush':
            print("Build Order:   Opener - Rush" + "\n" + "16: drone" + "\n" + "17: queen" + "\n" + 
                  "19: lings & lords")
            
        if myStrat == "Expand":
            print("Build Order:   Opener - Expand" + "\n" + "12: drone" + "\n" + "13: overlord" + "\n" + "13: drone*4" +
                  "\n" + "17: Hatchery" + "\n" + "16: drone*2" + "\n" + "18: Extractor" + "\n" + 
                  "17: Spawning Pool" + "\n" + "17: drone*2" + "\n" + "19: overlord" + "\n" + "19: drone" + 
                  "\n" + "20: queen*2" + "\n" + "24: ling*3" + "\n" + "27: Roach Warren")
        
        else:
            myStrat == 'Rush'
            
    if gameStage == "MidGame":
        print("Mid Game Unit Comp")   
    
    if gameStage == "LateGame":
        print("Late Game Unit Comp")
    
    return


#Predict enemy
def predictEnemy(enemyBuildings, buildingWeights, enemyUnits, unitWeights, chance, enemyRace):
    agressiveExpansion = 0
    turtling = 0
    rush = 0
    straightToAir = 0
    groundAttack = 0
    biggestChance = 0
    
#Set chance matrix based off weights and quantity of each building type. 
    if enemyRace == "protoss":
        chance["Chance"] += int(enemyBuildings["Nexus"][:1])*buildingWeights["Nexus"]
        chance["Chance"] += int(enemyBuildings["Gateway"][:1])*buildingWeights["Gateway"]
        chance["Chance"] += int(enemyBuildings["CC"][:1])*buildingWeights["CC"]
        chance["Chance"] += int(enemyBuildings["StarGate"][:1])*buildingWeights["StarGate"]
        chance["Chance"] += int(enemyBuildings["FleetBeacon"][:1])*buildingWeights["FleetBeacon"]
        chance["Chance"] += int(enemyBuildings["RoboticsFacility"][:1])*buildingWeights["RoboticsFacility"]
        chance["Chance"] += int(enemyBuildings["RoboticsBay"][:1])*buildingWeights["RoboticsBay"]
        chance["Chance"] += int(enemyBuildings["TwilightCouncil"][:1])*buildingWeights["TwilightCouncil"]
        chance["Chance"] += int(enemyBuildings["TemplarArchives"][:1])*buildingWeights["TemplarArchives"]
        chance["Chance"] += int(enemyBuildings["DarkShrine"][:1])*buildingWeights["DarkShrine"]
        chance["Chance"] += int(enemyBuildings["PC"][:1])*buildingWeights["PC"]
        
    if enemyRace == "terran":
        chance["Chance"] += int(enemyBuildings["CC"][:1])*buildingWeights["CC"]
        chance["Chance"] += int(enemyBuildings["Barracks"][:1])*buildingWeights["Barracks"]
        chance["Chance"] += int(enemyBuildings["Bunker"][:1])*buildingWeights["Bunker"]
        chance["Chance"] += int(enemyBuildings["Starport"][:1])*buildingWeights["Starport"]
        chance["Chance"] += int(enemyBuildings["Armory"][:1])*buildingWeights["Armory"]
        chance["Chance"] += int(enemyBuildings["FusionCore"][:1])*buildingWeights["FusionCore"]
        chance["Chance"] += int(enemyBuildings["GA"][:1])*buildingWeights["GA"]
       
    if enemyRace == "zerg":
        chance["Chance"] += int(enemyBuildings["Hatchery"][:1])*buildingWeights["Hatchery"]
        chance["Chance"] += int(enemyBuildings["SP"][:1])*buildingWeights["SP"]
        chance["Chance"] += int(enemyBuildings["RW"][:1])*buildingWeights["RW"]
        chance["Chance"] += int(enemyBuildings["BN"][:1])*buildingWeights["BN"]
        chance["Chance"] += int(enemyBuildings["SpineCrawler"][:1])*buildingWeights["SpineCrawler"]
        chance["Chance"] += int(enemyBuildings["Lair"][:1])*buildingWeights["Lair"]
        chance["Chance"] += int(enemyBuildings["IP"][:1])*buildingWeights["IP"]
        chance["Chance"] += int(enemyBuildings["HD"][:1])*buildingWeights["HD"]
        chance["Chance"] += int(enemyBuildings["Spire"][:1])*buildingWeights["Spire"]
        chance["Chance"] += int(enemyBuildings["LurkerDen"][:1])*buildingWeights["LurkerDen"]
        chance["Chance"] += int(enemyBuildings["NydusWorm"][:1])*buildingWeights["NydusWorm"]
        chance["Chance"] += int(enemyBuildings["Hive"][:1])*buildingWeights["Hive"]
        chance["Chance"] += int(enemyBuildings["UC"][:1])*buildingWeights["UC"]
        chance["Chance"] += int(enemyBuildings["GS"][:1])*buildingWeights["GS"]
    
    
#Set chance matrix based off weights and quantity of each unit type.    
    if enemyRace == "protoss":
        chance["Chance"] += int(enemyUnits["Archon"][:1])*unitWeights["Archon"]
        chance["Chance"] += int(enemyUnits["Carrier"][:1])*unitWeights["Carrier"]
        chance["Chance"] += int(enemyUnits["Colossus"][:1])*unitWeights["Colossus"]
        chance["Chance"] += int(enemyUnits["DarkTemplar"][:1])*unitWeights["DarkTemplar"]
        chance["Chance"] += int(enemyUnits["HighTemplar"][:1])*unitWeights["HighTemplar"]
        chance["Chance"] += int(enemyUnits["Immortal"][:1])*unitWeights["Immortal"]
        chance["Chance"] += int(enemyUnits["Mothership"][:1])*unitWeights["Mothership"]
        chance["Chance"] += int(enemyUnits["Observer"][:1])*unitWeights["Observer"]
        chance["Chance"] += int(enemyUnits["Phoenix"][:1])*unitWeights["Phoenix"]
        chance["Chance"] += int(enemyUnits["Probe"][:1])*unitWeights["Probe"]
        chance["Chance"] += int(enemyUnits["Sentry"][:1])*unitWeights["Sentry"]
        chance["Chance"] += int(enemyUnits["Stalker"][:1])*unitWeights["Stalker"]
        chance["Chance"] += int(enemyUnits["VoidRay"][:1])*unitWeights["VoidRay"]
        chance["Chance"] += int(enemyUnits["WarpPrism"][:1])*unitWeights["WarpPrism"]
        chance["Chance"] += int(enemyUnits["Zealot"][:1])*unitWeights["Zealot"]
        chance["Chance"] += int(enemyUnits["Oracle"][:1])*unitWeights["Oracle"]
        chance["Chance"] += int(enemyUnits["Tempest"][:1])*unitWeights["Tempest"]
        chance["Chance"] += int(enemyUnits["MothershipCore"][:1])*unitWeights["MothershipCore"]
        chance["Chance"] += int(enemyUnits["Adept"][:1])*unitWeights["Adept"]
        chance["Chance"] += int(enemyUnits["Disruptor"][:1])*unitWeights["Disruptor"]
        
    
#Set mode chance as ints. 
    agressiveExpansion = int(chance["Chance"][:1])
    turtling = int(chance["Chance"][1:2])
    rush = int(chance["Chance"][2:3])
    straightToAir = int(chance["Chance"][3:4])
    groundAttack = int(chance["Chance"][4:5])
    
#Compare chance values. 
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




#coutnerEnemy function
def counterEnemy(biggestChance):
#agressiveExpansion    
    counter = ''
    if biggestChance == "agressiveExpansion":
        counter = "Harass"

#turtling    
    if biggestChance == "turtling":
        counter = "Expand"
        
#rush    
    if biggestChance == "rush":
        counter = "Defend"
        
#straightToAir        
    if biggestChance == "straightToAir":
        counter = "Rush"
        
#groundAttack    
    if biggestChance == "groundAttack":
        counter = "Expand & Harass"
       
    return counter




def actionToMovement(action, currentX, currentY, enemyBaseX, enemyBaseY, ourBaseX, ourBaseY):
    moveStep = 8
    
    enemyDirX = (enemyBaseX - ourBaseY)
    enemyDirY = (enemyBaseY - ourBaseY)
    
    enemyStartDistance = (enemyDirX*enemyDirX + enemyDirY*enemyDirY)**.5
    
    enemyDirX = enemyDirX/enemyStartDistance
    enemyDirY = enemyDirY/enemyStartDistance
    
    valid = True
    
    #S action
    if action == 1 or valid == False:
        newX = currentX
        newY = currentY
       
    #F action
    if action == 2:
        newX = currentX + enemyDirX*moveStep
        newY = currentY + enemyDirY*moveStep
        
    #B action
    if action == 3:
        newX = currentX - enemyDirX*moveStep
        newY = currentY - enemyDirY*moveStep
        
    #R action
    if action == 4:
        newX = currentX + enemyDirX*moveStep
        newY = currentY - enemyDirY*moveStep
        
    #L action
    if action == 5:
        newX = currentX - enemyDirX*moveStep
        newY = currentY + enemyDirY*moveStep
        
    #Invalid Action Check
    if newX > 64 or newX < 0 or newY > 64 or newY < 0:
        valid = False
   
    #S action
    if action == 1 or valid == False:
        newX = currentX
        newY = currentY
    
    return newX, newY





def getGameFeatures():
    a = pd.DataFrame(columns=['Nexus', 'Gateway', 'CC', 'StarGate', 'FleetBeacon', 'RoboticsFacility', 
                           'RoboticsBay', 'TwilightCouncil', 'TemplarArchives', 'DarkShrine', 'PC'])
    
    a.loc[1] = [rd.randint(0,4), rd.randint(0,4), rd.randint(0,4), rd.randint(0,4), rd.randint(0,4),
                 rd.randint(0,4), rd.randint(0,4), rd.randint(0,4), rd.randint(0,4), rd.randint(0,4), 
                 rd.randint(0,4)]
    
    return a[:1]


def NNSR(features):
    #stuff and things as a network to make less states
    state = features["Nexus"][:1]
    return state
    
    
    
