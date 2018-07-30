"""
Main Author of all PYSC2 Related Code:   Frederick Qiu
Neural Network Optimizer (not in file):  Evan Troop
Machine Learning Input and Organization: John Zhuang, Benjamin Chen, Amir Saman Naseri

Received much help from Steven Brown in the form of discord and basic tutorials:
https://itnext.io/build-a-zerg-bot-with-pysc2-2-0-2self.SCREEN_DIM - 1375d2f58e
https://itnext.io/how-to-locate-and-select-units-in-pysc2-2bb1c81f2ad3
"""

from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
from absl import app
import random, math, csv, numpy, pdb
from sklearn.cluster import KMeans
import QLearningLib as ql
import FunctionListTest1 as flt

"""


INIT OF THE CLASS


"""
class ProtossAgent(base_agent.BaseAgent):

"""

Nesc Class variables
======================================
"""
    truzealots = 0
    truimmortals = 0
    trustalkers = 0
    trusentries = 0
    truprobes = 0
    
    trunumunits = [truzealots,trustalkers,trusentries,truimmortals,truprobes,t]
    finalNumUnits = []    
    xc = 10 #changed from 10
    yc = 9
    
    
    
    real_old_score = 0
    old_score = 0
    
    
    
    SCREEN_DIM = 96
    MINIMAP_DIM = 64
    ARMY_ATTACK_THRESHOLD = 25
    
    ARMY_RATIO = {
            "Zealot": 4,
            "Stalker": 8,
            "Sentry": 4,
            "Observer": 1,
            "Immortal": 4,
            "Templar": 4,
            "Total": 25
            }
    
    ARMY_COMPOSITION = [units.Protoss.Zealot, units.Protoss.Stalker, units.Protoss.Sentry, units.Protoss.Observer, units.Protoss.Immortal, units.Protoss.HighTemplar]
    
    Q_List = ql.Q_List('Army_Q.csv', 'LEARNING')
    
    attack_number = 0
    step_number = 0
    action_number = 1
    sub_action_number = 0
    number_of_bases = 1
    camera_location = 0
    time_until_nexus = 2000
    time_until_warpgates = 2400
    time_supply_needed = 250
    time_shield_up = 300
    time_chronoboost_effective = 0
    time_attempting_construction = 0
    number_of_facilities = 0
    supply_needed = True
    build_forward_pylon = True
    stop_worker_production = False
    minerals_filled = False
    possible_enemy_base_destroyed = False
    main_enemy_base_destroyed = False
    army_selected = False
    researching_warpgates = False
    attempting_construction = False
    
    resource_locations = []
    main_base_camera = [0, 0] #*****
    natural_base_camera = [0, 0]
    army_rally_camera = [0, 0]
    main_enemy_base = [0, 0] #*******
    possible_enemy_base = [0, 0]
    nexus_location = [0, 0]
    build_lean = [0, 0]
    first_pylon_location = [0, 0]
    
    geysers = []
    
    #These are for samans function
    truzealots = 0
    truimmortals = 0
    trustalkers = 0
    trusentries = 0
    truprobes = 0

    trunumunits = {truzealots,trustalkers,trusentries,truimmortals,truprobes,t}
    
    xc = 10 #changed from 10
    yc = 9
    
    
