#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 14:41:22 2018

@author: EvanTroop

Sources : 
    Evan's Sources : 
        https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
        https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_csv.html
        https://chrisalbon.com/python/data_wrangling/pandas_dataframe_importing_csv/
        https://stackoverflow.com/questions/4142151/how-to-import-the-class-within-the-same-directory-or-sub-directory
        https://stackoverflow.com/questions/17839973/construct-pandas-dataframe-from-values-in-variables
        https://stackoverflow.com/questions/19482970/get-list-from-pandas-dataframe-column-headers

"""

#Machine Learning Main Class

import pandas as pd
import tensorflow as tf
import Feature as f




class MachineLearningBase() :
        

    def __init__(self):
        self.data_set = pd.read_csv('SCDataset1.csv')
        
        print("Initilized")
     
        
    def print_data(self):
        print(self.data_set)
   
    #gets a row from the data (individual row) : dataType = 
    def get_row(self, from_row):
        if type(from_row) == int:
            return pd.DataFrame(self.data_set.loc[[from_row]])
        print("Error : Argument is not of correct Type 0001")
        return False
    
    #get all data from a single feature : dataType = 
    def get_feature(self, feature_name):
        if type(feature_name) == str :
            return self.data_set[feature_name]
        print("Error : Argument is not of correct Type 0002")
        return False
        
    #append to the datase; if export is true => commit changes made to dataset to the csv file
    def append(self, row_1, export):
        
        if type(row_1) == f.Row:
            row = row_1.get_data()
            if self.check_new_row(row): 
                self.data_set = self.data_set.append(row, ignore_index = True)
                if export == True :
                    self.export_data()
                    self.print_data()
                    return True
        return False
        
    #Checks to make sure that the row we want to add matches the fromat of our
    #data set
    def check_new_row(self, row):
        
        for key in list(row.columns.values):
            if key not in list(self.data_set.columns.values):
                print("Error : Row to add contains feature not in data_set")
                return
          
        
        row_headers = list(row.columns.values)
        row_types = list(row.dtypes)
        data_types = self.data_set.dtypes
            
        temp2 = True
        for i in range(len(row_headers)):
            if data_types[row_headers[i]] != row_types[i]:
                print("Error : Data types do not match")
                temp2 = False
                
        
        return temp2
        
        
            
   
    
    
    def export_data(self):
        self.data_set.to_csv("SCDataset1.csv", index = False)
        
    
        




print("---START---\n\n")
mach = MachineLearningBase()

d = pd.DataFrame(data = {'x' : [100], 'y' : [500]})
print(mach.append(f.Row(d), False))


print("\n\n---END---")



