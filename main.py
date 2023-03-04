import os
# Change into the src directory if this script is run outside of it
# (so the config file import works - relative import did not work for some reason?)
if "src" in os.listdir():
    os.chdir("src")

from irrigationsystem import IrrigationSystem
from smartplant import SmartPlant
from connections import connect_to_wifi
from logger import log_boot_time
import time
import config
import btree

def remove_inactive_plants_from_db(plants):
    try:
        f = open("smartplantdb", "r+b")
    except OSError:
        f = open("smartplantdb", "w+b")
    db = btree.open(f)
    names = [plant.name for plant in plants]
    for key in db.keys():
        if key.decode("utf-8") not in names:
            del db[b"" + key]
    db.flush()
    db.close()
    f.close()

def main():
    if config.SSID is not None:
        connect_to_wifi(config.SSID, config.WIFI_PASSWORD)
    if config.LOGGING_ENABLED:
        log_boot_time(config.DEVICE_NAME, time.time())
    
    smart_plants = [
        SmartPlant("plant_1",
                   pump_pin=33,
                   moisture_sensor_pin=34,
                   dry_reference=4000,
                   wet_reference=2900,
                   dry_treshold=20,
                   watered_threshold=70,
                   filter_window_size=config.MOVING_AVERAGE_WINDOW_SIZE,
                   watering_time=5),
        SmartPlant("plant_2",
                   pump_pin=32,
                   moisture_sensor_pin=35,
                   dry_reference=4000,
                   wet_reference=2900,
                   dry_treshold=20,
                   watered_threshold=70,
                   filter_window_size=config.MOVING_AVERAGE_WINDOW_SIZE,
                   watering_time=5)
    ]
    
    remove_inactive_plants_from_db(smart_plants)
    
    irrigation_system = IrrigationSystem(smart_plants,
                                         monitor_interval_seconds=config.MONITOR_INTERVAL_S,
                                         watering_cooldown_seconds=config.WATERING_COOLDOWN_S,
                                         logging_enabled=config.LOGGING_ENABLED)
    irrigation_system.start_monitoring()
    

if __name__ == "__main__":
    main()
