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
import random as rd

def generate_csv(name, type_list='BASIC'): 
    if type_list == 'BASIC':
        state_list = []
        for p1 in range(1,6):
            for p2 in range(1,6):
                for p3 in range(1,6):
                    for p4 in range(1,6):
                        for p5 in range(1,6):
                            n = 10000*p1  +1000*p2 + 100*p3 + 10*p4 + p5
                            state_list.append(n)
                        
        action_list = [1,2,3,4,5]
    
        frame = pd.DataFrame(0,index=state_list, columns=action_list)
        frame.to_csv(name)
        print('CSV Created : ' + name)
        frame.describe()
        return True
    return False
   
    
scales = [[1,2,4,8,16], #Zealot
          [2,4,8,16,32], #Stalker
          [0,1,2,4,8], #Immortal
          [0,1,2,4,8], #Sentury
          [2700,5400,8100,13500,27000]] #Time


""" Returns an array of scaled values in the format[zealot, stalker, immortal, sentury, time] """
def get_scaled_value(typ, n_zealot=0, n_stalker=0, n_immortal=0, n_sentury= 0, time=0):
    if typ == 'SIMPLE':
        numbers = [n_zealot, n_stalker, n_immortal, n_sentury, time]
        outs = [0,0,0,0,0]
        for i in range(len(numbers)):
            print("scales:  " + str(scales[i]))
            for j in range(len(scales[i])):

                if scales[i][j] >= numbers[i]:

                    outs[i] = j + 1
                    break
            if(outs[i] == 0):
                outs[i] = 5
        print("OUTS : : :" + str(outs))
        state = 10000*outs[0] + 1000*outs[1] + 100*outs[2] + 10*outs[3] + outs[4]
        return state
        

""" Q_List Driver Class"""
class Q_list():
    states = [10]
    actions = [10]
    index = 0
    def __init__(self, path, mode='LEARNING'):
        #rows(index) = states
        #columns is actions
        self.path = path
        self.min_state = 11111
        self.max_state = 55555
        
        # will store past actions
        self.past_actions = pd.DataFrame(0,index=[0,1], columns=['state', 'action'])

        #a number if you want to limit how many future steps are counted, -1 if you want no endpoint
        self.recersive_units = 10
        #how much each step into the future retains value
        self.gamma = 0.8
       
        #likleyhood that we try new spots
        if mode == "LEARNING" :
            print("LEARNING")
            self.is_learning = True
            self.epsilon = 0.95
        else : 
            self.is_learning = False
            self.epsilon = 0.0001
        
        
        self.q_list = pd.read_csv(path, index_col=0)
        print("Q-list generated from path : " + path)

        
      
    
    
    """This will return the desired action accounting for Epsilon"""
    def get_max_action(self, state):
        
        if state >= self.min_state and state <= self.max_state:
            if rd.randint(0,100) > 100 * self.epsilon:
                return self.q_list.loc[state].idxmax()
            else :
                rand = rd.randint(1, 5)
                return rand
        
    
    
    """This will set the reward for a given state. won't do any calculations"""
    def set_reward(self, state, action, last_reward):
        print("action: " + str(action))
        
        if self.is_learning:
            
            st = self.past_actions.loc[1]['state']
            ac = self.past_actions.loc[1]['action']

            if st != 0:   
                print(str(st) + "    " + str(ac))
                current_val = self.q_list.loc[st][str(ac)]
                current_val = current_val + last_reward #* self.gamma 
                print("reward: " + str(last_reward))
                print("current_val: " + str(current_val))
                #current_val =+ 1
                print("state is: " + str(st))
                print("action is: " + str(ac))
                print("type is: " + str(type(st)))
                self.q_list.loc[st][str(ac)] = current_val

               
        if int(state) >= int(self.min_state) and int(state) <= int(self.max_state) and int(action) >= 1 and int(action) <= 5:
            
            last_s = st = self.past_actions.loc[1]['state']
            last_a = self.past_actions.loc[1]['action']
            
            self.past_actions.loc[0]['state'] = last_s
            self.past_actions.loc[0]['action'] = last_a
            
            self.past_actions.loc[1]['state'] = state
            self.past_actions.loc[1]['action'] = action

            
            return True

        return False
    
    
    def export_q_list(self):
        self.q_list.to_csv(self.path)
        print("Q-List was successfully exported to path : " + self.path)
        
        
    def end_of_game(self):
        self.export_q_list()
        print("End of Game Funcitons Complete")
    


#generate_csv("Army_Q.csv")
ql = Q_list('Army_Q.csv')
print(ql.q_list)
#print(ql.get_max_action(11111))
#ql.set_reward(11111, 2, 10)
#ql.set_reward(11112, 3, 10)
#ql.set_reward(11113, 3, 10)
print(get_scaled_value("SIMPLE", n_zealot=1, n_stalker=3, n_immortal=4, n_sentury= 6, time=100))
#print(ql.q_list)
#ql.set_reward(11114, 4, 10)
#print("HELLO")
#print(ql.get_max_action(11111))
#print("HHHsssHHH")
#print(len(ql.q_list.loc[11111]))