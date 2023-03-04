from machine import Pin, ADC

class ReferenceLevels:
    def __init__(self, dry: int = 4095, wet: int = 3000) -> None:
        self.dry = dry
        self.wet = wet
        
        if dry <= wet:
            raise ValueError("Dry reference level cannot be lower than wet reference level.")


class MoistureSensor:
    def __init__(self, pin_id: int,
                 dry_reference: int = 4095,
                 wet_reference: int = 3000) -> None:
        self.__pin = ADC(Pin(pin_id))
        self.__pin.atten(ADC.ATTN_11DB)
        self.__reference_levels = ReferenceLevels(dry_reference, wet_reference)

    def __value_to_percent(self, value):
        new_value = ( 
            (((value - self.__reference_levels.dry) * (100 - 0))
            / (self.__reference_levels.wet - self.__reference_levels.dry))
            + 0
        )
        return new_value

    def read_raw(self):
        return self.__pin.read()
    
    def read_percent(self):
        return self.__value_to_percent(self.read_raw())

    def read_percent_and_raw(self):
        raw = self.read_raw()
        return self.__value_to_percent(raw), raw
