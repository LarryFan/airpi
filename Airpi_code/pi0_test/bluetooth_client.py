import bluetooth
import threading
import time
from temp_test import read_temp_and_humidity
from tof2_test import read_distance
import threading

print("Starting bluetooth_client.py")

server_address = "DC:A6:32:B4:14:43"
CONNECT_TIMEOUT = 180

client_socket = None
server_socket = None
recv_socket = None

# Add a global running flag
running = True
start_send = False
start_receive = False

def connect_client_socket():
    global running
    global start_send
    start_time = time.time()
    while running:
        if time.time() - start_time > CONNECT_TIMEOUT:
            raise TimeoutError("Failed to connect to server within timeout seconds.")
        try:
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((server_address, 1))
            print("Raspberry Pi 0: Connected to server on Pi 4 for sending data.")
            start_send = True
            return sock
        except bluetooth.btcommon.BluetoothError as e:
            if not running:  # Check if we should stop trying
                break
            print(f"Connection error: {e}. Retrying in 5 seconds...")
            time.sleep(5)
    # If we reach here without returning, raise a TimeoutError or just stop
    raise TimeoutError("Stopped attempting to connect due to shutdown.")

def accept_server_connection(sock):
    global running
    global start_receive
    start_time = time.time()
    while running:
        if time.time() - start_time > CONNECT_TIMEOUT:
            raise TimeoutError("No server connection received within timeout seconds.")
        try:
            print("Raspberry Pi 0: Waiting for Pi 4 to connect for receiving...")
            recv, recv_info = sock.accept()
            print(f"Raspberry Pi 0: Connection accepted from {recv_info}")
            start_receive = True
            return recv
        except bluetooth.btcommon.BluetoothError as e:
            if not running:  # Check if we should stop trying
                break
            print(f"Accept error: {e}. Retrying in 5 seconds...")
            time.sleep(5)
    raise TimeoutError("Stopped attempting to accept connection due to shutdown.")

def init_bluetooth_connections():
    global client_socket, server_socket, recv_socket
    client_socket = connect_client_socket()
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_socket.bind(("", 2))
    server_socket.listen(1)
    recv_socket = accept_server_connection(server_socket)

def safe_read_temp_and_humidity(timeout=0.5):
    """Safely read temperature and humidity with a timeout."""
    result = [None, None]

    def read():
        try:
            result[0], result[1] = read_temp_and_humidity()
        except Exception as e:
            print(f"Error reading temp and humidity: {e}")

    thread = threading.Thread(target=read)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        print("Timeout while reading temperature and humidity.")
        return None, None
    return result[0], result[1]

def send_data():
    print("Starting to send data")
    global client_socket, running
    global start_send
    global start_receive
    while running:
        print("Send_Data is running")
        try:
            print("Trying to read temp + humid")
            temperature, humidity = safe_read_temp_and_humidity()
            print("Trying to read distance")
            # temperature, humidity = 23.0, 11
            distance = read_distance()
            print("Successfully read temp, humid, dist")
            if temperature is not None and humidity is not None:
                data_str = f"Temp: {temperature:.1f}C, Humidity: {humidity}%, Altitude: {distance}in"
            else:
                data_str = f"Temp: N/A, Humidity: N/A, Altitude: {distance}in"
            client_socket.send(data_str)
            print(f"Raspberry Pi 0 Sent: {data_str}")
        except bluetooth.btcommon.BluetoothError as e:
            if not running:
                break
            print(f"Send Error: {e}. Retrying connection...")
            client_socket.close()
            if start_send and start_receive:
                running = False
            # If we fail to reconnect and running is False, we'll break out
            if running:
                client_socket = connect_client_socket()
        except Exception as e:
            print(f"Unexpected error during send: {e}")
        time.sleep(1)

def receive_data():
    global recv_socket, running
    while running:
        try:
            data = recv_socket.recv(1024).decode('utf-8')
            if not data:
                break
            with open("/home/pi/Documents/pi0_test/state_data.txt", "w") as file:
                file.write(data + "\n")
            # print(f"Raspberry Pi 0 Received: {data}")
        except bluetooth.btcommon.BluetoothError as e:
            if not running:
                break
            print(f"Receive Error: {e}. Retrying accept...")
            recv_socket.close()
            if start_send and start_receive:
                running = False
            if running:
                recv_socket = accept_server_connection(server_socket)
        except Exception as e:
            print(f"Unexpected error during receive: {e}")
            break
    # Exit loop gracefully when running is False or data ends

def start_bluetooth_threads():
    send_thread = threading.Thread(target=send_data, daemon=True)
    recv_thread = threading.Thread(target=receive_data, daemon=True)

    send_thread.start()
    recv_thread.start()

def stop_running():
    global running
    running = False

def cleanup():
    """Clean up sockets and set running to False so loops end."""
    stop_running()
    if client_socket:
        client_socket.close()
    if recv_socket:
        recv_socket.close()
    if server_socket:
        server_socket.close()
