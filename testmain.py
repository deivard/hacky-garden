import os
if "src" in os.listdir():
    os.chdir("src")

from irrigationsystem import IrrigationSystem
from connections import connect_to_wifi
import config
from smartplant import SmartPlant

def main():
    connect_to_wifi(config.SSID, config.WIFI_PASSWORD)
    
    smart_plants = [
        SmartPlant("test_plant_2",
                   pump_pin=33,
                   moisture_sensor_pin=34,
                   dry_reference=4095,
                   wet_reference=2900,
                   dry_treshold=30,
                   filter_window_size=5),
    ]
    
    irrigation_system = IrrigationSystem(smart_plants,
                                         monitor_interval_seconds=config.MONITOR_INTERVAL_S,
                                         watering_duration=0.5)
    irrigation_system.start_monitoring()
    
if __name__ == '__main__':
    main()
