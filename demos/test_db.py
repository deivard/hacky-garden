import urequests as requests

def connect_to_wifi(ssid, key):
    import network
    import time
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

def test_net():
    import urequests 
    from machine import Pin
    from time import sleep
    led = Pin(2, Pin.OUT)
    while True:
        # response = urequests.get('https://www.google.com')
        response = urequests.post('https://httpbin.org/post', data="asd")
        if response.status_code == 199:        
            led.value(not led.value())
        sleep(4)

connect_to_wifi("Mainframe","5gBOMBq1337")
test_net()

requests.post(
    "http://192.168.50.99:8086/write?db=home",
    headers={'content-type': 'text/plain'},
    data=f"plants,plant_name=test moisture=0.0"
)