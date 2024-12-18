import RPi.GPIO as GPIO

running = True

def initialize_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    def GPIO27_callback(channel):
        global running
        print("Button 27 pressed!")
        running = False
    GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=300)
    return GPIO

def cleanup_gpio(GPIO, pitft):
    GPIO.cleanup()
    del pitft
