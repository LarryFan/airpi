import adafruit_dht
import board

# Initialize the DHT sensor once
dht_device = adafruit_dht.DHT11(board.D17)

def read_temp_and_humidity():
    """Read the temperature and humidity from the DHT11 sensor."""
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        return temperature, humidity
    except RuntimeError as error:
        # This happens occasionally due to sensor timing, just return None
        print(f"DHT reading error: {error}")
        return None, None

if __name__ == "__main__":
    # If you run this file directly, test the sensor reading
    import time
    try:
        while True:
            temperature, humidity = read_temp_and_humidity()
            if temperature is not None and humidity is not None:
                print(f"Temp: {temperature:.1f} °C    Humidity: {humidity:.1f} %")
            else:
                print("Failed to read data from DHT sensor.")
            time.sleep(2.0)
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        dht_device.exit()
