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
    
