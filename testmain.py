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
        SmartPlant("citrus_1", 32, 34, 30),
        SmartPlant("citrus_2", 33, 35, 30),
    ]
    
    irrigation_system = IrrigationSystem(smart_plants, 5)
    irrigation_system.start_monitoring()
    
if __name__ == '__main__':
    main()