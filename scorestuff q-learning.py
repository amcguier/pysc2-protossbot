# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 10:49:07 2018

@author: makerspace-4
"""

import pandas as pd
import csv
import numpy as np
QScore = 0
ScoreStuff = obs.observation.score_cumulative
indices = ['score','idle_production_time','idle_worker_time','total_value_units','total_value_structures',
           'killed_value_units','killed_value_structures','collected_minerals',
           'collected_vespene','collection_rate_minerals','collection_rate_vespene',
           'spent_minerals','spent_vespene']

data = pd.DataFrame(columns=indices)
score = []
idlept = []
idlewt = []
totalvt = []
totalvs = []
killedvu = []
killedvs = []
collectedmins= []
collectedves =[]
collectionrtm = []
collectionrtv = []
spentmin = []
spentvesp = []
thinglist = [score,idlept,idlewt,totalvt,totalvs,killedvu,killedvs,collectedmins,
             collectedves,collectionrtm,collectionrtv,spentmin,spentvesp]
for i in range(len(thinglist)):
    thinglist[i].append(ScoreStuff[i])
    
QScore = (ScoreStuff[6])*4 + ScoreStuff[5] + 4000 # *win_true