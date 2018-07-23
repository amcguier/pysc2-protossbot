#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 22:53:59 2018

@author: EvanTroop

Sources : 
        Evan's Sources : 
            https://colab.research.google.com/drive/1HN7vgxBFfuZioyHiHTD5Noh2rNY_WbmH?authuser=2#scrollTo=2I8E2qhyKNd4
            
"""
import pandas as pd
import tensorflow as tf
import numpy as np


def main(type_of_learning, data, sel_features, target_output, ):
    """
    INFO
        type_of_learning
        
        data is a pandas data frame of all data that must be processed
        
        sel_features is a the an array of the headers of what should be sorted
        
        
    """
    
    
def get_required_features(data, sel_features):
    
    """
    INFO:
        data is a pandas data frame of all data that must be processed
        
        sel_features is a the an array of the headers of what should be sorted
        
        will return a copy of the data frame of selected features
    """
    if sel_features in data :
        print("Getting Features : contain successful")
        
        req_features = data[sel_features]
        return req_features.copy()
    
def prep_data():
    """
    INFO :
        p
    """
