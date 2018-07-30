# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 14:23:08 2018

@author: makerspace-4
"""

## class variables
    truzealots = 0
    truimmortals = 0
    trustalkers = 0
    trusentries = 0
    truprobes = 0
    pb = 0
    t = 0
    trunumunits = {truzealots,trustalkers,trusentries,truimmortals,truprobes,t}
    
    xc = 10 #changed from 10
    yc = 9
    
    
    #actual cheese
    self.t += 1
    def Find_Units(self,obs,time): # time however many steps you want it to run
        if self.t%time ==0 :     #and self.t%64 != self.pb  <---- ignore this for now
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
                self.trunumunits = {self.truzealots,self.trustalkers,self.trusentries,self.truimmortals,self.truprobes,self.t}
                print(len(probes))
                print(self.truprobes)
                print(self.trunumunits)
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
                print(self.trunumunits)
                self.truzealots = 0
                self.trustalkers = 0
                self.trusentries = 0
                self.truimmortals = 0
                self.truprobes = 0