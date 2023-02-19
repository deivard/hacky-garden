import os
# Change into the src directory if this script is run outside of it
# (so the config file import works - relative import did not work for some reason?)
if "src" in os.listdir():
    os.chdir("src")

from irrigationsystem import IrrigationSystem
from smartplant import SmartPlant
from connections import connect_to_wifi
import config


def main():
    connect_to_wifi(config.SSID, config.WIFI_PASSWORD)
    
    smart_plants = [
        SmartPlant("plant_1",
                   pump_pin=33,
                   moisture_sensor_pin=34,
                   dry_reference=3600,
                   wet_reference=2900,
                   dry_treshold=30,
                   filter_window_size=config.MOVING_AVERAGE_WINDOW_SIZE),
        SmartPlant("plant_2",
                   pump_pin=32,
                   moisture_sensor_pin=35,
                   dry_reference=3600,
                   wet_reference=2900,
                   dry_treshold=30,
                   filter_window_size=config.MOVING_AVERAGE_WINDOW_SIZE),
    ]
    
    irrigation_system = IrrigationSystem(smart_plants,
                                         monitor_interval_seconds=config.MONITOR_INTERVAL_S,
                                         watering_cooldown_seconds= 60*10,
                                         watering_duration=config.WATERING_DURATION_S)
    irrigation_system.start_monitoring()
    

if __name__ == "__main__":
    main()
