import urequests as requests
from config import config
from connections.wifi import connect_to_wifi, is_connected

EPOCH_1970_TO_2000_DELTA_NS = int(946681200*1e9)
EPOCH_1970_TO_2000_DELTA_S = 946681200

def log_moisture_level(plant_name, moisture_level, timestamp):
    if not is_connected():
        connect_to_wifi(config.SSID, config.WIFI_PASSWORD)
    
    timestamp_converted = int(timestamp + EPOCH_1970_TO_2000_DELTA_NS + int(config.TIME_OFFSET_S*1e9))
    line = f"plants,plant_name={plant_name} moisture={moisture_level} {timestamp_converted}"
    print(f"Sending to database: {line}")
    requests.post(
        f"{config.DB_URL}/write?db={config.DB_BUCKET}&precision=ns",
        headers={'content-type': 'text/plain'},
        data=line
    )


def log_raw_sensor_value(plant_name, sensor_value, timestamp):
    if not is_connected():
        connect_to_wifi(config.SSID, config.WIFI_PASSWORD)
    
    timestamp_converted = int(timestamp + EPOCH_1970_TO_2000_DELTA_NS + int(config.TIME_OFFSET_S*1e9))
    line = f"plants,plant_name={plant_name} sensor_value={sensor_value} {timestamp_converted}"
    print(f"Sending to database: {line}")
    requests.post(
        f"{config.DB_URL}/write?db={config.DB_BUCKET}&precision=ns",
        headers={'content-type': 'text/plain'},
        data=line
    )


def log_boot_time(device_id, timestamp):
    if not is_connected():
        connect_to_wifi(config.SSID, config.WIFI_PASSWORD)
    
    timestamp_converted = int(timestamp + EPOCH_1970_TO_2000_DELTA_S + config.TIME_OFFSET_S)
    line = f"boot_times,device_id={device_id} state=1 {timestamp_converted}"
    print(f"Sending to database: {line}")
    requests.post(
        f"{config.DB_URL}/write?db={config.DB_BUCKET}&precision=s",
        headers={'content-type': 'text/plain'},
        data=line
    )

def log_watering_time(plant_name, duration, timestamp):
    if not is_connected():
        connect_to_wifi(config.SSID, config.WIFI_PASSWORD)
    
    timestamp_converted = int(timestamp + EPOCH_1970_TO_2000_DELTA_S + config.TIME_OFFSET_S)
    line = f"watered,device_id={plant_name} duration={duration} {timestamp_converted}"
    print(f"Sending to database: {line}")
    requests.post(
        f"{config.DB_URL}/write?db={config.DB_BUCKET}&precision=s",
        headers={'content-type': 'text/plain'},
        data=line
    )
    