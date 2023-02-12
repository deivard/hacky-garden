from machine import Pin
import time

p0 = Pin(2, Pin.OUT)

for i in range(10):
    p0.value(int(not p0.value()))
    time.sleep(0.5)
    

