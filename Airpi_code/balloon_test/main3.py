from time import sleep

sleep(30)

import subprocess
import os
import pygame
import pigame
from pygame.locals import *
from helpers.draw_helpers import draw_buttons_and_indicators
from helpers.state_helpers import user_update
import helpers.gpio_helpers as gh  # Import the module, not just 'running'
import logging
import sys


'''
logging.basicConfig(
    filename='/home/pi/Documents/balloon_test/logfile.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

# Redirect print to logging
class PrintLogger:
    def write(self, message):
        if message.strip():  # Avoid logging empty lines
            logging.info(message.strip())

    def flush(self):  # Required for compatibility
        pass

sys.stdout = PrintLogger()
sys.stderr = PrintLogger() 

'''




os.putenv('SDL_VIDEODRV','fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV','dummy')
os.putenv('SDL_MOUSEDEV','/dev/null')
os.putenv('DISPLAY','')


# Use the absolute path to the Bluetooth server script
server_script_path = "/home/pi/Documents/balloon_test/bluetooth_server.py"

# Start the Bluetooth server as a separate process
server_process = subprocess.Popen(["python3", server_script_path])

sleep(1)

GPIO = gh.initialize_gpio()
pygame.init()
pitft = pigame.PiTft()
pygame.mouse.set_visible(False)

size = width, height = 320, 240
screen = pygame.display.set_mode(size)
font_big = pygame.font.Font(None, 38)
font_small = pygame.font.Font(None, 28)

state_counter = 0
altitude = 0.0
temperature = 0
humidity = 0
time_counter = 0.0
active_counter = 0.0
paused = True

def is_connection_established():
    try:
        with open("/home/pi/Documents/balloon_test/connection_status.txt", "r") as f:
            status = f.read().strip()
            return status == "True"
    except FileNotFoundError:
        return False

with open("/home/pi/Documents/balloon_test/user_data.txt", "w") as f:
    f.write(f"{state_counter},{paused}\n")

connection_established = is_connection_established()

draw_buttons_and_indicators(screen, font_big, font_small, state_counter, altitude, temperature, humidity, time_counter, paused, connection_established)

while True:
    # Now check gh.running instead of running
    # print(gh.running)
    if not gh.running:
        break

    pitft.update()

    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            state_counter, paused = user_update(x, y, state_counter, paused)
            with open("/home/pi/Documents/balloon_test/user_data.txt", "w") as f:
                f.write(f"{state_counter},{paused}\n")

    try:
        with open("/home/pi/Documents/balloon_test/sensor_data.txt", "r") as f:
            line = f.read().strip()
            # print(line)
            parts = line.split(",")
            if parts[0] != 'N/A':
                temperature = float(parts[0])
            if parts[1] != 'N/A':
                humidity = float(parts[1])
            if parts[2] != 'N/A':
                altitude = float(parts[2])
    except (FileNotFoundError, ValueError):
        pass

    connection_established = is_connection_established()

    draw_buttons_and_indicators(screen, font_big, font_small, state_counter, altitude, temperature, humidity, active_counter, paused, connection_established)

    if not paused:
        active_counter += 0.2

    time_counter += 0.2
    if time_counter > 180:
        break

    sleep(0.2)

print("Exits While Loop")

gh.cleanup_gpio(GPIO, pitft)
print("Finished GPIO cleanup")

pygame.quit()
print("Quit Pygame")

# server_process.terminate()
server_process.kill()
print("Terminating bluetooth subprocess")

print("End here")
os._exit(0)
