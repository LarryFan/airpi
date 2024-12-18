import time

time.sleep(30)

import os
import threading
import bluetooth_client as bt
from bluetooth_client import init_bluetooth_connections, start_bluetooth_threads, cleanup
print("Finished importing bluetooth_client")
from motor_control import motor_control, cleanup_gpio

# Flags and state variables
global_state_counter = 0
paused = True

# Thread-safe lock
state_lock = threading.Lock()

def receive_data_wrapper():
    """Wrapper for receiving Bluetooth data to update global state."""
    global global_state_counter, paused

    while True:
        try:
            with open("/home/pi/Documents/pi0_test/state_data.txt", "r") as f:
                contents = f.read().strip()
                if contents:
                    state_counter, paused_str = contents.split(',')

                    # Convert back to appropriate types
                    local_state_counter = int(state_counter)
                    local_paused = (paused_str.lower() == 'true')

                    with state_lock:
                        global_state_counter = local_state_counter
                        paused = local_paused

                    # print(f"Updated global state: state_counter={global_state_counter}, paused={paused}")
        except FileNotFoundError:
            pass
        except ValueError:
            pass
        except Exception as e:
            print(f"Receive data error: {e}")
            break

        time.sleep(1)  # Prevent tight looping if file doesn't change

def motor_handler():
    """Handle motor control based on the global state."""
    global global_state_counter, paused
    local_state_counter = global_state_counter
    local_paused = paused
    print("Start motor handler")

    while True:
        # print("Setting Motor Handler")

        if local_state_counter != global_state_counter or local_paused != paused:
            with state_lock:
                local_state_counter = global_state_counter
                local_paused = paused
            if local_paused:
                motor_control("paused")
            elif local_state_counter % 3 == 0:
                motor_control("hover")
            elif local_state_counter % 3 == 1:
                motor_control("up")
            elif local_state_counter % 3 == 2:
                motor_control("down")
        elif local_state_counter % 3 == 0 and not local_paused:
            motor_control("hover")

        time.sleep(1)  # Adjust as necessary

def main():
    """Main function to start the threads."""
    print("Initialize bluetooth connections")
    start_time = time.time()

    try:
        init_bluetooth_connections()
    except TimeoutError as te:
        print(te)
        print("Exiting program due to timeout.")
        return  # Exit gracefully if connection times out


    print("Initialize bluetooth threads")
    start_bluetooth_threads()

    # Start other threads if needed
    print("Initialize state reading thread")
    state_thread = threading.Thread(target=receive_data_wrapper)
    state_thread.start()

    print("Initialize motor thread")
    motor_thread = threading.Thread(target=motor_handler)
    motor_thread.start()

    print("Successfully started all threads")

    # Wait for timeout seconds after everything starts, then exit
    while True:
        elapsed = time.time() - start_time
        if elapsed > bt.CONNECT_TIMEOUT or not bt.running:
            print(bt.running)
            break
        time.sleep(2)
        
    # Timeout reached
    print("Timeout reached during runtime. Terminating now.")

    cleanup_gpio()
    print("Finished GPIO cleanup")

    cleanup()  # This will set running = False and close sockets
    print("Resources cleaned up. Exiting now.")
    # No more attempts to reconnect will be made, threads will exit.
    os._exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Main program stopped by user.")
        cleanup()
        print("Resources cleaned up. Exiting now.")
        
