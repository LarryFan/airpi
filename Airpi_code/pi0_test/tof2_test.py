import qwiic_vl53l1x
import time

ToF = qwiic_vl53l1x.QwiicVL53L1X()
if (ToF.sensor_init() == None):					 # Begin returns 0 on a good init
  print("Sensor online!\n")

def read_distance():
    """Read the distance from the VL6180X sensor."""

    ToF.start_ranging()						 # Write configuration bytes to initiate measurement
    time.sleep(.005)
    distance = ToF.get_distance()	 # Get the result of the measurement from the sensor
    time.sleep(.005)
    ToF.stop_ranging()
    distanceInches = distance / 25.4
    distanceFeet = distanceInches / 12.0

    return distanceInches


if __name__ == "__main__":
    # If you run this file directly, test the sensor reading
    try:
        while True:
            time.sleep(0.5)
            ToF.start_ranging()						 # Write configuration bytes to initiate measurement
            time.sleep(.005)
            distance = ToF.get_distance()	 # Get the result of the measurement from the sensor
            time.sleep(.005)
            ToF.stop_ranging()
            distanceInches = distance / 25.4
            distanceFeet = distanceInches / 12.0
            print("Distance(mm): %s Distance(ft): %s" % (distance, distanceFeet))
    except KeyboardInterrupt:
        print("Measurement stopped.")

