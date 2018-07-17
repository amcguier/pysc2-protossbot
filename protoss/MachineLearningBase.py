#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 14:41:22 2018

@author: EvanTroop

Sources : 
    https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
    https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_csv.html
    https://chrisalbon.com/python/data_wrangling/pandas_dataframe_importing_csv/
    https://stackoverflow.com/questions/4142151/how-to-import-the-class-within-the-same-directory-or-sub-directory
"""

#Machine Learning Main Class

import pandas as pd
import tensorflow as tf
import importlib as il




class MachineLearningBase() :
        

    def __init__(self):
        self.data_set = pd.read_csv('SCDataset1.csv')
        
        print("Initilized")
     
        
    def print_data(self):
        print(self.data_set)
   
    
    def get_row(self, from_row):
        if type(from_row) == int :
            return Row(self.data_set.loc[from_row]) 
        print("Error : Argument is not of correct Type")
        return False
    
    
    def set_data(self, row, export):
        temp = self.check_new_row(row)
        print("Set Data Called;")
        if temp == True : 
            print("PASSTHROUGH (set_data)")
            self.data_set = self.data_set.append(row, ignore_index = True)
            if export == True :
                self.export_data()
                self.print_data()
            return True
        return False
       
        
    def check_new_row(self, row):
        for c in self.data_set :
            temp2 = False
            for rh in row :
               if c == rh :
                   temp2 = True
            if temp2 == False:
                return False
            
        return True
    
    
    def export_data(self):
        self.data_set.to_csv("SCDataset1.csv", index = False)
        
    
        




print("---START---\n\n")
mach = MachineLearningBase()
mach.set_data({'x' : 40, 'z'  : 400}, False)
print(mach.get_row(0))
print("\n\n---END---")



