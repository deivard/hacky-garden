from devices import Pump, MoistureSensor
import time
from filters import MovingAverage

class SmartPlant:
    def __init__(self,
                 name: str,
                 pump_pin: int,
                 moisture_sensor_pin: int,
                 dry_treshold: int = 30):
        self.name = name
        self.pump = Pump(pump_pin)
        self.moisture_sensor = MoistureSensor(moisture_sensor_pin)
        self.__filter = MovingAverage(window_size=5)
        self.latest_moisture_level = None
        self.latest_reading_timestamp = None
        self.dry_treshold = dry_treshold
    
    def read_moisture_level(self):
        filtered_moisture_level = self.__filter(self.moisture_sensor.read_percent())
        self.latest_moisture_level = filtered_moisture_level
        self.latest_reading_timestamp = time.time()
        return filtered_moisture_level

    def needs_watering(self):
        return self.latest_moisture_level <= self.dry_treshold
    
    def water_on(self):
        self.pump.on()
    
    def water_off(self):
        self.pump.off()
    
    def water(self, duration_seconds: int = 1):
        self.pump.on()
        time.sleep(duration_seconds)
        self.pump.off()