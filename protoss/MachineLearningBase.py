#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 14:41:22 2018

@author: EvanTroop

Sources : 
    https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
    https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_csv.html
    https://chrisalbon.com/python/data_wrangling/pandas_dataframe_importing_csv/
    
"""

#Machine Learning Main Class

import pandas as pd
import tensorflow as tf

class MachineLearningBase() :
        

    def __init__(self):
        self.data_set = pd.read_csv('SCDataset1.csv')
        
        print("Initilized")
     
        
    def print_data(self):
        print(self.data_set)
        
    def set_data(self, export):
        print("Set Data Called;")
        self.data_set = self.data_set.append({'x' : 40, 'y'  : 400}, ignore_index = True)
        if export == True :
            self.export_data()
        self.print_data()
        
        
    def export_data(self):
        self.data_set.to_csv("SCDataset1.csv", index = False)
        
    
        




print("start\n\n")
mach = MachineLearningBase()
mach.set_data(True)
print("\n\nend")



