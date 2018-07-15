#TO-DO:
#Make method thingy manager for actions
#Fix priority and multi-tasking (e.g. once AI selects zealots for attack, continue building probes, pylons, etc.)





from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
from absl import app
import random

#Main class
class ProtossAgent(base_agent.BaseAgent):
    
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
            
            #Find locations of units and average them, use average to determine if top left or bottom right
            player_y, player_x = (obs.observation.feature_minimap.player_relative ==
                                  features.PlayerRelative.SELF).nonzero()
            xmean = player_x.mean()
            ymean = player_y.mean()
            
            if xmean <= 31 and ymean <= 31:
                self.attack_coordinates = (49, 49)
            else:
                self.attack_coordinates = (12, 16)            
        
        #Attack with zealots
        zealots = self.get_units_by_type(obs, units.Protoss.Zealot)
        if len(zealots) >= 5:
            if self.unit_type_is_selected(obs, units.Protoss.Zealot):
                if self.can_do(obs, actions.FUNCTIONS.Attack_minimap.id):
                        return actions.FUNCTIONS.Attack_minimap("now",
                                                                self.attack_coordinates)
        
        #Select zealots
        if len(zealots) > 0:
            if self.can_do(obs, actions.FUNCTIONS.select_army.id):
                return actions.FUNCTIONS.select_army("select")
        
        
        #Build pylons if free supply less than 10 and not capped at 200
        #PROBLEM: Once AI selects zealots for attack, it no longer has probes selected and can't run this; also building zealots takes priority
        if self.unit_type_is_selected(obs, units.Protoss.Probe):
            free_supply = (obs.observation.player.food_cap -
                                         obs.observation.player.food_used)
            if free_supply < 10 and obs.observation.player.food_cap != 200:
                if self.can_do(obs, actions.FUNCTIONS.Build_Pylon_screen.id):
                    x = random.randint(0, 83)
                    y = random.randint(0, 83)
                    return actions.FUNCTIONS.Build_Pylon_screen("now", (x, y))
      
        
        #Build gateways
        gateways = self.get_units_by_type(obs, units.Protoss.Gateway)
        if len(gateways) < 1:
            if self.unit_type_is_selected(obs, units.Protoss.Probe):
                if self.can_do(obs, actions.FUNCTIONS.Build_Gateway_screen.id):
                    x = random.randint(0, 83)
                    y = random.randint(0, 83)
                    
                    return actions.FUNCTIONS.Build_Gateway_screen("now", (x, y))
        
        #Train zealots if gateway selected
        if self.unit_type_is_selected(obs, units.Protoss.Gateway):
            if self.can_do(obs, actions.FUNCTIONS.Train_Zealot_quick.id):
                return actions.FUNCTIONS.Train_Zealot_quick("now")
            
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
                            feature_dimensions=features.Dimensions(screen=84, minimap=64),
                            
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