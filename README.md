# Hacky Garden
### **Moisture level monitoring and automated watering.**

Note to self so I remember how to run this in a few years when I revisit it:

1. Connect the things with the stuff so it works.
2. Install micropython firmware.
3. Create a config.py file in `src/config` based on the `config_example.py`.
4. Configure the config file.
5. Copy the src folder to the device. You can use [ampy](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy) to do this:

        ampy --port COM3 put src

6. Configure the `main.py` located in the root directory. Create some `SmartPumps`, put theM in the `IrrigationSystem` and call start monitoring, maybe. 7. Upload you `main.py` file to the microcontroller (tested on ESP32) and restart. It will now run every time you start the microcontroller.


Note: 
I used influxdb v1.8 since I host it on a Raspberry Pi with a 32 bit OS that does not support InfluxDB v2.0+. Don't know if the logger will work for v2.0+. :)