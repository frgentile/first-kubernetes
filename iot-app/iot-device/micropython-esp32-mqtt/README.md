# Micropython ESP32 MQTT Project

This project demonstrates how to use MicroPython on an ESP32 to connect to an MQTT broker using the Mosquitto protocol. It includes the necessary files to set up the ESP32, connect to Wi-Fi, and interact with the MQTT broker.

## Project Structure

```
micropython-esp32-mqtt
├── upython-repl         # Micropython Binaries (Choose one)
│   ├── ESP32_GENERIC-20241129-v1.24.1.bin
│   ├── ESP32_GENERIC-OTA-20241129-v1.24.1.bin
│   └── ESP32_GENERIC-SPIRAM-20241129-v1.24.1.bin
├── main.py              # Main entry point of the application
├── boot.py              # Startup configuration for the ESP32
├── config.py            # Configuration settings for MQTT
├── libs
│   └── umqtt
│       ├── simple.py    # MQTT client implementation
│       └── robust.py    # MQTT client implementation
└── README.md            # Project documentation
```

## Setup Instructions

1. **Install MicroPython on ESP32**: Follow the official MicroPython documentation to flash MicroPython firmware onto your [ESP32](https://micropython.org/download/ESP32_GENERIC/) or follow this steps:
    1. Located where this README.md file is, create a Python virtual environment: `python3 -m venv .venv`
    2. Activate it: `source .venv/bin/activate`
    3. Update pip: `pip install -U pip`
    4. Install *esptool* and *ampy*: `pip install esptool adafruit-ampy`
    5. Let's suppose `/dev/ttyUSB0` is the port connected to ESP32 board: `esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash`
    6. Write the uPython interpreter to the board, here I choose `ESP32_GENERIC-20241129-v1.24.1.bin` but can be anyone of those in `upython-repl` dir: `esptool.py --baud 460800 write_flash 0x1000 upython-repl/ESP32_GENERIC-20241129-v1.24.1.bin`

CONTINUAR DESDE AQUI
2. **Configure Wi-Fi and MQTT Settings**:
   - Open `config.py` and set the following parameters:
     - `WIFI_SSID`: Your Wi-Fi network name
     - `WIFI_PASSWORD`: Your Wi-Fi password
     - `MQTT_BROKER`: The address of your MQTT broker
     - `MQTT_PORT`: The port number (usually 1883)
     - `MQTT_USERNAME`: Your MQTT username (if required)
     - `MQTT_PASSWORD`: Your MQTT password (if required)

3. **Upload Files**: Use a tool like `ampy` or `rshell` to upload the project files to your ESP32. Follow these steps with ampy:
    1. Upload MQTT libraries: 
        1. `ampy --port /dev/ttyUSB0 mkdir /libs`
        2. `ampy --port /dev/ttyUSB0 mkdir /libs/umqtt`
        3. `ampy --port /dev/ttyUSB0 put libs/umqtt/simple.py /libs/umqtt/simple.py`
        4. `ampy --port /dev/ttyUSB0 put libs/umqtt/robust.py /libs/umqtt/robust.py`
    2. Upload application files:
        1. `ampy --port /dev/ttyUSB0 put boot.py`
        1. `ampy --port /dev/ttyUSB0 put main.py`
        1. `ampy --port /dev/ttyUSB0 put config.py`

4. **Run the Application**: After uploading the files and configuring the settings, reset your ESP32. The `boot.py` will run automatically, connecting to Wi-Fi, and then `main.py` will execute, connecting to the MQTT broker.

## Usage Examples

- **Publishing Messages**: Use the `mqtt.publish(topic, message)` function from `lib/mqtt.py` to send messages to a specific topic.
- **Subscribing to Topics**: Use the `mqtt.subscribe(topic)` function to listen for messages on a specific topic.

## Troubleshooting

- Ensure that your ESP32 is connected to the Wi-Fi network.
- Check the MQTT broker address and credentials in `config.py`.
- Monitor the serial output for any error messages during connection attempts.

## License

This project is licensed under the MIT License.