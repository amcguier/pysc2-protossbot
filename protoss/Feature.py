#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 23:41:48 2018

@author: EvanTroop

sources : 
    https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html
    https://stackoverflow.com/questions/23549231/check-if-a-value-exists-in-pandas-dataframe-index
    
"""
#Individual Set of Data
import pandas as pd

class Feature:
    
    def __init__(self, d):
        if type(d) == pd.DataFrame :
            self.data = d
        else:
            print("Error : Argument is not of correct type")
            
        print("Initilized")
        
        
    #If the dataframe has a column that is called "for_key" returns value; else False
    def get_value(self, for_key):
        if for_key in self.data.columns :
            print("Through")
            return self.data[for_key]
        print("Error Accesing Data: Key not in data")
        return False
        
"""
feat = Feature( pd.DataFrame(data = {'x' : [86], 'y' : [3], 'z' : [4]} ))
print(feat.get_value('x') * 100)
print(feat.get_value('y') * 100)
print(feat.get_value('z') * 100)
"""