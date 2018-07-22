#CREDIT STEVEN BROWN

from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
from absl import app
import random, math
from sklearn.cluster import KMeans

class ProtossAgent(base_agent.BaseAgent):
    
    MINIMAP_DIM = 64
    
    step_number = 0
    action_number = 1
    sub_action_number = 0
    number_of_bases = 1
    time_until_nexus = 2000
    time_supply_needed = 10
    time_without_idle = 10
    stop_worker_production = False
    main_base_filled = False
    minerals_filled = False
    
    resource_locations = []
    main_base_camera = [0, 0]
    natural_base_camera = [0, 0]
    main_enemy_base = [0, 0]
    possible_enemy_base = [0, 0]
    nexus_location = [0, 0]
    build_lean = [0, 0]
    first_pylon_location = [0, 0]
    pylon_area = [[0, 0],
                  [0, 0]]
    
    geysers = []
    
    
    
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
    
    #Adds all units of the same type on screen to an array
    def get_units_by_type(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units
                        if unit.unit_type == unit_type]
    
    #Checks if selected unit can execute an action
    def can_do(self, obs, action):
        return action in obs.observation.available_actions
    
    #Generates a random location on the screen
    def random_location(self):
        return [random.randint(0, 83), random.randint(0, 69)]
    
    
    
    
    
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
                self.pylon_area[1][0] = 0
                self.build_lean[0] = -1
            else:
                self.pylon_area[1][0] = 69
                self.build_lean[0] = 1
                
            if ymean < self.MINIMAP_DIM / 2:
                self.pylon_area[1][1] = 0
                self.build_lean[1] = -1
            else:
                self.pylon_area[1][1] = 69
                self.build_lean[1] = 1    
            for i in range(number_of_clusters):
                if abs(self.resource_locations[i][1] - ymean) < 10:
                    if abs(self.resource_locations[i][0] - xmean) < 10:
                        self.main_base_camera[0] = self.resource_locations[i][0] - self.build_lean[0]
                        self.main_base_camera[1] = self.resource_locations[i][1] + self.build_lean[1]
                    else:
                        self.natural_base_camera[0] = self.resource_locations[i][0] - self.build_lean[0]
                        self.natural_base_camera[1] = self.resource_locations[i][1] + self.build_lean[1]
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
        
        
        
        
        
        self.sub_action_number+=1
        if self.number_of_bases == 2 and self.time_until_nexus > 0:
            self.time_until_nexus-=1
        
        
        
        #Select the main base and train and send workers to resources
        if self.action_number == 1:
            
            if self.sub_action_number == 1:
                return actions.FUNCTIONS.move_camera(self.main_base_camera)
            
            if self.sub_action_number == 2:
                return actions.FUNCTIONS.no_op()
            
            if self.sub_action_number == 3:
                if len(self.geysers) == 0:
                    self.geysers = self.get_units_by_type(obs, units.Neutral.VespeneGeyser)
                if self.number_of_bases == 1 and len(nexi) > 0:
                    self.nexus_location[0] = nexus.x
                    self.nexus_location[1] = nexus.y
                if len(nexi) > 0:
                    return actions.FUNCTIONS.select_point("select", self.nexus_location)
            
            if self.sub_action_number == 4:
                if self.unit_type_is_selected(obs, units.Protoss.Nexus):
                    if self.can_do(obs, actions.FUNCTIONS.select_idle_worker.id):
                        self.time_without_idle = 0
                    else:
                        self.time_without_idle+=1
                        if self.time_without_idle > 10:
                            return actions.FUNCTIONS.Rally_Workers_screen("now", (42, 42))
                    if nexus.assigned_harvesters < nexus.ideal_harvesters:
                        return actions.FUNCTIONS.Rally_Workers_screen("now", (minerals[0].x, minerals[0].y))
                    for i in range(len(assimilators)):
                        if assimilators[i].assigned_harvesters < assimilators[i].ideal_harvesters and assimilators[i].ideal_harvesters != 0:
                            return actions.FUNCTIONS.Rally_Workers_screen("now", (assimilators[i].x, assimilators[i].y))
                    if self.number_of_bases == 1:
                        self.main_base_filled = True
                        if self.can_do(obs, actions.FUNCTIONS.Cancel_Last_quick.id):
                            return actions.FUNCTIONS.Cancel_Last_quick("now")
                    if self.minerals_filled:
                        if self.can_do(obs, actions.FUNCTIONS.Cancel_Last_quick.id):
                            return actions.FUNCTIONS.Cancel_Last_quick("now")
                            
            if self.sub_action_number == 5:
                print(self.minerals_filled)
                print(len(obs.observation.build_queue))
                if self.number_of_bases == 1:
                    self.sub_action_number = 0
                    self.action_number = 2
                if self.minerals_filled == False and (self.main_base_filled == False or self.number_of_bases > 1):
                    if self.unit_type_is_selected(obs, units.Protoss.Nexus):
                        if len(obs.observation.build_queue) <= 1:
                            if self.can_do(obs, actions.FUNCTIONS.Train_Probe_quick.id):
                                return actions.FUNCTIONS.Train_Probe_quick("now")
            
            if self.sub_action_number == 6:
                return actions.FUNCTIONS.move_camera(self.natural_base_camera)
            
            if self.sub_action_number == 7:
                return actions.FUNCTIONS.no_op()
            
            if self.sub_action_number == 8:
                self.sub_action_number = 0
                self.action_number = 2
                if self.unit_type_is_selected(obs, units.Protoss.Nexus):
                    return actions.FUNCTIONS.Rally_Workers_screen("now", (minerals[0].x, minerals[0].y))
                
                
        #Select idle worker and build pylons and assimilators
        if self.action_number == 2:
            
            if self.sub_action_number == 1:
                if self.can_do(obs, actions.FUNCTIONS.select_idle_worker.id):
                    return actions.FUNCTIONS.select_idle_worker("select")
            
            if self.sub_action_number == 2:
                return actions.FUNCTIONS.move_camera(self.main_base_camera)
                
            if self.sub_action_number == 3:
                return actions.FUNCTIONS.no_op()
            
            if self.sub_action_number == 4:
                if self.unit_type_is_selected(obs, units.Protoss.Probe):
                    if obs.observation.player.food_cap - obs.observation.player.food_used < 20 and obs.observation.player.food_cap != 200:
                        self.time_supply_needed+=1
                        if self.time_supply_needed > 10:
                            if self.can_do(obs, actions.FUNCTIONS.Build_Pylon_screen.id):
                                self.time_supply_needed = 0
                                if len(pylons) == 0:
                                    unit_type = obs.observation["feature_screen"][features.SCREEN_FEATURES.unit_type.index]
                                    mineral_y, mineral_x = (unit_type == units.Neutral.MineralField).nonzero()
                                    dx = int(round(mineral_x.mean()))
                                    dy = int(round(mineral_y.mean()))
                                    x = nexus.x
                                    y = nexus.y
                                    self.pylon_area[0][0] = dx
                                    self.pylon_area[0][1] = dy - 40*self.build_lean[1]
                                    dx-=x
                                    dy-=y
                                    x-=(dx + 5*self.build_lean[0])
                                    y-=(dy + 5*self.build_lean[1])
                                    self.first_pylon_location[0] = x
                                    self.first_pylon_location[1] = y
                                    return actions.FUNCTIONS.Build_Pylon_screen("queued", self.first_pylon_location)
                                elif len(pylons) == 1:
                                    return actions.FUNCTIONS.Build_Pylon_screen("queued", (self.first_pylon_location[0] + self.build_lean[0]*35, self.first_pylon_location[1]))
                                elif len(pylons) == 2:
                                    return actions.FUNCTIONS.Build_Pylon_screen("queued", (self.first_pylon_location[0], self.first_pylon_location[1] + self.build_lean[1]*35))
                                else:
                                    if(self.pylon_area[1][0] < self.pylon_area[0][0]):
                                        return actions.FUNCTIONS.Build_Pylon_screen("queued", (random.randint(self.pylon_area[1][0], self.pylon_area[0][0]), random.randint(self.pylon_area[1][1], self.pylon_area[0][1])))
                                    else:
                                        return actions.FUNCTIONS.Build_Pylon_screen("queued", (random.randint(self.pylon_area[0][0], self.pylon_area[1][0]), random.randint(self.pylon_area[0][1], self.pylon_area[1][1])))
                                    
            if self.sub_action_number == 5:
                self.sub_action_number = 0
                if self.time_until_nexus == 0:
                    self.action_number = 3
                elif obs.observation.player.minerals > 550 and self.number_of_bases == 1:
                    self.action_number = 10
                else:
                    self.action_number = 1
                if len(pylons) > 0 and len(assimilators) < len(self.geysers):
                    if self.unit_type_is_selected(obs, units.Protoss.Probe):
                        if self.can_do(obs, actions.FUNCTIONS.Build_Assimilator_screen.id):
                            return actions.FUNCTIONS.Build_Assimilator_screen("queued", (self.geysers[len(assimilators)].x, self.geysers[len(assimilators)].y))
            
            
        #Pan camera to natural expansion to train and send workers to resources
        if self.action_number == 3:
            if self.sub_action_number == 1:
                return actions.FUNCTIONS.move_camera(self.natural_base_camera)
            
            if self.sub_action_number == 2:
                return actions.FUNCTIONS.no_op()
            
            if self.sub_action_number == 3:
                return actions.FUNCTIONS.select_point("select", (42, 42))
                
            if self.sub_action_number == 4:
                if self.unit_type_is_selected(obs, units.Protoss.Nexus):
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
                            
            if self.sub_action_number == 5:
                print(len(obs.observation.build_queue))
                self.sub_action_number = 0
                self.action_number = 1
                if self.stop_worker_production == False:
                    if self.unit_type_is_selected(obs, units.Protoss.Nexus):
                        if len(obs.observation.build_queue) <= 1:
                            if self.can_do(obs, actions.FUNCTIONS.Train_Probe_quick.id):
                                return actions.FUNCTIONS.Train_Probe_quick("now")
                            
                            
        #Select worker, pan camera to natural expansion, and build nexus and assimilators
        if self.action_number == 10:
            
            if self.sub_action_number == 1:
                self.number_of_bases+=1
                if self.can_do(obs, actions.FUNCTIONS.select_idle_worker.id):
                    return actions.FUNCTIONS.select_idle_worker("select")
                    
            if self.sub_action_number == 2:
                return actions.FUNCTIONS.move_camera(self.natural_base_camera)
            
            if self.sub_action_number == 3:
                return actions.FUNCTIONS.no_op()
            
            if self.sub_action_number == 4:
                if self.unit_type_is_selected(obs, units.Protoss.Probe):
                    if self.can_do(obs, actions.FUNCTIONS.Build_Nexus_screen.id):
                        return actions.FUNCTIONS.Build_Nexus_screen("queued", (42, 42))
                
            if self.sub_action_number == 5:
                self.geysers = self.get_units_by_type(obs, units.Neutral.VespeneGeyser)
                if self.unit_type_is_selected(obs, units.Protoss.Probe):
                    if self.can_do(obs, actions.FUNCTIONS.Build_Assimilator_screen.id):
                        return actions.FUNCTIONS.Build_Assimilator_screen("queued", (self.geysers[0].x, self.geysers[0].y))
                
            if self.sub_action_number == 6:
                self.sub_action_number = 0
                self.action_number = 1
                if self.unit_type_is_selected(obs, units.Protoss.Probe):
                    if self.can_do(obs, actions.FUNCTIONS.Build_Assimilator_screen.id):
                        return actions.FUNCTIONS.Build_Assimilator_screen("queued", (self.geysers[1].x, self.geysers[1].y))
                            
                            
                            
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
                                     sc2_env.Bot(sc2_env.Race.random,
                                                             sc2_env.Difficulty.very_easy)],
                    
                    #Define map and minimap size and enable feature units
                    agent_interface_format=features.AgentInterfaceFormat(
                            feature_dimensions=features.Dimensions(screen=84, minimap=64),
                            use_feature_units=True),
                            
                    #Number of steps that will pass before bot makes an action
                    step_mul=1,
                    
                    #Unlimited game length
                    game_steps_per_episode=0,
                    
                    #GUI
                    visualize=True) as env:
                
                #Looping code
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