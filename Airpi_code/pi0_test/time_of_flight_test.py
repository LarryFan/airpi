import board
import busio
from adafruit_vl6180x import VL6180X

# Initialize I2C and the sensor once
i2c = busio.I2C(board.SCL, board.SDA)
sensor = VL6180X(i2c)

def read_distance():
    """Read the distance from the VL6180X sensor."""
    return sensor.range

if __name__ == "__main__":
    # If you run this file directly, test the sensor reading
    import time
    try:
        while True:
            distance = read_distance()
            print(f"Distance: {distance} mm")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Measurement stopped.")
