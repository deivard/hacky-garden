from machine import Pin, ADC

class ReferenceLevels:
    def __init__(self, water: int = 300, air: int = 2300) -> None:
        self.water = water
        self.air = air
        
        if air <= water:
            raise ValueError("Air reference level cannot be lower than water reference level.")


class MoistureSensor:
    def __init__(self, pin_id: int) -> None:
        self.__pin = ADC(Pin(pin_id))
        self.__pin.atten(ADC.ATTN_11DB)
        self.__reference_levels = ReferenceLevels()

    def __value_to_percent(self, value):
        new_value = ( 
            (((value - self.__reference_levels.water) * (100 - 0))
            / (self.__reference_levels.air - self.__reference_levels.water))
            + 0
        )
        return new_value

    def read_raw(self):
        return self.__pin.read()

    def read_percent(self):
        return self.__value_to_percent(self.read_raw())

