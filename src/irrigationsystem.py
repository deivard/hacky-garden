import time
from smartplant import SmartPlant
from logger import log_moisture_level
        

class IrrigationSystem:
    def __init__(self,
                 smart_plants: list[SmartPlant] = None,
                 monitor_interval_seconds: int = 3600) -> None:
        if smart_plants is None:
            smart_plants = []
        self.smart_plants = smart_plants
        self.monitor_interval_seconds = monitor_interval_seconds
    
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
        
    def start_monitoring(self):
        while True:
            start_time = time.time()

            self.update_moisture_readings()
            self.log_moisture_levels()
            self.water_dry_plants()
            
            end_time = time.time()
            next_monitor_time = end_time - start_time
            time_to_sleep = next_monitor_time - time.time()
            time.sleep(time_to_sleep)
            print(f"Sleeping for {time_to_sleep}")
