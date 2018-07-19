#TO-DO:
#FIX ACCURACY OF MINERALS AND GAS LOCATION DETECTION
#FIND OUT HOW TO OPTIMIZE UNIT QUEUING AND COUNTING
#CREDIT STEVEN BROWN

from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
from absl import app
import random



#Main class
class ProtossAgent(base_agent.BaseAgent):
    
    STEP_CYCLE = 22
    
    VIABLE_MINERALS = 2
    GEYSERS_PER_BASE = 2
    COORDINATES = 2
    
    step_number = -1
    time_supply_needed = 0
    time_without_idle = 0
    building_pylons = False
    scout_sent = False
    
    initial_camera = [0, 0]
    build_lean = [0, 0]
    build_area = [0, 0]
    pylon_area = [[0, 0],
                  [0, 0]]
    
    base_saturated = [False, False]
    minerals_filled = [False, False]
    assimilator_filled = [[False, False],
                          [False, False]]
    
    
    #Initializes variables
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
    
    
    #Adds all units of a type to an array
    def get_units_by_type(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units
                        if unit.unit_type == unit_type]
    
    
    #See if unit can execute action
    def can_do(self, obs, action):
        return action in obs.observation.available_actions
    
    
    #Optimal location generator
    def random_location(self):
        return [random.randint(0, 83),
                random.randint(0, 83)]
    
    
    
    
    #Decision making section, returns an action at the end of each step of the game
    def step(self, obs):
        super(ProtossAgent, self).step(obs)
        
        #If first step of the game
        if obs.first():
            
            #Find locations of units and average them, use average to determine if top left or bottom right
            player_y, player_x = (obs.observation.feature_minimap.player_relative ==
                                  features.PlayerRelative.SELF).nonzero()
            
            xmean = player_x.mean()
            ymean = player_y.mean()
            
            if xmean <= 31 and ymean <= 31:
                self.attack_coordinates = (39, 45)
                self.initial_camera = [19, 23]
                self.pylon_area[1][0] = 0
                self.pylon_area[1][1] = 0
                
            else:
                self.attack_coordinates = (19, 23)
                self.initial_camera = [39, 45]
                self.pylon_area[1][0] = 83
                self.pylon_area[1][1] = 83
                
            return actions.FUNCTIONS.move_camera(self.initial_camera)
        
        player_y, player_x = (obs.observation.feature_minimap.player_relative ==
                                  features.PlayerRelative.NEUTRAL).nonzero()
        
        print(player_y)
        print(player_x)
        
        self.step_number+=1
        
        
        nexi = self.get_units_by_type(obs, units.Protoss.Nexus)
        probes = self.get_units_by_type(obs, units.Protoss.Probe)
        minerals = self.get_units_by_type(obs, units.Neutral.MineralField)
        geysers = self.get_units_by_type(obs, units.Neutral.VespeneGeyser)
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
        
        
        
        #Check if 16 probes on the nexus
        for i in range(0, len(nexi)):
            if nexi[i].assigned_harvesters >= nexi[i].ideal_harvesters:
                self.minerals_filled[i] = True        
        
        #Check if 3 probes on the assimilators
        for i in range(0, len(nexi)):
            for j in range(0, len(assimilators)):
                if assimilators[(i+1)*(j+1)-1].assigned_harvesters >= assimilators[(i+1)*(j+1)-1].ideal_harvesters and assimilators[(i+1)*(j+1)-1].ideal_harvesters != 0:
                    self.assimilator_filled[i][j] = True
        
        
        (obs.observation.player.minerals)
        
        
        if self.step_number%self.STEP_CYCLE == 0:
            
            #Select Nexus
            if len(nexi) > 0:
                nexus = random.choice(nexi)
                return actions.FUNCTIONS.select_point("select", (nexus.x, nexus.y))
        
        
        if self.step_number%self.STEP_CYCLE == 1:
            
            #Rally Probes
            if self.unit_type_is_selected(obs, units.Protoss.Nexus):
                self.base_saturated[0] = False
                
                #If no idle Probe for 10 seconds, send the next Probe to idle location
                if self.can_do(obs, actions.FUNCTIONS.select_idle_worker.id) == False:
                    self.time_without_idle+=1
                    
                    if self.time_without_idle > 10 or self.step_number == 1:
                        return actions.FUNCTIONS.Rally_Workers_screen("now", (42, 42))
            
                else:
                    self.time_without_idle = 0
                
                #Send Probe to Minerals
                for i in range(len(nexi)):
                    if self.minerals_filled[i] == False:
                        return actions.FUNCTIONS.Rally_Workers_screen("now", (minerals[0].x, minerals[0].y))
                
                #Send Probe to Assimilator #NOT WORKING########################################
                for i in range(len(nexi)):
                    for j in range(self.GEYSERS_PER_BASE):
                        if self.assimilator_filled[i][j] == False:
                            return actions.FUNCTIONS.Rally_Workers_screen("now", (assimilators[(i+1)*(j+1)-1].x, assimilators[(i+1)*(j+1)-1].y))
                    
                #Saturated Base
                if self.can_do(obs, actions.FUNCTIONS.Cancel_Last_quick.id):
                    self.base_saturated[0] = True
                    return actions.FUNCTIONS.Cancel_Last_quick("now")
        
        if self.step_number%self.STEP_CYCLE == 2 and self.base_saturated[0] == False:
            
            #Train Probes
            if self.unit_type_is_selected(obs, units.Protoss.Nexus):
                if len(obs.observation.build_queue) <= 1:
                    if self.can_do(obs, actions.FUNCTIONS.Train_Probe_quick.id):
                        return actions.FUNCTIONS.Train_Probe_quick("now")
                
                
        if self.step_number%self.STEP_CYCLE == 3:
            #Select Idle Probe
            if self.can_do(obs, actions.FUNCTIONS.select_idle_worker.id):
                return actions.FUNCTIONS.select_idle_worker("select")
            
            
        if self.step_number%self.STEP_CYCLE == 4:
            #ADD 3 PRECONSTRUCTED PYLONS, THEN ADD NEW SPACE TO PLACE FUTURE PYLONS
            #Build Pylons IF about to be supply capped
            if self.unit_type_is_selected(obs, units.Protoss.Probe):
                free_supply = (obs.observation.player.food_cap -
                               obs.observation.player.food_used)
                
                if free_supply < 20 and obs.observation.player.food_cap != 200:
                    self.time_supply_needed+=1
                    
                    if self.time_supply_needed > 10 or len(pylons) == 0:
                        if self.can_do(obs, actions.FUNCTIONS.Build_Pylon_screen.id):
                            self.time_supply_needed = 0
                            
                            if len(pylons) == 0:
                                unit_type = obs.observation["feature_screen"][features.SCREEN_FEATURES.unit_type.index]
                                mineral_y, mineral_x = (unit_type == units.Neutral.MineralField).nonzero()
                                
                                dx = int(round(mineral_x.mean()))
                                dy = int(round(mineral_y.mean()))
                                x = nexi[0].x
                                y = nexi[0].y
                                self.pylon_area[0][0] = dx
                                self.pylon_area[0][1] = dy
                                
                                dx-=x
                                dy-=y
                                
                                if dx < 0:
                                    self.build_lean[0] = -1
                                else:
                                    self.build_lean[0] = 1
                                
                                if dy < 0:
                                    self.build_lean[1] = -1
                                else:
                                    self.build_lean[1] = 1
                                
                                x-=(dx + 0*self.build_lean[0])
                                y-=(dy + 5*self.build_lean[1])
                                
                                self.build_area[0] = x
                                self.build_area[1] = y
                                
                                return actions.FUNCTIONS.Build_Pylon_screen("now", self.build_area)
                            
                            elif len(pylons) == 1:
                                return actions.FUNCTIONS.Build_Pylon_screen("now", (self.build_area[0] + self.build_lean[0]*25, self.build_area[1]))
                                
                            elif len(pylons) == 2:
                                return actions.FUNCTIONS.Build_Pylon_screen("now", (self.build_area[0], self.build_area[1] + self.build_lean[1]*25))
                                
                            else:
                                if(self.pylon_area[1][0] < self.pylon_area[0][0]):
                                    return actions.FUNCTIONS.Build_Pylon_screen("now", (random.randint(self.pylon_area[1][0], self.pylon_area[0][0]), random.randint(self.pylon_area[1][1], self.pylon_area[0][1])))
                                else:
                                    return actions.FUNCTIONS.Build_Pylon_screen("now", (random.randint(self.pylon_area[0][0], self.pylon_area[1][0]), random.randint(self.pylon_area[0][1], self.pylon_area[1][1])))
        
        
        if self.step_number%self.STEP_CYCLE == 7 and len(pylons) > 0 and len(assimilators) < 2*len(nexi):
            
            #Build Assimilators
            if self.unit_type_is_selected(obs, units.Protoss.Probe):
                if self.can_do(obs, actions.FUNCTIONS.Build_Assimilator_screen.id):
                    return actions.FUNCTIONS.Build_Assimilator_screen("now", (geysers[len(assimilators)%2].x, geysers[len(assimilators)%2].y))
                        
        
        if self.step_number%self.STEP_CYCLE == 8:
            
            #Tech build order
            if self.unit_type_is_selected(obs, units.Protoss.Probe):
                
                if len(gateways) < 1:
                    if self.can_do(obs, actions.FUNCTIONS.Build_Gateway_screen.id):
                        return actions.FUNCTIONS.Build_Gateway_screen("now", self.random_location())
                    
                elif len(cores) < 1:
                    if self.can_do(obs, actions.FUNCTIONS.Build_CyberneticsCore_screen.id):
                        return actions.FUNCTIONS.Build_CyberneticsCore_screen("now", self.random_location())
                            
                elif len(forges) < 1:
                    if self.can_do(obs, actions.FUNCTIONS.Build_Forge_screen.id):
                        return actions.FUNCTIONS.Build_Forge_screen("now", self.random_location())
                    
                elif len(nexi) > 0:
                    
                    if len(gateways) < 2:
                        if self.can_do(obs, actions.FUNCTIONS.Build_Gateway_screen.id):
                            return actions.FUNCTIONS.Build_Gateway_screen("now", self.random_location())
                    
                    elif len(facilities) < 1:
                        if self.can_do(obs, actions.FUNCTIONS.Build_RoboticsFacility_screen.id):
                            return actions.FUNCTIONS.Build_RoboticsFacility_screen("now", self.random_location())
                        
                    elif len(forges) < 2:
                        if self.can_do(obs, actions.FUNCTIONS.Build_Forge_screen.id):
                            return actions.FUNCTIONS.Build_Forge_screen("now", self.random_location())
                        
                    elif len(councils) < 1:
                        if self.can_do(obs, actions.FUNCTIONS.Build_TwilightCouncil_screen.id):
                            return actions.FUNCTIONS.Build_TwilightCouncil_screen("now", self.random_location())
                        
                    elif len(gateways) < 4:
                        if self.can_do(obs, actions.FUNCTIONS.Build_Gateway_screen.id):
                            return actions.FUNCTIONS.Build_Gateway_screen("now", self.random_location())
                        
                    elif len(archives) < 1:
                        if self.can_do(obs, actions.FUNCTIONS.Build_TemplarArchive_screen.id):
                            return actions.FUNCTIONS.Build_TemplarArchive_screen("now", self.random_location())
                        
                    elif len(facilities) < 2:
                        if self.can_do(obs, actions.FUNCTIONS.Build_RoboticsFacility_screen.id):
                            return actions.FUNCTIONS.Build_RoboticsFacility_screen("now", self.random_location())
        
        
    
        
        
        if self.step_number%self.STEP_CYCLE == 16:
            
            #Build 2nd Nexus if enough resources
            if self.unit_type_is_selected(obs, units.Protoss.Probe):
                if len(nexi) < 2:
                    if self.can_do(obs, actions.FUNCTIONS.Build_Nexus_screen.id):
                        print("richboi")
                        #return actions.FUNCTIONS.Build_Nexus_screen("now", (0, 0))
        
        
        if self.step_number%self.STEP_CYCLE == 9:
            
            #Select a random Gateway###########
            if len(gateways) > 0:
                gateway = random.choice(gateways)
                return actions.FUNCTIONS.select_point("select", (gateway.x,
                                                                 gateway.y))
                
                
        if self.step_number%self.STEP_CYCLE == 10:
            
            #Train zealots if gateway selected
            if self.unit_type_is_selected(obs, units.Protoss.Gateway):
                if self.can_do(obs, actions.FUNCTIONS.Train_Zealot_quick.id):
                    return actions.FUNCTIONS.Train_Zealot_quick("now")
        
        
        if self.step_number%self.STEP_CYCLE == 11 and self.scout_sent == False:
            
            #Select 1 Zealot to scout
            if len(zealots) == 1:
                if self.can_do(obs, actions.FUNCTIONS.select_army.id):
                    return actions.FUNCTIONS.select_army("select")
                
        
        if self.step_number%self.STEP_CYCLE == 12 and self.scout_sent == False:
            
            #Scout with Zealot
            if self.unit_type_is_selected(obs, units.Protoss.Zealot):
                if self.can_do(obs, actions.FUNCTIONS.Move_minimap.id):
                    self.scout_sent = True
                    return actions.FUNCTIONS.Move_minimap("now",
                                                          self.attack_coordinates)
        
        
        
        
        
        
        
        
            
            
      
        
        
        
      
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
                            feature_dimensions=features.Dimensions(screen=84, minimap=64),
                            
                            #Use feature units
                            use_feature_units=True),
                            
                    #Number of steps that will pass before bot makes an action
                    step_mul=1,
                    
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