#TO-DO:
#Make method thingy manager for actions
#Fix priority and multi-tasking (e.g. once AI selects zealots for attack, continue building probes, pylons, etc.)





from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
from absl import app
import random
import csv
import pandas as pd
import numpy as np
import math
#Main class
class ProtossAgent(base_agent.BaseAgent):
    truzealots = 0
    truimmortals = 0
    trustalkers = 0
    trusentries = 0
    truprobes = 0
    pb = 0
    trunumunits = {truzealots,trustalkers,trusentries,truimmortals,truprobes}
    t = 0
    #doc = open("StarCraft_data", "w")
    xc = 10 #changed from 10
    yc = 8
    infodump = ''
    x = 70
    y = 40
    n = 10000000
    #Initializes variables ??????
    def __init__(self):
        super(ProtossAgent, self).__init__()
    
        self.attack_coordinates = None
    
    #Utility method, will check if first unit in selected group is of the correct unit type
    def unit_type_is_selected(self, obs, unit_type):
        if (len(obs.observation.single_select) > 0 and
                obs.observation.single_select[0].unit_type == unit_type):
            return True
        
        if (len(obs.observation.multi_select) > 0 and
                obs.observation.multi_select[0].unit_type == unit_type):
            return True
        
        return False
    
    #????????
    def get_units_by_type(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units
                        if unit.unit_type == unit_type]
    
    #See if unit can execute action
    def can_do(self, obs, action):
        return action in obs.observation.available_actions
    
    
    #Decision making section, returns an action at the end of each step of the game
    #Prioritized actions go at the top
    def step(self, obs):
        super(ProtossAgent, self).step(obs)
        
        #If first step of the game
        if obs.first():
            return actions.FUNCTIONS.move_camera((48, 48))
            #Find locations of units and average them, use average to determine if top left or bottom right
            player_y, player_x = (obs.observation.feature_minimap.player_relative ==
                                  features.PlayerRelative.SELF).nonzero()
            xmean = player_x.mean()
            ymean = player_y.mean()
            
            if xmean <= 31 and ymean <= 31:
                self.attack_coordinates = (49, 49)
                self.infodump = self.infodump + 'top left\n'
                self.pb = 1
            else:
                self.attack_coordinates = (12, 16)   
                self.infodump = self.infodump + 'bottom right\n'
                #bottom right
        #Attack with zealots
        
        
        self.t +=1
        
        
        
        zealots = self.get_units_by_type(obs, units.Protoss.Zealot)
        #print(type(zealots))
        '''
        if len(zealots) >= 5:
            if self.unit_type_is_selected(obs, units.Protoss.Zealot):
                if self.can_do(obs, actions.FUNCTIONS.Attack_minimap.id):
                        return actions.FUNCTIONS.Attack_minimap("now",
                                                                self.attack_coordinates)
        
        #Select zealots
        if len(zealots) > 0:
            if self.can_do(obs, actions.FUNCTIONS.select_army.id):
                return actions.FUNCTIONS.select_army("select")
                
                '''
        
        
        #Build pylons if free supply less than 10 and not capped at 200
        #PROBLEM: Once AI selects zealots for attack, it no longer has probes selected and can't run this; also building zealots takes priority
        #xn= self.x
        #yn = self.y
        
        
        #### enemy units shit
        '''
        print (obs.observation)
        _PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
        _PLAYER_HOSTILE = 4
        hot_squares = np.zeros(16)        
        enemy_y, enemy_x = (obs.observation['minimap'][_PLAYER_RELATIVE] == _PLAYER_HOSTILE).nonzero()
        for i in range(0, len(enemy_y)):
            y = int(math.ceil((enemy_y[i] + 1) / 16))
            x = int(math.ceil((enemy_x[i] + 1) / 16))
            
            hot_squares[((y - 1) * 4) + (x - 1)] = 1
        '''
        
        probes = self.get_units_by_type(obs, units.Protoss.Probe)
        ###########print(len(probes)) 
        
        '''
        if self.unit_type_is_selected(obs, units.Protoss.Probe):
            free_supply = (obs.observation.player.food_cap -
                           obs.observation.player.food_used)
            if free_supply < 10 and obs.observation.player.food_cap != 200:
                if self.can_do(obs, actions.FUNCTIONS.Build_Pylon_screen.id) and self.t%64 == self.pb:
                    x = random.randint(0, 20) #changed from 83
                    y = random.randint(0, 20)
                    return actions.FUNCTIONS.Build_Pylon_screen("now", (x, y))
                    
        '''            
        '''
        if self.unit_type_is_selected(obs, units.Protoss.Probe):
            free_supply = (obs.observation.player.food_cap -
                                         obs.observation.player.food_used)
            
            
            if self.x < 78 and self.y < 78:
                self.n -= 1
                
                #yn += 5
                if self.can_do(obs, actions.FUNCTIONS.Build_Pylon_screen.id):
                    
                    
                    
                    #self.y = 45
                    #x = random.randint(0, 83)
                    #y = random.randint(0, 83)
                    #x = 20
                    #y = 30
                    #xn += 5
                    #yn += 5
                    
                    return actions.FUNCTIONS.Build_Pylon_screen("now", (self.x, self.y))
                if self.can_do(obs, actions.FUNCTIONS.Build_Pylon_screen.id):
                    self.y += 5
        pylons = self.get_units_by_type(obs, units.Protoss.Pylon)
             
        #doc = open("StarCraft_data1", "w")
        lp1 = len(pylons)
        #self.n -=1
        lp2 = 0 
        '''
        '''
        if lp2 != lp1:
            print(pylons)
            lp2 = lp1
            print(lp1)
            print(lp2)
            '''
        '''
        self.t +=1
        if self.t%2 == 0:                #changed from tick of 15
            print(pylons)
            self.infodump = self.infodump+ 'top left\n\n' + 'x = ' + str(self.x) + 'y = ' + str(self.y) + '\n\n'
            if len(pylons) > 0:
                self.infodump = self.infodump +  str(pylons[0])

        if self.t%100== 0: #changed from 150
            #with open("StarCraft_data1", "a") as doc
            print('lililililillilililililililililililililililililililililliliilililililillilililililililililililililililililililililliliilililililillilililililililililililililililililililililliliilililililillilililililililililililililililililililililliliilililililillililililililililililililililililililililillilii')
            doc = open("StarCraft_data1", "a")
            doc.write('\n\n\n')
            doc.write(self.infodump)
            doc.close()
       
        '''
        '''
        zealots = self.get_units_by_type(obs, units.Protoss.Zealot)
        stalkers = self.get_units_by_type(obs, units.Protoss.Stalker)
        sentries = self.get_units_by_type(obs, units.Protoss.Sentry)
        observers = self.get_units_by_type(obs, units.Protoss.Observer)
        immortals = self.get_units_by_type(obs, units.Protoss.Immortal)
        templars = self.get_units_by_type(obs, units.Protoss.HighTemplar)
        '''
        #need to make an incrementeing class variable
        if self.t%12 ==0 :#and self.t%64 != self.pb
            zealots = self.get_units_by_type(obs, units.Protoss.Zealot)
            stalkers = self.get_units_by_type(obs, units.Protoss.Stalker)
            sentries = self.get_units_by_type(obs, units.Protoss.Sentry)
            observers = self.get_units_by_type(obs, units.Protoss.Observer)
            immortals = self.get_units_by_type(obs, units.Protoss.Immortal)
            templars = self.get_units_by_type(obs, units.Protoss.HighTemplar)
            probes = self.get_units_by_type(obs, units.Protoss.Probe)
            numUnits = {len(zealots),len(stalkers),len(sentries),len(immortals)}
            
            
            if self.xc <56:
                self.truzealots += len(zealots)
                self.trustalkers += len(stalkers)
                self.trusentries += len(sentries)
                self.truimmortals += len(immortals)
                self.truprobes += len(probes)
                self.trunumunits = {self.truzealots,self.trustalkers,self.trusentries,self.truimmortals,self.truprobes}
                print(len(probes))
                print(self.truprobes)
                print(self.trunumunits)
                if self.yc < 56:
                    self.yc += 12
                    return actions.FUNCTIONS.move_camera((self.xc, self.yc))
                else:
                    self.xc +=16
                    self.yc = 8
            else:
                self.xc = 10
                self.yc = 8
                self.truzealots += len(zealots)
                self.trustalkers += len(stalkers)
                self.trusentries += len(sentries)
                self.truimmortals += len(immortals)
                self.truprobes += len(probes)
                print(self.trunumunits)
                self.truzealots = 0
                self.trustalkers = 0
                self.trusentries = 0
                self.truimmortals = 0
                self.truprobes = 0
            
            
            
        '''
            for i in range(10, 58, 16):
                for j in range(8, 56, 16):
                    zealots = self.get_units_by_type(obs, units.Protoss.Zealot)
                    stalkers = self.get_units_by_type(obs, units.Protoss.Stalker)
                    sentries = self.get_units_by_type(obs, units.Protoss.Sentry)
                    observers = self.get_units_by_type(obs, units.Protoss.Observer)
                    immortals = self.get_units_by_type(obs, units.Protoss.Immortal)
                    templars = self.get_units_by_type(obs, units.Protoss.HighTemplar)
                    numUnits = {len(zealots),len(stalkers),len(sentries),len(immortals)}
                    print(numUnits)
                    return actions.FUNCTIONS.move_camera((i, j))
        '''    
        
        #minimapcamera = obs.observation.feature_minimap.camera
        #print(minimapcamera)
        #csvfile = 'SCtest1.csv'
        #with open(csvfile, "w") as output:
        #    writer = csv.writer(output,lineterminator='')
        #    writer.writerows(minimapcamera)
        #Build gateways
        
        gateways = self.get_units_by_type(obs, units.Protoss.Gateway)
        '''
        if len(gateways) < 1:
            if self.unit_type_is_selected(obs, units.Protoss.Probe):
                if self.can_do(obs, actions.FUNCTIONS.Build_Gateway_screen.id) and self.t%64 == self.pb:
                    x = random.randint(0, 20)  #CHANGED from 83
                    y = random.randint(0, 20)
                    
                    return actions.FUNCTIONS.Build_Gateway_screen("now", (x, y))
        
        #Train zealots if gateway selected
        if self.unit_type_is_selected(obs, units.Protoss.Gateway):
            if self.can_do(obs, actions.FUNCTIONS.Train_Zealot_quick.id):
                return actions.FUNCTIONS.Train_Zealot_quick("now")
        '''    
        #zealots = self.get_units_by_type(obs, units.Protoss.Zealot) 
        print(self.t)
        if self.t%100 == 0:                #changed from tick of 15
            #print(zealots)
            #self.infodump = self.infodump+ 
            if len(zealots) > 0:
                self.infodump = self.infodump +  str(zealots) + '\n\n\n'
        
        if self.t%250== 0: #changed from 150
            #with open("StarCraft_data1", "a") as doc
            print('lililililillilililililililililililililililililililililliliilililililillilililililililililililililililililililililliliilililililillilililililililililililililililililililililliliilililililillilililililililililililililililililililililliliilililililillililililililililililililililililililililillilii')
            doc = open("StarCraft_data1_zealots", "a")
            doc.write('\n\n\n\n\n')
            doc.write(self.infodump)
            doc.close()
            '''
            csvfile = 'test.csv'
            ScoreShit = obs.observation.score_cumulative
            print(ScoreShit)
#Assuming res is a flat list
            indices = ['idle_production_time','idle_worker_time','total_value_units','total_value_structures',
                       'killed_value_units','killed_value_structures','collected_minerals',
                       'collected_vespene','collection_rate_minerals','collection_rate_vespene',
                       'spent_minerals','spent_vespene']
            csvlist = []
            dict1 = {}
            for thing in ScoreShit:
                csvlist.append(thing)
            data = []
            alldata = []
            for val in ScoreShit:
                data.append(val)
            for x in range(len(indices)):
                    datarow = []
                    datarow.append(indices[x])
                    datarow.append(data[x])
                    alldata.append(datarow)    
            with open(csvfile, "w") as output:
                
                writer = csv.writer(output, lineterminator='\n')
                writer.writerows(alldata)
            '''
            ScoreShit = obs.observation.score_cumulative
            indices = ['score','idle_production_time','idle_worker_time','total_value_units','total_value_structures',
                       'killed_value_units','killed_value_structures','collected_minerals',
                       'collected_vespene','collection_rate_minerals','collection_rate_vespene',
                       'spent_minerals','spent_vespene']
            #ScoreShit = [354,2345,356,3456,346,567,4567,4567,47,235,345,356,456]
            data = pd.DataFrame(columns=indices)
            score = []
            idlept = []
            idlewt = []
            totalvt = []
            totalvs = []
            killedvu = []
            killedvs = []
            collectedmins= []
            collectedves =[]
            collectionrtm = []
            collectionrtv = []
            spentmin = []
            spentvesp = []
            thinglist = [score,idlept,idlewt,totalvt,totalvs,killedvu,killedvs,collectedmins,
                         collectedves,collectionrtm,collectionrtv,spentmin,spentvesp]
            for i in range(len(thinglist)):
                thinglist[i].append(ScoreShit[i])

            '''
            infile = 'a.csv'
            colnames = ['angle', 'wave','trans','refl']
            df1 = pd.read_csv(infile,sep='\s+', header = None,skiprows = 0,
                      comment='#',names=colnames,usecols=(0,1,2,3))
            df2 = pd.read_csv(infile,sep='\s+', header = None,skiprows = 0,
                              comment='#',names=colnames,usecols=(0,1))
                              result = pd.merge(df1,df2,on='wave')
            '''         
            ###### NOTICE: the commented part you have to run the first time then recomment it after the first time
            ######         because it formats the csv file, you should comment out the bottom part when you run the code for
            ######         the first time
            '''
            new_d = data.append(pd.Series(thinglist, index=indices),ignore_index=True)



            data = data.append(new_d, ignore_index=True)

            print(data)
            #data.to_csv("SCtest.csv",mode = 'a', index = False)
            data.to_csv("SCtest.csv",mode = 'w', index = False)
            '''
            
            
            ###run this part second to infinite times
            
            '''
            csvfile = 'SCtest.csv'
            with open(csvfile, "a") as output:
                writer = csv.writer(output,lineterminator=',')
                writer.writerows(thinglist)
            
            '''    
                
                
                
            '''
            indices = ['score','idle_production_time','idle_worker_time','total_value_units','total_value_structures',
                       'killed_value_units','killed_value_structures','collected_minerals',
                       'collected_vespene','collection_rate_minerals','collection_rate_vespene',
                       'spent_minerals','spent_vespene']
            
            data = pd.DataFrame(columns=indices)
            print(data)
            new_d = pd.DataFrame({'score' : [0],'idle_production_time': [0],'idle_worker_time' : [0],'total_value_units' : [0],'total_value_structures' : [0],
                       'killed_value_units':[0],'killed_value_structures':[0],'collected_minerals':[0],
                       'collected_vespene':[0],'collection_rate_minerals':[0],'collection_rate_vespene':[0],
                       'spent_minerals':[0],'spent_vespene':[0]})
            print(new_d)
            data.append(new_d, ignore_index=False)
            print(data)
            '''
            """
            ScoreShit = obs.observation.score_cumulative
            indices = ['score','idle_production_time','idle_worker_time','total_value_units','total_value_structures',
                       'killed_value_units','killed_value_structures','collected_minerals',
                       'collected_vespene','collection_rate_minerals','collection_rate_vespene',
                       'spent_minerals','spent_vespene']            
            data = []
            #alldata = []
            for val in ScoreShit:
                data.append(val)
            print(data)
            df = pd.DataFrame(data, columns=indices)
            print(df)
             """   
            '''
                for val in ScoreShit and key in indices:
                    d
                    writer.writerow([val]) 
                '''
                
                    
                    
                    
