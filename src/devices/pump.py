from machine import Pin
from .relay import Relay

class Pump:
    def __init__(self, pin, relay_type=Relay.NORMALLY_OPEN) -> None:
        self.__pin = Pin(pin)
        self.__relay_type = relay_type
    
    def toggle(self):
        self.__pin.value(int(not self.pin.value()))
    
    def on(self):
        self.__pin.value(self.__relay_type.ON)
        
    def off(self):
        self.__pin.value(self.__relay_type.OFF)
