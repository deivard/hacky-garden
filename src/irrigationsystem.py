import time
from smartplant import SmartPlant
from logger import log_moisture_level
from machine import WDT, Pin
import gc


class IrrigationSystem:
    def __init__(self,
                 smart_plants: list[SmartPlant] = None,
                 monitor_interval_seconds: int = 3600,
                 watering_duration: int = 1) -> None:
        if smart_plants is None:
            smart_plants = []
        self.smart_plants = smart_plants
        self.monitor_interval_seconds = monitor_interval_seconds
        self.watering_duration = watering_duration
        self.led = Pin(2, Pin.OUT)
        self.wdt = WDT(timeout=max((self.monitor_interval_seconds + 200)*1000, 5000))
        gc.enable()
    
    def update_moisture_readings(self):
        for plant in self.smart_plants:
            plant.read_moisture_level()
    
    def log_moisture_levels(self):
        for plant in self.smart_plants:
            log_moisture_level(plant.name,
                               plant.latest_moisture_level,
                               plant.latest_reading_timestamp)
    
    def water_dry_plants(self, watering_duration_seconds: int = 1):
        for plant in self.smart_plants:
            if plant.needs_watering():
                print(f"Starts watering {plant.name}")
                plant.water_on()
        time.sleep(watering_duration_seconds)
        for plant in self.smart_plants:
            print(f"Stops watering {plant.name}")
            plant.water_off()
        
    def __get_sleep_time(self, start_time_ns):
        end_time = time.time_ns()
        duration_ns = end_time - start_time_ns
        time_to_sleep = self.monitor_interval_seconds - (duration_ns / 1e9)
        return time_to_sleep
        
    def start_monitoring(self):
        while True:
            self.led.on()
            start_time_ns = time.time_ns()
            # For microcontroller health (RAM and WDT)
            gc.collect()
            self.wdt.feed()

            self.update_moisture_readings()
            self.log_moisture_levels()
            self.water_dry_plants(self.watering_duration)
            self.wdt.feed()
            
            time_to_sleep = self.__get_sleep_time(start_time_ns)
            self.led.off()
            time.sleep(time_to_sleep)
            print(f"Sleeping for {time_to_sleep}")