#Which produce
        #Look for gateways
        if len(gateways) > 0:
            gateway = random.choice(gateways)
            
            return actions.FUNCTIONS.select_point("select_all_type", (gateway.x,
                                                                      gateway.y))
            
            
      
        #Looking for probes and adding them to the array
        probes = [unit for unit in obs.observation.feature_units
              if unit.unit_type == units.Protoss.Probe]
        
        #If probes exist, select all probes
        if len(probes) > 0:
            probe = random.choice(probes)
      
            return actions.FUNCTIONS.select_point("select_all_type", (probe.x,
                                                                probe.y))
      
        return actions.FUNCTIONS.no_op()
        
        

def main(unused_argv):
    agent = ProtossAgent()
    try:
        while True:
            with sc2_env.SC2Env(
                    
                    #Map selection
                    map_name="Simple64",
                    
                    #Players, first argument is OUR bot
                    players=[sc2_env.Agent(sc2_env.Race.protoss),
                             
                             #Enemy bot configuration, can be another agent
                                     sc2_env.Bot(sc2_env.Race.random,
                                                             sc2_env.Difficulty.very_easy)],
                    
                    #Define map and minimap size that bot will use to see terrain and features
                    #Can add RGB-Dimensions?
                    agent_interface_format=features.AgentInterfaceFormat(
                            feature_dimensions=features.Dimensions(screen=96, minimap=64),
                            
                            #Use feature units
                            use_feature_units=True),
                            
                    #Number of steps that will pass before bot makes an action
                    step_mul=16,
                    
                    #Game length = unlimited
                    game_steps_per_episode=0,
                    
                    #Interface for us
                    visualize=True) as env:
                
                #Looping technicalities and stuff
                agent.setup(env.observation_spec(), env.action_spec())
                
                timesteps = env.reset()
                agent.reset()
                
                while True:
                    step_actions = [agent.step(timesteps[0])]
                    if timesteps[0].last():
                        break
                    timesteps = env.step(step_actions)
            
    except KeyboardInterrupt:
        pass
    
if __name__ == "__main__":
    app.run(main)