import time
import RPi.GPIO as GPIO
from tof2_test import read_distance

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Set for GPIO numbering, not pin numbers...
GPIO.setup(26, GPIO.OUT)  # Set GPIO 26 as output to blink LED
GPIO.setup(25, GPIO.OUT)  # Set GPIO 25 as output to blink LED

freq = 50

pwm = GPIO.PWM(26, freq)  # Pin 26 will generate a PWM pulse
pwm.start(0)

pwm2 = GPIO.PWM(25, freq)  # Pin 25 will generate a PWM pulse
pwm2.start(0)


# Hovering mode control
prevmode = "paused"
distance = 0

def motor_control(mode):
    """
    Control the motor based on the specified mode.
    Modes:
        - "up": Moves motor in forward direction at a fixed duty cycle (e.g., 70%).
        - "down": Moves motor in backward direction at a fixed duty cycle (e.g., 70%).
        - "hover": Keeps motor running in forward direction at a lower duty cycle (e.g., 30%).
        - "paused": Stops the motor.
    """
    global prevmode
    global distance

    if mode != "hover":
        pwm.ChangeFrequency(50)
        pwm2.ChangeFrequency(50)
    
    if mode == "up":
        # Upward direction
        if prevmode != "up":
            prevmode = "up"

        pwm.ChangeDutyCycle(100)  # Duty cycle for upward movement
        pwm2.ChangeDutyCycle(0) 
        print("Motor moving UP")

    elif mode == "down":
        # Downward direction
        if prevmode != "down":
            prevmode = "down"

        pwm.ChangeDutyCycle(0)  # Duty cycle for downward movement
        pwm2.ChangeDutyCycle(100)  
        print("Motor moving DOWN")

    elif mode == "hover":
        # Hover state (low speed forward)
        if prevmode != "hover":
            distance = read_distance()
            prevmode = "hover"
            current_distance = distance 
        else:
            current_distance = read_distance()
        
        difference = current_distance - distance 
        control_signal = difference * 5

        duty_cycle = 50

        frequency = min(max(abs(difference), 1), 500) 
        print("Frequency: " + str(frequency))

        print("Control Signal: " + str(control_signal))
        
        if control_signal > 0:
            pwm.ChangeDutyCycle(0)
            pwm2.ChangeDutyCycle(duty_cycle)
            pwm2.ChangeFrequency(frequency)
        else:
            pwm.ChangeDutyCycle(duty_cycle)
            pwm2.ChangeDutyCycle(0)
            pwm.ChangeFrequency(frequency)
        
        print("Motor in HOVER mode")

    elif mode == "paused":
        if prevmode != "paused":
            prevmode = "paused"

        pwm.ChangeDutyCycle(0)  # Stop Green
        pwm2.ChangeDutyCycle(0)  # Stop Red
        print("Motor PAUSED")

def cleanup_gpio():
    global pwm
    global pwm2 
    pwm.stop()
    pwm2.stop()
    GPIO.cleanup()

# pwm.stop()
# GPIO.cleanup()