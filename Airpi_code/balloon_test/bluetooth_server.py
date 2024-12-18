# bluetooth_server.py
import bluetooth
import threading
import time
# import signal
# import sys
import helpers.gpio_helpers as gh # running is a shared state
# import logging

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

print("Bluetooth_server begins running")

connection_established = False
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
client_socket = None
recv_socket = None

with open("/home/pi/Documents/balloon_test/connection_status.txt", "w") as f:
    f.write("True" if connection_established else "False")


server_socket.bind(("", 1))
server_socket.listen(1)

try:
    while True:
        print("Raspberry Pi 4 Server: Waiting for connection...")

        try:
            recv_socket, recv_info = server_socket.accept()
            print(f"Raspberry Pi 4: Connection accepted from {recv_info}")
            connection_established = True
            break
        except bluetooth.btcommon.BluetoothError as e:
            print(f"Accept error: {e}, retrying...")
            time.sleep(1)

except KeyboardInterrupt:
    gh.running = False
    print("Interrupted before connection was established.")

if connection_established:
    client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    client_socket.connect((recv_info[0], 2))
    print("Raspberry Pi 4: Connected to client on Pi 0 for sending.")
    with open("/home/pi/Documents/balloon_test/connection_status.txt", "w") as f:
        f.write("True" if connection_established else "False")

    def send_data():
        while True:
            try:
                with open("/home/pi/Documents/balloon_test/user_data.txt", "r") as f:
                    line = f.read().strip()
                    if line:
                        parts = line.split(",")
                        state_counter = int(parts[0])
                        paused = parts[1].lower() in ['true', '1', 'yes']
                        send_message = f"{state_counter},{paused}".encode('utf-8')
                        client_socket.send(send_message)
            except (FileNotFoundError, ValueError):
                pass
            except bluetooth.btcommon.BluetoothError:
                # If send fails due to closed socket
                time.sleep(1)
            time.sleep(1)

    def receive_data():
        while True:
            try:
                data = recv_socket.recv(1024)
                data = data.decode('utf-8')
                print("RPi 4 Received " + data)
                parts = data.split(",")
                temp_part = parts[0].split(":")[1].strip()
                humid_part = parts[1].split(":")[1].strip()
                altitude_part = parts[2].split(":")[1].strip()

                if temp_part != 'N/A' and humid_part != 'N/A':
                    temperature_value = float(temp_part.replace("C", ""))
                    humid_value = float(humid_part.replace("%", ""))
                else:
                    temperature_value = 'N/A'
                    humid_value = 'N/A'

                altitude_value = float(altitude_part.replace("in", ""))

                with open("/home/pi/Documents/balloon_test/sensor_data.txt", "w") as f:
                    f.write(f"{temperature_value},{humid_value},{altitude_value}\n")
            except bluetooth.btcommon.BluetoothError as g:
                # Socket closed or error caused by termination
                print(f"Bluetooth error occurred: {g}")
                pass
            except Exception as e:
                print(f"Raspberry Pi 4 Receive Error: {e}")
                pass

    send_thread = threading.Thread(target=send_data)
    recv_thread = threading.Thread(target=receive_data)

    send_thread.start()
    recv_thread.start()

    send_thread.join()
    recv_thread.join()

    if client_socket:
        client_socket.close()
    if recv_socket:
        recv_socket.close()

try:
    server_socket.close()
except:
    pass

print("Bluetooth server shutdown complete.")
