# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 23:29:04 2018

@author: makerspace-4
"""

import pandas as pd
import csv
import numpy as np
            ScoreShit = obs.observation.score_cumulative
            indices = ['score','idle_production_time','idle_worker_time','total_value_units','total_value_structures',
                       'killed_value_units','killed_value_structures','collected_minerals',
                       'collected_vespene','collection_rate_minerals','collection_rate_vespene',
                       'spent_minerals','spent_vespene']
            #ScoreShit = [354,2345,356,3456,346,567,4567,4567,47,235,345,356,456]
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
                thinglist[i].append(ScoreShit[i])
                            ###### NOTICE: the commented part you have to run the first time then recomment it after the first time
            ######         because it formats the csv file, you should comment out the bottom part when you run the code for
            ######         the first time
            '''
            new_d = data.append(pd.Series(thinglist, index=indices),ignore_index=True)



            data = data.append(new_d, ignore_index=True)

            print(data)
            #data.to_csv("SCtest.csv",mode = 'a', index = False)
            data.to_csv("SCtest.csv",mode = 'w', index = False)
            '''
            
            
            ###run this part second to infinite times
            csvfile = 'SCtest.csv'
            with open(csvfile, "a") as output:
                writer = csv.writer(output,lineterminator=',')
                writer.writerows(thinglist)