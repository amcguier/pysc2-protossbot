#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 23:41:48 2018

@author: EvanTroop

sources : 
    https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html
    https://stackoverflow.com/questions/23549231/check-if-a-value-exists-in-pandas-dataframe-index
    https://stackoverflow.com/questions/17071871/select-rows-from-a-dataframe-based-on-values-in-a-column-in-pandas
"""

#Individual Set of Data
import pandas as pd

class Row:
    
    def __init__(self, d):
        if type(d) == pd.DataFrame :
            self.data = d
        else :
            print("Error : Argument is not of correct type")
        self.get_description(False)
        print("Initilized")
        
        
    #If the dataframe has a column that is called "for_key" returns value; else False
    def get_value(self, for_key):
        if for_key in self.data.columns :
            return self.data[for_key]
        print("Error Accesing Data: Key not in data")
        return False
    
    #Check to make sure data contains key and if so set to value, return true; else , return false
    def set_value(self, value, for_key):
        if for_key in self.data.columns :
            self.data[for_key] = value
            print("Error : Key to set data for is not in data")
            return True
        return False
    
    #get all of the data as a panda dataframe
    def get_data(self):
        return self.data
    
    #easily print all values in the row 
    #argument = true : w index, false : w/o index
    def get_description(self, with_index):
        if(with_index == True):
            print(self.data)
        else:
            for c in self.data :
                s = str(c) + " : "
                for v in self.data[c]:
                    s += str(v) + ", "
                print(s)
        
"""
feat = Row( pd.DataFrame(data = {'x' : [86], 'y' : [3], 'z' : [4]} ))
print(feat.get_value('x') * 100)
print(feat.get_value('y') * 100)
print(feat.get_value('z') * 100)
"""