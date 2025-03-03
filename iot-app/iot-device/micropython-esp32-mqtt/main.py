import network
import time
import json
from libs.umqtt.robust import MQTTClient
import config
import ntptime
import machine


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

    while not wlan.isconnected():
        print("Connecting to WiFi...")
        time.sleep(1)

    print("Connected to WiFi:", wlan.ifconfig())

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe(config.COMMANDS_TOPIC)

def on_message(topic, msg):
    print("Received message on topic {}: {}".format(topic, msg.decode()))

def sync_time():
    count = 10
    while count > 0:
        try:
            ntptime.host = 'ar.pool.ntp.org'  # Specify the NTP server
            ntptime.settime()
            rtc = machine.RTC()
            # Adjust the time for your timezone, e.g., UTC+2
            current_time = list(rtc.datetime())
            current_time[4] -= 3  # Adjust the hour for timezone
            rtc.datetime(tuple(current_time))
            print("Time synchronized with NTP server")
            count = 0
        except Exception as e:
            print("Failed to synchronize time:", e)
            time.sleep(1)
            count -= 1

def read_temperature_sensor():
    # Replace with actual temperature sensor reading code
    return 25.0

def main():
    connect_wifi()
    sync_time()

    client = MQTTClient(client_id=config.CLIENT_ID, server=config.BROKER_ADDRESS, user=config.BROKER_USER, password=config.BROKER_PASSWORD)
    client.set_callback(on_message)
    client.connect()

    client.subscribe(config.COMMANDS_TOPIC)
    print("Subscribed to topic:", config.COMMANDS_TOPIC)

    last_sensor_read_time = time.ticks_ms()

    try:
        while True:
            client.check_msg()
            current_time = time.ticks_ms()
            if time.ticks_diff(current_time, last_sensor_read_time) >= config.SENSOR_SENDING_INTERVAL_MS:
                sensor_value = read_temperature_sensor()
                if sensor_value is not None:
                    print("Sending sensor value:", sensor_value)
                    rtc = machine.RTC()
                    now = rtc.datetime()
                    ts = f"{now[0]}-{now[1]:02d}-{now[2]:02d} {now[4]:02d}:{now[5]:02d}:{now[6]:02d}"
                    payload = {
                        "device": config.DEVICE_NAME,
                        "ts": ts,
                        "temp": sensor_value
                    }
                    client.publish(config.DATA_TOPIC, json.dumps(payload))
                last_sensor_read_time = current_time
            time.sleep(1)
    except KeyboardInterrupt:
        print("Disconnecting from MQTT broker...")
        client.disconnect()

if __name__ == "__main__":
    main()