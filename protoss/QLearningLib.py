#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 15:47:13 2018

@author: EvanTroop

Sources : 
    https://stackoverflow.com/questions/22963263/creating-a-zero-filled-pandas-data-frame
    https://stackoverflow.com/questions/18692261/whats-a-simple-way-to-hard-code-a-6x6-numpy-matrix
    https://stackoverflow.com/questions/16729574/how-to-get-a-value-from-a-cell-of-a-dataframe
    https://stackoverflow.com/questions/16729574/how-to-get-a-value-from-a-cell-of-a-dataframe
    https://stackoverflow.com/questions/10202570/pandas-dataframe-find-row-where-values-for-column-is-maximal
    https://stackoverflow.com/questions/13717554/weird-behaviour-initializing-a-numpy-array-of-string-data
    
    
"""

import pandas as pd
import tensorflow as tf
import numpy as np
import Feature as f
import MachineLearningDriver as mld
import random as rd

def generate_csv(name): 
    #pre_q = pd.Dataframe(
    #states = np.
    print()
    
class Q_list():
    
    def __init__(self, path, mode):
        #rows(index) = states
        #columns is actions
        
        #
        
        # will store past actions
        self.past_actions = pd.DataFrame(index=[], columns=['state', 'action'])
        
        #a number if you want to limit how many future steps are counted, -1 if you want no endpoint
        self.recersive_units = 10
        
        self.gamma = 0.8
        
        #likleyhood that we try new spots
        if mode == "LEARNING" :
            self.is_learning = True
            self.epsilon = 0.85
        else : 
            self.is_learning = False
            self.epsilon = 0.0001
        
        
        self.q_list = pd.read_csv(path)
        print("Q-list generated from path : " + path)
      
    """This will return the desired action accounting for Epsilon"""
    def get_max_action(self, state):
        if state in self.q_list.index :
            if rd.rand(0,1) > self.epsilon:
                return self.q_list.loc[state].idxmax()
            else :
                #need to do a random thing here
                si = np.rand.rand_int(0, high=10)
                
                return self.q_list.loc[state][action]
        
    """This will set the reward for a given state. won't do any calculations"""
    def set_reward(self, state, action, reward):
        if self.is_learning:
            for i in range(len(self.past_actions)):
                st = self.past_actions.loc[i]['state']
                ac = self.past_actions.loc[i]['action']
                
                current_val = self.q_list.loc[st][ac]
                current_val = current_val + reward * (self.gamma ** (len(self.past_actions) - i))
                print(current_val)
               
        if state in self.q_list.index and action in self.q_list.columns:
            self.q_list.loc[state][action] = reward
            return True
        
        return False
            
        

#zs = pd.DataFrame(0, index=['state1','state2','state3','state4'], columns=['action1','action2'])

#zs.loc[state][action] = 1

"""
m = zs.loc['state1'].idxmax()
print('state2' in zs.index)
print()
print(zs.loc['state1']['action1'])
print()
print(zs)
print()
print(m)
"""

past_actions = pd.DataFrame(index=[], columns=['action', 'state'])

past_actions = past_actions.append(pd.DataFrame.from_dict({'action' : ['hello1'], 'state':['hello1']}), ignore_index=True)
past_actions = past_actions.append(pd.DataFrame.from_dict({'action' : ['hello'], 'state':['hello1']}), ignore_index=True)

past_actions = past_actions.append(pd.DataFrame.from_dict({'action' : ['hello'], 'state':['hello1']}), ignore_index=True)
print(len(past_actions.loc[1]))
print(past_actions.loc[1][0])


si = np.random.randint(0, high=10)
print(si)
for i in range(len(past_actions)):
    print(past_actions.loc[i]['action'])
print(past_actions)
    