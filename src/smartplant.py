from devices import Pump, MoistureSensor
import time
from filters import MovingAverage, Clamp
import btree


class SmartPlant:
    def __init__(self,
                 name: str,
                 pump_pin: int,
                 moisture_sensor_pin: int,
                 dry_reference: int = 4095,
                 wet_reference: int = 3000,
                 dry_treshold: int = 30,
                 watered_threshold: int = 70,
                 filter_window_size: int = 10,
                 watering_time: int = 1):
        self.name = name
        self.pump = Pump(pump_pin)
        self.moisture_sensor = MoistureSensor(moisture_sensor_pin,
                                              dry_reference,
                                              wet_reference)
        self.latest_watering_time = None
        self.__filters = [
            Clamp(0, 100),
            MovingAverage(window_size=filter_window_size)
        ]
        self.latest_moisture_level = None
        self.latest_raw_sensor_value = None
        self.latest_reading_timestamp_ns = None
        self.watering_time = watering_time
        self.dry_treshold = dry_treshold
        self.watered_threshold = watered_threshold
        self.watering_cycle_active = False
        self.water_on_timestamp_ns = 0
        self.latest_watering_duration = 0
        self.restore_watering_cycle_state()
        
    def restore_watering_cycle_state(self):
        try:
            f = open("smartplantdb", "r+b")
        except OSError:
            f = open("smartplantdb", "w+b")
        db = btree.open(f)
        self.watering_cycle_active = (
            False if (db.get(self.name, b"False")) == b"False" else True
        )
        print(f"Restored watering cycle state for {self.name}, current state is {self.watering_cycle_active}")
        db.close()
        f.close()
        
    def store_watering_cycle_state(self):
        try:
            f = open("smartplantdb", "r+b")
        except OSError:
            f = open("smartplantdb", "w+b")
        db = btree.open(f)
        db[self.name] = str(self.watering_cycle_active).encode("utf-8")
        db.flush()
        db.close()
        f.close()
        
    
    def filter_value(self, value):
        filtered = value
        for filter_ in self.__filters:
            filtered = filter_(filtered) 
        return filtered

    def update_moisture_level(self):
        unfiltered_percent, raw = self.moisture_sensor.read_percent_and_raw()
        filtered = self.filter_value(unfiltered_percent)
        print(f"{self.name} - Unfiltered moisture level: {unfiltered_percent}%. Filtered: {filtered}")
        print(f"\t Last {len(self.__filters[-1].__window)} readings: {self.__filters[-1].__window}")
        self.latest_moisture_level = filtered
        self.latest_raw_sensor_value = raw
        self.latest_reading_timestamp_ns = time.time_ns()
        return filtered

    def watering_cycle_should_end(self):
        return self.latest_moisture_level >= self.watered_threshold

    def watering_cycle_should_start(self):
        return self.latest_moisture_level <= self.dry_treshold

    def manage_watering_cycle(self):
        if self.watering_cycle_should_end() and self.watering_cycle_active:
            self.watering_cycle_active = False
            self.store_watering_cycle_state()
            print(f"{self.name} - Ended watering cycle")
        elif self.watering_cycle_should_start() and not self.watering_cycle_active:
            self.watering_cycle_active = True
            self.store_watering_cycle_state()
            print(f"{self.name} - Started watering cycle")

    def needs_watering(self) -> bool:
        self.manage_watering_cycle()
        if self.latest_moisture_level is not None:
            return (self.latest_moisture_level <= self.dry_treshold
                    or self.watering_cycle_active)
        return False

    def water_on(self):
        self.pump.on()
        self.water_on_timestamp_ns = time.time_ns()
        self.latest_watering_time = time.time()
        self.manage_watering_cycle()
    
    def water_off(self):
        self.pump.off()
        self.manage_watering_cycle()
        if self.water_on_timestamp_ns is not None:
            self.latest_watering_duration = time.time_ns() - self.water_on_timestamp_ns
            self.water_on_timestamp_ns = None
    
    def water(self, duration_seconds: int = 1):
        self.pump.on()
        self.latest_watering_time = time.time()
        time.sleep(duration_seconds)
        self.pump.off()
        self.manage_watering_cycle()