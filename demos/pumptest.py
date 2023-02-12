from machine import Pin
import time

p0 = Pin(33, Pin.OUT)

for i in range(9):
    p0.value(int(not p0.value()))
    time.sleep(2)
    
p0.value(1)