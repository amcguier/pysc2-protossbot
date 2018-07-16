#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 14:41:22 2018

@author: EvanTroop
"""

#Machine Learning Main Class

import pandas as pd
import tensorflow as tf

class MachineLearningBase() :
        

    def __init__(self):
        self.dataSet = pd.read_csv('SCDataset1.csv')
        print("Initilized")
     
        
    def printData(self):
        print(self.dataSet)
        
    def setData(self):
        print("Set Data Called;")
        self.dataSet = self.dataSet.append({'x' : 40, 'y'  : 400}, ignore_index = True)
        sure = input("Are you sure?(Y/N)\n")
        if('y' in sure):
            self.dataSet.to_csv('SCDataSet1.csv')
            self.dataSet = pd.read_csv('SCDataset1.csv')
        
        self.printData()
        
        


"""
mach = MachineLearningBase()
print("start\n\n")
mach.setData()

mmach2 = MachineLearningBase()
mach.printData()
print("\n\nend")
"""

data = pd.read_csv("SCDataset1.csv")

print(data)
data = data.append({'x' : 40, 'y'  : 400}, ignore_index = True)
print(data)
data.to_csv("SCDataset1.csv", index = False)
