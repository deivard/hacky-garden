import network
import time
from config.config import TIME_OFFSET_S

def connect_to_wifi(ssid, key):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        start_time = time.time()
        wlan.connect(ssid, key)
        while not wlan.isconnected():
            if time.time() - start_time > 10:
                print(f"Could not connect to network {ssid}, timed out.")
                return
    print('network config:', wlan.ifconfig())
    sync_clock()
    print(f"Updated RTC via NTP: Current time is {time.localtime(time.time() + TIME_OFFSET_S)}")
    
def sync_clock():
    import ntptime
    ntptime.settime()

def is_connected():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    return wlan.isconnected()
