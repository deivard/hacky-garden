from src.devices.pump import Pump

p = Pump(33)

while True:
    on_off = input("(a)ctivate or (o)ff?")
    if on_off.strip().lower() == "a":
        p.on()
    else:
        p.off()