#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 15:47:13 2018

@author: EvanTroop

Sources : 
    https://stackoverflow.com/questions/22963263/creating-a-zero-filled-pandas-data-frame
    https://stackoverflow.com/questions/18692261/whats-a-simple-way-to-hard-code-a-6x6-numpy-matrix
    
    
"""

import pandas as pd
import tensorflow as tf
import numpy as np
import Feature as f
import MachineLearningDriver as mld
import random as rd

def generate_csv(name): 
    pre_q = pd.Dataframe()
    
class Qlist():
    
    def __init__(self, path, mode):
        #rows(index) = states
        #columns is actions
        
        #likleyhood that we try new spots
        if mode == "LEARNING" :
            self.epsilon = 0.85
        else : 
            self.epsilon = 0.0001
        
        self.q_list = pd.read_csv(path)
        print("Q-list generated from path : " + path)
        
    def get_max_action(self, state):
        if state in self.q_list.index :
            if rd.rand(0,1) > self.epsilon:
                return self.q_list.loc[state].idxmax()
            else :
                ind = rd.randint(0, len(self.q_list.columns))
                return self.q_list.loc[state][action]
        
        
    def set_reward(self, state, action):
        print()
        

zs = pd.DataFrame(0, index=['state1','state2','state3','state4'], columns=['action1','action2'])

#zs.loc[state][action] = 1
m = zs.loc['state1'].idxmax()
print('state2' in zs.index)
print()
print(zs.loc['state1']['action1'])
print()
print(zs)
print()
print(m)
    