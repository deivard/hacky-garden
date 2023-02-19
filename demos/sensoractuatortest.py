from machine import Pin, ADC
import time

sensor = ADC(Pin(33))
sensor.atten(ADC.ATTN_11DB)
pump = Pin(32, Pin.OUT)

water = 3000
air = 4095

while True:
    sensor_value = sensor.read()
    print(f"Moisture: {sensor_value}")
    if sensor_value > 1800:
        # if not pump.value():
        pump.value(0)
        print("Turning on pump for 1 second.")
        time.sleep(1)
        pump.value(1)
    elif sensor_value < 1000:
        pump.value(1)
        print("Moist enough, not turning on pump.")

    time.sleep(2)