import urequests as requests
from config import config
from connections.wifi import connect_to_wifi, is_connected


def log_moisture_level(plant_name, moisture_level, timestamp):
    if not is_connected:
        connect_to_wifi(config.SSID, config.WIFI_PASSWORD)
    
    epoch_1970_to_2000_delta_ns = int(946681200*1e9)
    timestamp_converted = int(timestamp + epoch_1970_to_2000_delta_ns + int(config.TIME_OFFSET_S*1e9))
    line = f"plants,plant_name={plant_name} moisture={moisture_level} {timestamp_converted}"
    print(f"Sending to database: {line}")
    
    requests.post(
        f"{config.DB_URL}/write?db={config.DB_BUCKET}&precision=ns",
        headers={'content-type': 'text/plain'},
        data=line
    )
