from devices import Pump, MoistureSensor
import time
from filters import MovingAverage, Clamp


class SmartPlant:
    def __init__(self,
                 name: str,
                 pump_pin: int,
                 moisture_sensor_pin: int,
                 dry_reference: int = 4095,
                 wet_reference: int = 3000,
                 dry_treshold: int = 30,
                 filter_window_size: int = 10):
        self.name = name
        self.pump = Pump(pump_pin)
        self.moisture_sensor = MoistureSensor(moisture_sensor_pin,
                                              dry_reference,
                                              wet_reference)
        self.__filters = [
            Clamp(0, 100),
            MovingAverage(window_size=filter_window_size)
        ]
        self.latest_moisture_level = None
        self.latest_reading_timestamp = None
        self.dry_treshold = dry_treshold
    
    def filter_value(self, value):
        filtered = value
        for filter_ in self.__filters:
            filtered = filter_(filtered) 
        return filtered
    
    def read_moisture_level(self):
        unfiltered = self.moisture_sensor.read_percent()
        filtered = self.filter_value(unfiltered)
        print(f"{self.name} - Unfiltered moisture level: {unfiltered}%. Filtered: {filtered}")
        print(f"\t Last {len(self.__filters[-1].__window)} readings: {self.__filters[-1].__window}")
        self.latest_moisture_level = filtered
        self.latest_reading_timestamp = time.time_ns()
        return filtered

    def needs_watering(self):
        if self.latest_moisture_level is not None:
            return self.latest_moisture_level <= self.dry_treshold
        return False
    
    def water_on(self):
        self.pump.on()
    
    def water_off(self):
        self.pump.off()
    
    def water(self, duration_seconds: int = 1):
        self.pump.on()
        time.sleep(duration_seconds)
        self.pump.off()