'''
Contains utility functions and classes to handle events
'''

import time
from typing import Callable, List,Dict

class TimedEvent:
    '''
    performs a certain function every t seconds
    '''
    def __init__(self,current_time:float,interval:float,function:Callable[[],None]):
        self.function:Callable[[],None] = function
        self.delay:float = interval
        self.previous_time:float = current_time
    def run(self,current_time:float)->None:
        '''
        runs the function if the set time has elapsed
        '''
        #print(current_time,self.previous_time,self.delay)
        if(current_time - self.previous_time > self.delay):
            self.function()
            self.previous_time = current_time
    def reset(self,current_time:float):
        self.previous_time = current_time



class TimedEventManager:
    '''
    Manages a lot of TimedEvent
    '''
    def __init__(self,timer:Callable[[],float]=time.time):
        self.timed_events:List[TimedEvent] = []
        self.timer:Callable[[],float] = timer
    
    def add_event(self,delay:float,function:Callable[[],None]):
        self.timed_events.append(
            TimedEvent(self.timer(),delay,function)
        )
    def reset_all(self):
        for te in self.timed_events:
            te.reset(self.timer())
    def run(self):
        for te in self.timed_events:
            te.run(self.timer())


class Event_Manager:
    def __init__(self):
        self.events : Dict[str,List[Callable[[],None]]] = dict()

    def on_event(self,event_name:str,function: Callable[[],None]):
        if(event_name not in self.events):
            self.events[event_name] = []
        self.events[event_name].append(function)
    def publish_event(self,event_name:str):
        if(event_name in self.events):
            for func in self.events[event_name]:
                func()
                

