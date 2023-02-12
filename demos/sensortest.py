from machine import Pin, ADC
import time

p = ADC(Pin(15))
p.atten(ADC.ATTN_11DB)

while True:
    print(p.read())
    time.sleep(0.1)