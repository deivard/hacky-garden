from machine import Pin, WDT
import time
wdt = WDT(timeout=5000)

p0 = Pin(33, Pin.OUT, value=1)
p0.value(0)


curr = p0.value()
for i in range(5):
    next_val = not curr
    curr = next_val
    p0.value(int(next_val))
    print(curr)
    time.sleep(1.0)
    wdt.feed()
    
p0.value(1)
print(p0.value())