import time
from smartplant import SmartPlant
from logger import log_moisture_level, log_watering_time
from machine import WDT, Pin
import gc


class IrrigationSystem:
    def __init__(self,
                 smart_plants: list[SmartPlant] = None,
                 monitor_interval_seconds: int = 3600,
                 watering_cooldown_seconds: int = 60 * 5) -> None:
        if smart_plants is None:
            smart_plants = []
        self.smart_plants = smart_plants
        self.monitor_interval_s = monitor_interval_seconds
        self.watering_cooldown_s = watering_cooldown_seconds
        self.led = Pin(2, Pin.OUT)
        self.wdt = WDT(timeout=max((self.monitor_interval_s + 200)*1000, 5000))
        gc.enable()
    
    def update_moisture_readings(self):
        for plant in self.smart_plants:
            plant.update_moisture_level()
    
    def log_moisture_levels(self):
        for plant in self.smart_plants:
            log_moisture_level(plant.name,
                               plant.latest_moisture_level,
                               plant.latest_reading_timestamp_ns)
    
    def allowed_to_water_plant(self, plant: SmartPlant):
        current_time = time.time()
        if plant.latest_watering_time is None:
            return True
        return (current_time - plant.latest_watering_time) > self.watering_cooldown_s
    
    def __turn_off_pumps_when_finished(self, plants_watering):
        while plants_watering:
            current_time = time.time()
            still_needs_watering = []
            for plant_info in plants_watering:
                if current_time > plant_info["end_time"]:
                    plant_info["plant"].water_off()
                    print(f"Stops watering {plant_info['plant'].name}")
                else:
                    still_needs_watering.append(plant_info)
            plants_watering = still_needs_watering

    def __turn_off_all_pumps(self):
        print("Shuts down all pumps.")
        for plant in self.smart_plants:
            plant.water_off()

    def water_dry_plants(self):
        watered_plants = []
        active_pumps = []
        for plant in self.smart_plants:
            if plant.needs_watering() and self.allowed_to_water_plant(plant):
                print(f"Starts watering {plant.name}")
                plant.water_on()
                active_pumps.append({"plant": plant, "end_time": time.time() + plant.watering_time})
                watered_plants.append(plant)

        self.__turn_off_pumps_when_finished(active_pumps)
        self.__turn_off_all_pumps()
        print("Finished watering.")
        return watered_plants
        
    def log_watering_durations(self, plants):
        for plant in plants:
            log_watering_time(plant.name, plant.latest_watering_duration, time.time())
        
    def __get_sleep_time(self, start_time_ns):
        end_time = time.time_ns()
        duration_ns = end_time - start_time_ns
        time_to_sleep = self.monitor_interval_s - (duration_ns / 1e9)
        time_to_sleep = max(time_to_sleep, 1)
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
            watered_plants = self.water_dry_plants()
            self.log_watering_durations(watered_plants)
            self.wdt.feed()
            
            time_to_sleep = self.__get_sleep_time(start_time_ns)
            self.led.off()
            print(f"Sleeping for {time_to_sleep} when next cycle should start.")
            time.sleep(time_to_sleep)
