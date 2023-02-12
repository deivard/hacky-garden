from machine import Pin, ADC
import time

sensor = ADC(Pin(15))
sensor.atten(ADC.ATTN_11DB)
pump = Pin(33, Pin.OUT)

water = 360
air = 2300

while True:
    sensor_value = sensor.read()
    print(f"Moisture: {sensor_value}")
    if sensor_value > 1800:
        # if not pump.value():
        pump.value(0)
        print("Turning on pump.")
    elif sensor_value < 1000:
        pump.value(1)
        print("Turning off pump.")

    time.sleep(0.5)