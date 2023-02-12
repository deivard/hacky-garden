from irrigationsystem import IrrigationSystem
from smartplant import SmartPlant
from connections import connect_to_wifi
import config

def main():
    connect_to_wifi(config.SSID, config.WIFI_PASSWORD)
    
    smart_plants = [
        SmartPlant("citrus_1", 32, 33, 30),
        SmartPlant("citrus_2", 34, 35, 30),
    ]
    
    irrigation_system = IrrigationSystem(smart_plants, 3600)
    irrigation_system.start_monitoring()
    

if __name__ == "__main__":
    main()