"""
========================================
"""

    def actionToMovement(action, currentX, currentY, enemyBaseX, enemyBaseY, ourBaseX, ourBaseY):
        moveStep = 8
        enemyDirX = (enemyBaseX - ourBaseY)
        enemyDirY = (enemyBaseY - ourBaseY)
        enemyStartDistance = (enemyDirX*enemyDirX + enemyDirY*enemyDirY)**.5
        enemyDirX = enemyDirX/enemyStartDistance
        enemyDirY = enemyDirY/enemyStartDistance
        valid = True
        #S action
        if action == 1 or valid == False:
            newX = currentX
            newY = currentY
        #F action
        if action == 2:
            newX = currentX + enemyDirX*moveStep
            newY = currentY + enemyDirY*moveStep
        #B action
        if action == 3:
            newX = currentX - enemyDirX*moveStep
            newY = currentY - enemyDirY*moveStep
        #R action
        if action == 4:
            newX = currentX + enemyDirX*moveStep
            newY = currentY - enemyDirY*moveStep
        #L action
        if action == 5:
            newX = currentX - enemyDirX*moveStep
            newY = currentY + enemyDirY*moveStep
        #Invalid Action Check
        if newX >= 64 or newX < 0 or newY >= 64 or newY < 0:
            valid = False
        if valid:
            return newX, newY
        else:
            return currentX, currentY
    
   
    #Initializes variables
    def __init__(self):
        super(ProtossAgent, self).__init__()
    
   
    #Checks if selected unit is of the correct type
    def unit_type_is_selected(self, obs, unit_type):
        if (len(obs.observation.single_select) > 0 and
                obs.observation.single_select[0].unit_type == unit_type):
            return True
        if (len(obs.observation.multi_select) > 0 and
                obs.observation.multi_select[0].unit_type == unit_type):
            return True
        return False
    
    def Find_Units(self,obs,time): # time has to be greater than 8, its what mod you want
        if self.sub_action_number%time ==0 or self.sub_action_number%time ==1 or 
        self.sub_action_number%time ==2 or self.sub_action_number%time ==3 or 
        self.sub_action_number%time == 4 or self.sub_action_number%time ==5
        or self.sub_action_number%time ==6 or self.sub_action_number%time ==7
        or self.sub_action_number%time ==8:
            
            
        # time however many steps you want it to run
            zealots = self.get_units_by_type(obs, units.Protoss.Zealot)
            stalkers = self.get_units_by_type(obs, units.Protoss.Stalker)
            sentries = self.get_units_by_type(obs, units.Protoss.Sentry)
            observers = self.get_units_by_type(obs, units.Protoss.Observer)
            immortals = self.get_units_by_type(obs, units.Protoss.Immortal)
            templars = self.get_units_by_type(obs, units.Protoss.HighTemplar)
            probes = self.get_units_by_type(obs, units.Protoss.Probe)
            numUnits = {len(zealots),len(stalkers),len(sentries),len(immortals)}
    
    
            if self.xc <54:
                self.truzealots += len(zealots)
                self.trustalkers += len(stalkers)
                self.trusentries += len(sentries)
                self.truimmortals += len(immortals)
                self.truprobes += len(probes)
                self.trunumunits = [self.truzealots,self.trustalkers,self.trusentries,self.truimmortals,self.truprobes,self.t]
            #print(len(probes))
            #print(self.truprobes)
            #print(self.trunumunits)
                if self.yc < 54:
                    self.yc += 16
                    return actions.FUNCTIONS.move_camera((self.xc, self.yc))
                else:
                    self.xc +=18
                    self.yc = 9
            else:
                self.xc = 10
                self.yc = 9 
                self.truzealots += len(zealots)
                self.trustalkers += len(stalkers)
                self.trusentries += len(sentries)
                self.truimmortals += len(immortals)
                self.truprobes += len(probes)
            #print(self.trunumunits)# get rid of the print statement
                finalNumUnits = [self.truzealots,self.trustalkers,self.trusentries,self.truimmortals,self.truprobes,self.sub_action_number]
                self.truzealots = 0
                self.trustalkers = 0
                self.trusentries = 0
                self.truimmortals = 0
                self.truprobes = 0
    
    
    #Adds all units of the same type on screen to an array
    def get_units_by_type(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units
                        if unit.unit_type == unit_type]
    
    
    #Checks if selected unit can execute an action
    def can_do(self, obs, action):
        return action in obs.observation.available_actions
    
    
    #Generates a random location on the screen
    def random_location(self):
        return [random.randint(0, self.SCREEN_DIM - 1), random.randint(0, 71)]
    
    
    #Find the distance between 2 points
    def get_distance(self, x1, y1, x2, y2):
        return math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
    
    
    
   
    #Calculate the affinity generated by effects
    def get_effect_affinity(self, obs, control_group):
        effect_affinity = numpy.zeros((24, 24), dtype = "int")
        all_effects = obs.observation.feature_screen.effects
        value = 15
        for i in range(int(round(self.SCREEN_DIM/4))):
            for j in range(int(round(self.SCREEN_DIM/4))):
                if all_effects[4*i + 1][4*j + 1] == 1 or all_effects[4*i + 1][4*j + 1] == 11:
                    effect_affinity[i, j]+=(value*4)
                elif all_effects[4*i + 1][4*j + 1] == 10:
                    effect_affinity[i, j]-=(value*2)
                elif all_effects[4*i + 1][4*j + 1] == 2:
                    effect_affinity[i, j]+=(value*1)
        return effect_affinity
        
    
    #Calculate the affinity generated by a specific unit for a location
    def get_unit_affinity(self, obs, control_group, x, y):
        affinity = 0
        all_units = obs.observation.feature_units
        for i in range(len(all_units)):
            ###########SOME_FUNCTION#########(control_group, all_units[i])
            distance = self.get_distance(x, y, all_units[i].x, all_units[i].y)
            if all_units[i].alliance == 4:
                value = 5
                if control_group == 2 or control_group == 5:
                    affinity+=(value * (1 / (1 + (distance/4 - 7)**2) - 1 / (1 + math.exp(distance - 24))))
                elif control_group == 1:
                    affinity+=(value * (1 / (1 + (distance/4 - 5)**2) - 1 / (1 + math.exp(distance - 16))))
                elif control_group == 4:
                    affinity+=(value * (1 / (1 + (distance/4 - 3)**2) - 1 / (1 + math.exp(distance - 8))))
            elif all_units[i].alliance == 1:
                value = 1
                if control_group == 3:
                    affinity+=(value * (10 / (distance + 1)))
        return affinity
    
    
    #Calculate the affinities for moves and return the highest affinity
    def get_optimal_move(self, obs, control_group, x, y):
        location = [48, 48]
        highest_affinity = -1000
        effect_affinity = self.get_effect_affinity(obs, control_group)
        x = min(max(int(round(x)), 0), 95)
        y = min(max(int(round(y)), 0), 95)
        for i in range(int(round(self.SCREEN_DIM/4))):
            for j in range(int(round(self.SCREEN_DIM/4))):
                distance = self.get_distance(x, y, 4*i + 1, 4*j + 1)
                if abs(obs.observation.feature_screen.height_map[i][j] - obs.observation.feature_screen.height_map[x][y]) < 5:
                    affinity = (self.get_unit_affinity(obs, control_group, 4*i + 1, 4*j + 1) + effect_affinity[i, j]) / (1 + math.exp(distance/4 - 8))
                    if affinity > highest_affinity:
                        highest_affinity = affinity
                        location = [i, j]
        print(highest_affinity)
        return location
        
    
    #Get score differential
    def get_score(self, obs):
        self.real_old_score = self.old_score
        self.old_score = 4*obs.observation.score_cumulative.killed_value_structures + obs.observation.score_cumulative.killed_value_units
        return (4*obs.observation.score_cumulative.killed_value_structures + obs.observation.score_cumulative.killed_value_units - self.real_old_score)
        
    
    #Returns an action to the game at the end of every step
    def step(self, obs):
        super(ProtossAgent, self).step(obs)
        
        #Use K-Means clustering to find center of masses of the various resource clusters
        if obs.first():
            resources_y, resources_x = (obs.observation.feature_minimap.player_relative == features.PlayerRelative.NEUTRAL).nonzero()
            number_of_clusters = int(math.ceil(len(resources_y) / 16))
            resources = []
            for i in range(0, len(resources_y)):
                resources.append((resources_x[i], resources_y[i]))
            kmeans = KMeans(n_clusters = number_of_clusters)
            kmeans.fit(resources)
            for i in range(number_of_clusters):
                self.resource_locations.append((kmeans.cluster_centers_[i][0], kmeans.cluster_centers_[i][1]))
            for i in range(number_of_clusters):
                if self.resource_locations[i][0] < self.MINIMAP_DIM / 2:
                    if self.resource_locations[i][1] < self.MINIMAP_DIM / 2:
                        self.resource_locations[i] = (int(round(self.resource_locations[i][0])) + 3, int(round(self.resource_locations[i][1])) + 3)
                    else:
                        self.resource_locations[i] = (int(round(self.resource_locations[i][0])) + 3, int(round(self.resource_locations[i][1])) - 3)
                else:
                    if self.resource_locations[i][1] < self.MINIMAP_DIM / 2:
                        self.resource_locations[i] = (int(round(self.resource_locations[i][0])) - 3, int(round(self.resource_locations[i][1])) + 3)
                    else:
                        self.resource_locations[i] = (int(round(self.resource_locations[i][0])) - 3, int(round(self.resource_locations[i][1])) - 3)
                    
            #ONLY FOR SIMPLE64 MAP
            player_y, player_x = (obs.observation.feature_minimap.player_relative == features.PlayerRelative.SELF).nonzero()
            xmean = player_x.mean()
            ymean = player_y.mean()
            if xmean < self.MINIMAP_DIM / 2:
                self.build_lean[0] = -1
            else:
                self.build_lean[0] = 1
            if ymean < self.MINIMAP_DIM / 2:
                self.build_lean[1] = -1
            else:
                self.build_lean[1] = 1
            for i in range(number_of_clusters):
                if abs(self.resource_locations[i][1] - ymean) < 10:
                    if abs(self.resource_locations[i][0] - xmean) < 10:
                        self.main_base_camera[0] = self.resource_locations[i][0] - self.build_lean[0]
                        self.main_base_camera[1] = self.resource_locations[i][1] + self.build_lean[1]
                    else:
                        self.natural_base_camera[0] = self.resource_locations[i][0] - self.build_lean[0]
                        self.natural_base_camera[1] = self.resource_locations[i][1] + self.build_lean[1]
                        self.army_rally_camera[0] = self.resource_locations[i][0] + 2*self.build_lean[0]
                        self.army_rally_camera[1] = self.resource_locations[i][1] - 4*self.build_lean[1]
                else:
                    if abs(self.resource_locations[i][0] - xmean) > 10:
                        self.main_enemy_base = self.resource_locations[i]
                    else:
                        self.possible_enemy_base = self.resource_locations[i]
        
        
        
        
        
        
        
        nexi = self.get_units_by_type(obs, units.Protoss.Nexus)
        if len(nexi) == 1:
            nexus = nexi[0]
        
        probes = self.get_units_by_type(obs, units.Protoss.Probe)
        minerals = self.get_units_by_type(obs, units.Neutral.MineralField)
        assimilators = self.get_units_by_type(obs, units.Protoss.Assimilator)
        pylons = self.get_units_by_type(obs, units.Protoss.Pylon)
        
        gateways = self.get_units_by_type(obs, units.Protoss.Gateway)
        warpgates = self.get_units_by_type(obs, units.Protoss.WarpGate)
        facilities = self.get_units_by_type(obs, units.Protoss.RoboticsFacility)
        
        forges = self.get_units_by_type(obs, units.Protoss.Forge)
        cores = self.get_units_by_type(obs, units.Protoss.CyberneticsCore)
        councils = self.get_units_by_type(obs, units.Protoss.TwilightCouncil)
        archives = self.get_units_by_type(obs, units.Protoss.TemplarArchive)
        
        zealots = self.get_units_by_type(obs, units.Protoss.Zealot)
        stalkers = self.get_units_by_type(obs, units.Protoss.Stalker)
        sentries = self.get_units_by_type(obs, units.Protoss.Sentry)
        observers = self.get_units_by_type(obs, units.Protoss.Observer)
        immortals = self.get_units_by_type(obs, units.Protoss.Immortal)
        templars = self.get_units_by_type(obs, units.Protoss.HighTemplar)
        
        scrap_metals = [zealots, stalkers, sentries, observers, immortals, templars]
        
        
        
        
        
        
        self.step_number+=1
        self.sub_action_number+=1
        self.time_shield_up+=1
        self.time_chronoboost_effective+=1
        if self.number_of_bases == 2 and self.time_until_nexus > 0:
            self.time_until_nexus-=1
        if self.researching_warpgates and self.time_until_warpgates > 0:
            self.time_until_warpgates-=1
        if self.supply_needed == False:
            self.time_supply_needed = 0
        else:
            self.time_supply_needed+=1
        if self.attempting_construction:
            self.time_attempting_construction+=1
            if self.time_attempting_construction > 250:
                self.attempting_construction = False
                self.time_attempting_construction = 0
        
        obs.observation.score_cumulative.total_value_units - obs.observation.score_cumulative.killed_value_units
        
        
        """if self.sub_action_number < 10:
            return actions.FUNCTIONS.move_camera((self.main_base_camera[0] - 8*self.build_lean[0], self.main_base_camera[1]))
        
        self.res = obs.observation.feature_screen.height_map
        
        csvfile = "height_map_sample.csv"
        
        #Assuming res is a flat list
        with open(csvfile, "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            for val in self.res:
                writer.writerow([val])    
        
        #Assuming res is a list of lists
        with open(csvfile, "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(self.res)
            print("nice")
        
        exit()"""
        
        
        
        print(str(self.action_number) + " " + str(self.sub_action_number))###################################
        
        #Center camera on and select the main base, rally probes to correct resources, train probes
        if self.action_number == 1:
            
            if self.sub_action_number == 2:
                self.camera_location = 0
                return actions.FUNCTIONS.move_camera(self.main_base_camera)
            
            if self.sub_action_number == 4:
                if len(self.geysers) == 0:
                    self.geysers = self.get_units_by_type(obs, units.Neutral.VespeneGeyser)
                if self.number_of_bases == 1 and len(nexi) > 0:
                    self.nexus_location[0] = nexus.x
                    self.nexus_location[1] = nexus.y
                if len(nexi) > 0:
                    if self.nexus_location[0] >= 0 and self.nexus_location[0] <= self.SCREEN_DIM - 1 and self.nexus_location[1] >= 0 and self.nexus_location[1] <= self.SCREEN_DIM - 1:
                        return actions.FUNCTIONS.select_point("select", self.nexus_location)
            
            if self.sub_action_number == 5:
                if self.unit_type_is_selected(obs, units.Protoss.Nexus):
                    if obs.observation.control_groups[9][1] == 0:
                        return actions.FUNCTIONS.select_control_group("append", 9)
                    if nexus.assigned_harvesters < nexus.ideal_harvesters and len(minerals) > 0:
                        return actions.FUNCTIONS.Rally_Workers_screen("now", (minerals[0].x, minerals[0].y))
                    for i in range(len(assimilators)):
                        if assimilators[i].assigned_harvesters < assimilators[i].ideal_harvesters and assimilators[i].ideal_harvesters != 0:
                            return actions.FUNCTIONS.Rally_Workers_screen("now", (assimilators[i].x, assimilators[i].y))
                    if self.number_of_bases == 1 or self.minerals_filled:
                        if self.can_do(obs, actions.FUNCTIONS.Cancel_Last_quick.id):
                            return actions.FUNCTIONS.Cancel_Last_quick("now")
                            
            if self.sub_action_number == 6:
                if self.number_of_bases == 1:
                    self.sub_action_number = 0
                    self.action_number = 2
                if self.unit_type_is_selected(obs, units.Protoss.Nexus):
                    if self.minerals_filled == False:
                        if len(obs.observation.build_queue) <= 1:
                            if self.can_do(obs, actions.FUNCTIONS.Train_Probe_quick.id):
                                return actions.FUNCTIONS.Train_Probe_quick("now")
                    
            if self.sub_action_number == 8:
                if self.number_of_bases > 1:
                    self.camera_location = 1
                    return actions.FUNCTIONS.move_camera(self.natural_base_camera)
            
            if self.sub_action_number == 10:
                self.sub_action_number = 0
                self.action_number = 2
                if self.unit_type_is_selected(obs, units.Protoss.Nexus):
                    if len(minerals) > 0:
                        return actions.FUNCTIONS.Rally_Workers_screen("now", (minerals[0].x, minerals[0].y))
                
                
        #Select CG8 (or bind worker to CG8) and center camera on main base, build assimilators and pylons at main base, build pylons by natural expansion if necessary
        if self.action_number == 2:
            
            if self.sub_action_number == 1:
                if obs.observation.control_groups[8][1] == 0:
                    self.sub_action_number-=1
                    if self.unit_type_is_selected(obs, units.Protoss.Probe):
                        return actions.FUNCTIONS.select_control_group("set", 8)
                    elif len(probes) > 0:
                        return actions.FUNCTIONS.select_point("select", (probes[0].x, probes[0].y))
                else:
                    return actions.FUNCTIONS.select_control_group("recall", 8)
            
            if self.sub_action_number == 3:
                self.camera_location = 0
                return actions.FUNCTIONS.move_camera(self.main_base_camera)
                                    
            if self.sub_action_number == 5:
                if len(pylons) > 0 and len(assimilators) < len(self.geysers):
                    if self.unit_type_is_selected(obs, units.Protoss.Probe):
                        if self.can_do(obs, actions.FUNCTIONS.Build_Assimilator_screen.id):
                            return actions.FUNCTIONS.Build_Assimilator_screen("queued", (self.geysers[len(assimilators)].x, self.geysers[len(assimilators)].y))
            
            if self.sub_action_number == 7:
                if self.unit_type_is_selected(obs, units.Protoss.Probe):
                    if obs.observation.player.food_cap - obs.observation.player.food_used < 20 and obs.observation.player.food_cap != 200:
                        self.supply_needed = True
                        if self.time_supply_needed > 250:
                            if self.can_do(obs, actions.FUNCTIONS.Build_Pylon_screen.id):
                                self.supply_needed = False
                                if len(pylons) == 0:
                                    unit_type = obs.observation["feature_screen"][features.SCREEN_FEATURES.unit_type.index]
                                    mineral_y, mineral_x = (unit_type == units.Neutral.MineralField).nonzero()
                                    x = 2*nexus.x - int(round(mineral_x.mean())) - 5*self.build_lean[0]
                                    y = 2*nexus.y - int(round(mineral_y.mean())) - 5*self.build_lean[1]
                                    self.first_pylon_location[0] = x
                                    self.first_pylon_location[1] = y
                                    return actions.FUNCTIONS.Build_Pylon_screen("queued", self.first_pylon_location)
                                elif len(pylons) == 1 and len(gateways) > 0:
                                    return actions.FUNCTIONS.Build_Pylon_screen("queued", (self.first_pylon_location[0] + self.build_lean[0]*35, self.first_pylon_location[1]))
                                elif len(pylons) == 2:
                                    return actions.FUNCTIONS.Build_Pylon_screen("queued", (self.first_pylon_location[0], self.first_pylon_location[1] + self.build_lean[1]*35))
                                elif len(pylons) == 3:
                                    if self.build_forward_pylon:
                                        self.camera_location = 2
                                        return actions.FUNCTIONS.move_camera(self.army_rally_camera)
                                    else:
                                        self.camera_location = 1
                                        return actions.FUNCTIONS.move_camera(self.natural_base_camera)
                                    
            if self.sub_action_number == 9:
                self.sub_action_number = 0
                if self.time_until_nexus == 0:
                    self.action_number = 3
                elif obs.observation.player.minerals > 550 and self.number_of_bases == 1:
                    self.action_number = 11
                else:
                    self.action_number = 4
                    
                if self.can_do(obs, actions.FUNCTIONS.Build_Pylon_screen.id):
                    if self.build_forward_pylon and self.camera_location == 2:
                        self.build_forward_pylon = False
                        return actions.FUNCTIONS.Build_Pylon_screen("queued", (48 - 8*self.build_lean[0], 48 + 8*self.build_lean[1]))
                    if self.camera_location == 1:    
                        if random.randint(0, 1) == 0:
                            if self.build_lean[0] == -1:
                                return actions.FUNCTIONS.Build_Pylon_screen("queued", (random.randint(0, 32), random.randint(0, 71)))
                            else:
                                return actions.FUNCTIONS.Build_Pylon_screen("queued", (random.randint(63, self.SCREEN_DIM - 1), random.randint(0, 71)))
                        else:
                            if self.build_lean[1] == -1:
                                return actions.FUNCTIONS.Build_Pylon_screen("queued", (random.randint(0, self.SCREEN_DIM - 1), random.randint(63, 71)))
                            else:
                                return actions.FUNCTIONS.Build_Pylon_screen("queued", (random.randint(0, self.SCREEN_DIM - 1), random.randint(0, 32)))
                
                
        #Center camera on natural expansion, rally probes to correct resources, train probes
        if self.action_number == 3:
            
            if self.sub_action_number == 2:
                self.camera_location = 1
                return actions.FUNCTIONS.move_camera(self.natural_base_camera)
            
            if self.sub_action_number == 4:
                return actions.FUNCTIONS.select_point("select", (48, 48))
                
            if self.sub_action_number == 5:
                if self.unit_type_is_selected(obs, units.Protoss.Nexus):
                    if obs.observation.control_groups[9][1] == 1:
                        return actions.FUNCTIONS.select_control_group("append", 9)
                    if nexus.assigned_harvesters < nexus.ideal_harvesters:
                        return actions.FUNCTIONS.Rally_Workers_screen("now", (minerals[0].x, minerals[0].y))
                    else:
                        self.minerals_filled = True
                    for i in range(len(assimilators)):
                        if assimilators[i].assigned_harvesters < assimilators[i].ideal_harvesters and assimilators[i].ideal_harvesters != 0:
                            return actions.FUNCTIONS.Rally_Workers_screen("now", (assimilators[i].x, assimilators[i].y))
                    if self.can_do(obs, actions.FUNCTIONS.Cancel_Last_quick.id):
                        self.stop_worker_production = True
                        return actions.FUNCTIONS.Cancel_Last_quick("now")
                            
            if self.sub_action_number == 6:
                self.sub_action_number = 0
                self.action_number = 4
                if self.unit_type_is_selected(obs, units.Protoss.Nexus):
                    if self.stop_worker_production == False:
                        if len(obs.observation.build_queue) <= 1:
                            if self.can_do(obs, actions.FUNCTIONS.Train_Probe_quick.id):
                                return actions.FUNCTIONS.Train_Probe_quick("now")
                            
        
        #Select all nexi and chronoboost
        if self.action_number == 4:
            
            if self.sub_action_number == 1:
                return actions.FUNCTIONS.select_control_group("recall", 9)
            
            if self.sub_action_number == 3:
                self.camera_location = 0
                return actions.FUNCTIONS.move_camera(self.main_base_camera)
            
            if self.sub_action_number == 5:
                self.sub_action_number = 0
                self.action_number = 5
                if self.unit_type_is_selected(obs, units.Protoss.Nexus):
                    if self.can_do(obs, actions.FUNCTIONS.Effect_ChronoBoostEnergyCost_screen.id):
                        if self.time_chronoboost_effective > 450:
                            self.time_chronoboost_effective = 0
                            if len(cores) > 0 and self.time_until_warpgates > 0:
                                return actions.FUNCTIONS.Effect_ChronoBoostEnergyCost_screen("now", (cores[0].x, cores[0].y))
                            elif len(facilities) > 0:
                                return actions.FUNCTIONS.Effect_ChronoBoostEnergyCost_screen("now", (facilities[0].x, facilities[0].y))
                        
                        
        #Center camera on main base and construct combat buildings
        if self.action_number == 5:
            
            if self.sub_action_number == 1:
                return actions.FUNCTIONS.select_control_group("recall", 8)
            
            if self.sub_action_number == 3:
                self.camera_location = 0
                return actions.FUNCTIONS.move_camera(self.main_base_camera)
            
            if self.sub_action_number == 5:
                self.sub_action_number = 0
                if len(cores) > 0 and self.researching_warpgates == False:
                    self.action_number = 12
                else:
                    self.action_number = 6
                if self.unit_type_is_selected(obs, units.Protoss.Probe):    
                    if len(gateways) + len(warpgates) < 1:
                        if self.can_do(obs, actions.FUNCTIONS.Build_Gateway_screen.id):
                            return actions.FUNCTIONS.Build_Gateway_screen("queued", self.random_location())
                    elif len(cores) < 1 and self.attempting_construction == False:
                        if self.can_do(obs, actions.FUNCTIONS.Build_CyberneticsCore_screen.id):
                            self.attempting_construction = True
                            return actions.FUNCTIONS.Build_CyberneticsCore_screen("queued", self.random_location())
                    elif len(gateways) + len(warpgates) < 2:
                        if self.can_do(obs, actions.FUNCTIONS.Build_Gateway_screen.id):
                            return actions.FUNCTIONS.Build_Gateway_screen("queued", self.random_location())
                    elif len(forges) < 1:
                        if self.can_do(obs, actions.FUNCTIONS.Build_Forge_screen.id):
                            return actions.FUNCTIONS.Build_Forge_screen("queued", self.random_location())
                    elif self.number_of_bases > 1:
                        if len(facilities) < 1:
                            if self.can_do(obs, actions.FUNCTIONS.Build_RoboticsFacility_screen.id):
                                return actions.FUNCTIONS.Build_RoboticsFacility_screen("queued", self.random_location())
                        elif len(councils) < 1:
                            if self.can_do(obs, actions.FUNCTIONS.Build_TwilightCouncil_screen.id):
                                return actions.FUNCTIONS.Build_TwilightCouncil_screen("queued", self.random_location())
                        elif len(gateways) + len(warpgates) < 3:
                            if self.can_do(obs, actions.FUNCTIONS.Build_Gateway_screen.id):
                                return actions.FUNCTIONS.Build_Gateway_screen("queued", self.random_location())
                        elif len(archives) < 1:
                            if self.can_do(obs, actions.FUNCTIONS.Build_TemplarArchive_screen.id):
                                return actions.FUNCTIONS.Build_TemplarArchive_screen("queued", self.random_location())
                        elif len(facilities) < 2:
                            if self.can_do(obs, actions.FUNCTIONS.Build_RoboticsFacility_screen.id):
                                return actions.FUNCTIONS.Build_RoboticsFacility_screen("queued", self.random_location())
                        elif len(forges) < 2:
                            if self.can_do(obs, actions.FUNCTIONS.Build_Forge_screen.id):
                                return actions.FUNCTIONS.Build_Forge_screen("queued", self.random_location())
                        elif len(gateways) + len(warpgates) < 4:
                            if self.can_do(obs, actions.FUNCTIONS.Build_Gateway_screen.id):
                                return actions.FUNCTIONS.Build_Gateway_screen("queued", self.random_location())
                        elif len(facilities) < 3:
                            if self.can_do(obs, actions.FUNCTIONS.Build_RoboticsFacility_screen.id):
                                return actions.FUNCTIONS.Build_RoboticsFacility_screen("queued", self.random_location())
                            
        
        #Research upgrades from forge
        if self.action_number == 6:
            
            if self.sub_action_number == 2:
                self.camera_location = 0
                return actions.FUNCTIONS.move_camera(self.main_base_camera)
                
            if self.sub_action_number == 4:
                if len(forges) > 0:
                    forge = random.choice(forges)
                    if forge.x >= 0 and forge.x < self.SCREEN_DIM and forge.y >= 0 and forge.y < self.SCREEN_DIM:
                        return actions.FUNCTIONS.select_point("select", (forge.x, forge.y))
                    
            if self.sub_action_number == 5:
                self.sub_action_number = 0
                self.action_number = 7
                if self.unit_type_is_selected(obs, units.Protoss.Forge):
                    if len(obs.observation.build_queue) == 0:
                        if self.can_do(obs, actions.FUNCTIONS.Research_ProtossGroundWeapons_quick.id):
                            return actions.FUNCTIONS.Research_ProtossGroundWeapons_quick("now")
                        elif self.can_do(obs, actions.FUNCTIONS.Research_ProtossGroundArmor_quick.id):
                            return actions.FUNCTIONS.Research_ProtossGroundArmor_quick("now")
                        elif self.can_do(obs, actions.FUNCTIONS.Research_ProtossShields_quick.id):
                            return actions.FUNCTIONS.Research_ProtossShields_quick("now")
                        
                    
        #Train units from gateway/warpgate
        
        if self.action_number == 7:
            
            self.number_of_facilities = len(facilities)
            if len(gateways) > 0 or self.sub_action_number > 6:
                
                if self.sub_action_number == 2:
                    self.camera_location = 0
                    return actions.FUNCTIONS.move_camera(self.main_base_camera)
                
                if self.sub_action_number == 4:
                    self.number_of_facilities = len(facilities)
                    gateway = random.choice(gateways)
                    if gateway.x >= 0 and gateway.x < self.SCREEN_DIM and gateway.y >= 0 and gateway.y < self.SCREEN_DIM:
                        return actions.FUNCTIONS.select_point("select", (gateway.x, gateway.y))
                
                if self.sub_action_number == 6:
                    if self.unit_type_is_selected(obs, units.Protoss.Gateway):
                        print(self.time_until_warpgates)
                        print(len(gateways))
                        if self.time_until_warpgates == 0:
                            if self.can_do(obs, actions.FUNCTIONS.Morph_WarpGate_quick.id):
                                self.sub_action_number = 0
                                return actions.FUNCTIONS.Morph_WarpGate_quick("now")
                            elif self.can_do(obs, actions.FUNCTIONS.Cancel_Last_quick.id):
                                self.sub_action_number-=1
                                return actions.FUNCTIONS.Cancel_Last_quick("now")
                        else:
                            self.camera_location = 2
                            return actions.FUNCTIONS.move_camera(self.army_rally_camera)
                
                if self.sub_action_number == 8:
                    if self.unit_type_is_selected(obs, units.Protoss.Gateway):
                        return actions.FUNCTIONS.Rally_Units_screen("now", (48, 48 - 16*self.build_lean[1]))
                
                if self.sub_action_number == 9:
                    self.sub_action_number = 0
                    if self.number_of_facilities > 0:
                        self.action_number = 8
                    else:
                        self.action_number = 9
                    if self.unit_type_is_selected(obs, units.Protoss.Gateway):
                        if len(obs.observation.build_queue) < 2:
                            if len(stalkers) / (obs.observation.player.army_count + 1) < self.ARMY_RATIO["Stalker"] / self.ARMY_RATIO["Total"]:
                                if self.can_do(obs, actions.FUNCTIONS.Train_Stalker_quick.id):
                                    return actions.FUNCTIONS.Train_Stalker_quick("now")
                            if len(sentries) / (obs.observation.player.army_count + 1) < self.ARMY_RATIO["Sentry"] / self.ARMY_RATIO["Total"]:
                                if self.can_do(obs, actions.FUNCTIONS.Train_Sentry_quick.id):
                                    return actions.FUNCTIONS.Train_Sentry_quick("now")
                            if len(templars) / (obs.observation.player.army_count + 1) < self.ARMY_RATIO["Templar"] / self.ARMY_RATIO["Total"]:
                                if self.can_do(obs, actions.FUNCTIONS.Train_HighTemplar_quick.id):
                                    return actions.FUNCTIONS.Train_HighTemplar_quick("now")
                            if self.can_do(obs, actions.FUNCTIONS.Train_Zealot_quick.id):
                                return actions.FUNCTIONS.Train_Zealot_quick("now")
                        
            elif len(warpgates) > 0 or self.sub_action_number > 3:
                if self.sub_action_number == 1:
                    return actions.FUNCTIONS.select_warp_gates("select")
                
                if self.sub_action_number == 3:
                    self.camera_location = 2
                    return actions.FUNCTIONS.move_camera(self.army_rally_camera)
                
                if self.sub_action_number == 5:
                    self.sub_action_number = 0
                    if self.number_of_facilities > 0:
                        self.action_number = 8
                    else:
                        self.action_number = 9
                    if self.unit_type_is_selected(obs, units.Protoss.WarpGate):
                        if len(stalkers) / (obs.observation.player.army_count + 1) < self.ARMY_RATIO["Stalker"] / self.ARMY_RATIO["Total"]:
                            if self.can_do(obs, actions.FUNCTIONS.TrainWarp_Stalker_screen.id):
                                return actions.FUNCTIONS.TrainWarp_Stalker_screen("now", (48, 48 + 8*self.build_lean[1]))
                        if len(sentries) / (obs.observation.player.army_count + 1) < self.ARMY_RATIO["Sentry"] / self.ARMY_RATIO["Total"]:
                            if self.can_do(obs, actions.FUNCTIONS.TrainWarp_Sentry_screen.id):
                                return actions.FUNCTIONS.TrainWarp_Sentry_screen("now", (48, 48 + 8*self.build_lean[1]))
                        if len(templars) / (obs.observation.player.army_count + 1) < self.ARMY_RATIO["Templar"] / self.ARMY_RATIO["Total"]:
                            if self.can_do(obs, actions.FUNCTIONS.TrainWarp_HighTemplar_screen.id):
                                return actions.FUNCTIONS.TrainWarp_HighTemplar_screen("now", (48, 48 + 8*self.build_lean[1]))
                        if self.can_do(obs, actions.FUNCTIONS.TrainWarp_Zealot_screen.id):
                            return actions.FUNCTIONS.TrainWarp_Zealot_screen("now", (48, 48 + 8*self.build_lean[1]))
                        
            else:
                self.sub_action_number = 0
                if self.number_of_facilities > 0:
                    self.action_number = 8
                else:
                    self.action_number = 9
                        
        #Train units from robotics facility
        if self.action_number == 8:
            
            if self.sub_action_number == 2:
                self.camera_location = 0
                return actions.FUNCTIONS.move_camera(self.main_base_camera)
                            
            if self.sub_action_number == 4:
                if len(facilities) > 0:
                    facility = random.choice(facilities)
                    if facility.x >= 0 and facility.x <= self.SCREEN_DIM - 1 and facility.y >= 0 and facility.y <= self.SCREEN_DIM - 1:
                        return actions.FUNCTIONS.select_point("select", (facility.x, facility.y))
            
            if self.sub_action_number == 6:
                if self.unit_type_is_selected(obs, units.Protoss.RoboticsFacility):
                    self.camera_location = 2
                    return actions.FUNCTIONS.move_camera(self.army_rally_camera)
            
            if self.sub_action_number == 8:
                if self.unit_type_is_selected(obs, units.Protoss.RoboticsFacility):
                    return actions.FUNCTIONS.Rally_Units_screen("now", (48, 48 - 16*self.build_lean[1]))
                
            if self.sub_action_number == 9:
                self.sub_action_number = 0
                if obs.observation.player.army_count > 0:
                    self.action_number = 9
                else:
                    self.action_number = 1
                if self.unit_type_is_selected(obs, units.Protoss.RoboticsFacility):
                    if len(obs.observation.build_queue) < 2:
                        if len(observers) / (obs.observation.player.army_count + 1) < self.ARMY_RATIO["Observer"] / self.ARMY_RATIO["Total"]:
                            if self.can_do(obs, actions.FUNCTIONS.Train_Observer_quick.id):
                                return actions.FUNCTIONS.Train_Observer_quick("now")
                        if self.can_do(obs, actions.FUNCTIONS.Train_Immortal_quick.id):
                            return actions.FUNCTIONS.Train_Immortal_quick("now")
                            
        
        #Select and add units to control groups
        if self.action_number == 9:
            
            if self.sub_action_number == 2:
                if obs.observation.player.army_count > 0:
                    self.camera_location = 2
                    return actions.FUNCTIONS.move_camera(self.army_rally_camera)
                
            if self.sub_action_number == 4:
                if obs.observation.control_groups[0][1] < self.ARMY_ATTACK_THRESHOLD:
                    if self.can_do(obs, actions.FUNCTIONS.select_army.id):
                        self.army_selected = True
                        return actions.FUNCTIONS.select_army("select")
                
            if self.sub_action_number == 5:
                if self.army_selected:
                    self.army_selected = False
                    return actions.FUNCTIONS.select_control_group("set", 0)
                
            if self.sub_action_number % 2 == 0 and self.sub_action_number >= 6:
                x = int(round((self.sub_action_number - 4) / 2))
                if len(scrap_metals[x]) > 0:
                    scrap_metal = random.choice(scrap_metals[x])
                    if scrap_metal.x >= 0 and scrap_metal.x < self.SCREEN_DIM and scrap_metal.y >= 0 and scrap_metal.y < self.SCREEN_DIM:
                        return actions.FUNCTIONS.select_point("select_all_type", (scrap_metal.x, scrap_metal.y))
            
            if self.sub_action_number % 2 == 1 and self.sub_action_number >= 7:
                x = int(round((self.sub_action_number - 5) / 2))
                if self.sub_action_number == 15:
                    self.sub_action_number = 0
                    self.action_number = 10
                if self.unit_type_is_selected(obs, self.ARMY_COMPOSITION[x]):
                    return actions.FUNCTIONS.select_control_group("set", x)
                
            
        #Send army to rekt enemy ezzzzzzzz
        if self.action_number == 10:
            self.attack_number+=1
            zealots = self.get_units_by_type(obs, units.Protoss.Zealot)
            stalkers = self.get_units_by_type(obs, units.Protoss.Stalker)
            sentries = self.get_units_by_type(obs, units.Protoss.Sentry)
            observers = self.get_units_by_type(obs, units.Protoss.Observer)
            immortals = self.get_units_by_type(obs, units.Protoss.Immortal)
            templars = self.get_units_by_type(obs, units.Protoss.HighTemplar)
            probes = self.get_units_by_type(obs, units.Protoss.Probe)
            if self.attack_number % 2 == 0:
                last_reward = self.get_score(obs)
                
                if self.sub_action_number% 3 == 1:
                    self.yc = 22
                elif self.sub_action_number% 3 == 2:
                    self.yc = 38
                else:
                    self.yc = 6
                if math.floor((self.sub_action_number - 1) / 3) == 0:
                    self.xc = 10
                elif math.floor((self.sub_action_number - 1) / 3) == 1:
                    self.xc = 28
                else:
                    self.xc = 45
            self.truzealots += len(zealots)
            self.trustalkers += len(stalkers)
            self.trusentries += len(sentries)
            self.truimmortals += len(immortals)
            self.truprobes += len(probes)
            
            self.trunumunits = [self.truzealots, self.trustalkers, self.trusentries,self.truimmortals,self.truprobes,self.step_number]
            self.truzealots = 0
            self.trustalkers = 0
            self.trusentries = 0
            self.truimmortals = 0
            self.truprobes = 0
            return actions.FUNCTIONS.move_camera((self.xc, self.yc))
            ##### REMEBER TO DO SOMETHING WITH self.trunumunits  BEFORE YOU PAN THE SCREEN AGAIN                
            if self.sub_action_number % 4:
                
                state = ql.get_scaled_value('SIMPLE', n_zealot=trunumunits[0], 
                                            n_stalker=trunumunits[1], 
                                            n_immortal=trunumunits[2],
                                            n_sentury=trunumunits[3],
                                            time=trunumunits[4])
                last_reward = self.get_score(obs)
                
                action = self.Q_List.get_max_action(state)
                self.Q_List.set_reward(state, action, last_reward)
                
                
                new_x, new_y = actionToMovement(action, )
                
                
            """
            if self.sub_action_number == 1:
                return actions.FUNCTIONS.select_control_group("recall", 0)
            
            if self.sub_action_number == 3:
                pixels_y, pixels_x = (obs.observation.feature_minimap.selected == features.PlayerRelative.SELF).nonzero()
                pixels = []
                for i in range(0, len(pixels_y)):
                    pixels.append((pixels_x[i], pixels_y[i]))
                kmeans = KMeans(n_clusters = 1)
                if len(pixels) > 0:
                    kmeans.fit(pixels)
                    self.camera_location = 3
                    return actions.FUNCTIONS.move_camera(kmeans.cluster_centers_[0])
            
            if self.sub_action_number == 5:
                pixels_y, pixels_x = (obs.observation.feature_minimap.selected == features.PlayerRelative.SELF).nonzero()
                pixels = []
                for i in range(0, len(pixels_y)):
                    pixels.append((pixels_x[i], pixels_y[i]))
                kmeans = KMeans(n_clusters = 1)
                if len(pixels) > 0:
                    kmeans.fit(pixels)
                    micromanage = False
                    for i in range(len(obs.observation.feature_units)):
                        if obs.observation.feature_units[i].alliance == 4 and obs.observation.feature_units[i].unit_type != units.Zerg.ChangelingZealot:
                            micromanage = True
                    if micromanage == False or self.step_number > 200:
                        self.step_number = 0
                        self.sub_action_number = 0
                        self.action_number = 1
                        if obs.observation.control_groups[0][1] >= self.ARMY_ATTACK_THRESHOLD:
                            if abs(kmeans.cluster_centers_[0][0] - self.possible_enemy_base[0]) < 4 and abs(kmeans.cluster_centers_[0][1] - self.possible_enemy_base[1]) < 4:
                                self.possible_enemy_base_destroyed = True
                            if self.possible_enemy_base_destroyed == False:
                                if self.can_do(obs, actions.FUNCTIONS.Attack_minimap.id):
                                    return actions.FUNCTIONS.Attack_minimap("now", self.possible_enemy_base)
                            if abs(kmeans.cluster_centers_[0][0] - self.main_enemy_base[0]) < 4 and abs(kmeans.cluster_centers_[0][1] - self.main_enemy_base[1]) < 4:
                                self.possible_enemy_base_destroyed = True
                            if self.main_enemy_base_destroyed == False:
                                if self.can_do(obs, actions.FUNCTIONS.Attack_minimap.id):
                                    return actions.FUNCTIONS.Attack_minimap("now", self.main_enemy_base)
                            ############################################SEARCH ENTIRE MAP############
                        else:
                            if self.can_do(obs, actions.FUNCTIONS.Move_minimap.id):
                                if self.unit_type_is_selected(obs, units.Protoss.Probe) == False:
                                    return actions.FUNCTIONS.Move_minimap("now", (self.army_rally_camera[0], self.army_rally_camera[1] - 2*self.build_lean[1]))
                        
            if self.sub_action_number % 4 == 2 and self.sub_action_number >= 6:
                return actions.FUNCTIONS.select_control_group("recall", int(round((self.sub_action_number - 2) / 4)))
            
            if self.sub_action_number % 4 == 3 and self.sub_action_number >= 7:
                x = int(round((self.sub_action_number - 3) / 4))
                if len(scrap_metals[x]) > 0:
                    scrap_metals_x = []
                    scrap_metals_y = []
                    for i in range(len(scrap_metals[x])):
                        scrap_metals_x.append(scrap_metals[x][i].x)
                        scrap_metals_y.append(scrap_metals[x][i].y)
                    scrap_metals_x = sum(scrap_metals_x) / len(scrap_metals_x)
                    scrap_metals_y = sum(scrap_metals_y) / len(scrap_metals_y)
                    optimal_move = self.get_optimal_move(obs, x, scrap_metals_x, scrap_metals_y)
                    if self.unit_type_is_selected(obs, self.ARMY_COMPOSITION[x]):
                        if self.can_do(obs, actions.FUNCTIONS.Scan_Move_screen.id):
                            return actions.FUNCTIONS.Scan_Move_screen("now", optimal_move)
                    
            if self.sub_action_number % 4 == 0 and self.sub_action_number >= 8:
                if len(sentries) > 0:
                    if self.time_shield_up > 300:
                        for i in range(len(sentries)):
                            if sentries[i].energy > 75:
                                return actions.FUNCTIONS.select_point("select", (sentries[i].x, sentries[i].y))
                                    
            if self.sub_action_number % 4 == 1 and self.sub_action_number >= 9:
                self.sub_action_number = 0
                if obs.observation.control_groups[0][1] < self.ARMY_ATTACK_THRESHOLD:#############
                    self.action_number = 1
                if self.unit_type_is_selected(obs, units.Protoss.Sentry):
                    if self.can_do(obs, actions.FUNCTIONS.Effect_GuardianShield_quick.id):
                        self.time_shield_up = 0
                        return actions.FUNCTIONS.Effect_GuardianShield_quick("now")
                    
        
            if self.sub_action_number == 100:
                self.sub_action_number == 0
            """
                
        #Select worker and center camera on natural expansion, build nexus and assimilators
        if self.action_number == 11:
            
            if self.sub_action_number == 1:
                self.number_of_bases+=1
                return actions.FUNCTIONS.select_control_group("recall", 8)
                    
            if self.sub_action_number == 3:
                self.camera_location = 1
                return actions.FUNCTIONS.move_camera(self.natural_base_camera)
            
            if self.sub_action_number == 5:
                if self.unit_type_is_selected(obs, units.Protoss.Probe):
                    if self.can_do(obs, actions.FUNCTIONS.Build_Nexus_screen.id):
                        return actions.FUNCTIONS.Build_Nexus_screen("queued", (48, 48))
                
            if self.sub_action_number == 6:
                self.geysers = self.get_units_by_type(obs, units.Neutral.VespeneGeyser)
                if self.unit_type_is_selected(obs, units.Protoss.Probe):
                    if self.can_do(obs, actions.FUNCTIONS.Build_Assimilator_screen.id):
                        return actions.FUNCTIONS.Build_Assimilator_screen("queued", (self.geysers[0].x, self.geysers[0].y))
                
            if self.sub_action_number == 7:
                self.sub_action_number = 0
                self.action_number = 1
                if self.unit_type_is_selected(obs, units.Protoss.Probe):
                    if self.can_do(obs, actions.FUNCTIONS.Build_Assimilator_screen.id):
                        return actions.FUNCTIONS.Build_Assimilator_screen("queued", (self.geysers[1].x, self.geysers[1].y))
                            
                            
        #Research and warpgates
        if self.action_number == 12:
            
            if self.sub_action_number == 2:
                self.camera_location = 0
                return actions.FUNCTIONS.move_camera(self.main_base_camera)
            
            if self.sub_action_number == 4:
                return actions.FUNCTIONS.select_point("select", (cores[0].x, cores[0].y))
            
            if self.sub_action_number == 5:
                self.sub_action_number = 0
                self.action_number = 6
                if self.unit_type_is_selected(obs, units.Protoss.CyberneticsCore):
                    if self.can_do(obs, actions.FUNCTIONS.Research_WarpGate_quick.id):
                        self.researching_warpgates = True
                        return actions.FUNCTIONS.Research_WarpGate_quick("now")
            
            
        
        return actions.FUNCTIONS.no_op()





def main(unused_argv):
    agent = ProtossAgent()
    try:
        while True:
            with sc2_env.SC2Env(
                    #Map selection
                    map_name="Simple64",
                    #Players
                    players=[sc2_env.Agent(sc2_env.Race.protoss),
                             sc2_env.Bot(sc2_env.Race.zerg,
                                         sc2_env.Difficulty.very_easy)],
                    #Define map and minimap size
                    agent_interface_format=features.AgentInterfaceFormat(
                            feature_dimensions=features.Dimensions(screen=96, minimap=64),
                            use_feature_units=True),
                    step_mul=1,
                    game_steps_per_episode=0,
                    visualize=True) as env:
                
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