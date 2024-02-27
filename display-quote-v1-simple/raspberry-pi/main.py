import sys
import importlib
import RPi.GPIO as GPIO
import time
import logging
import display_from_file as display_module

# Define the intervals (in seconds)
interval1 = 0.01  # Function 1 interval
interval2 = 5  # Function 2 interval

# Initialize previous time for each function
prev_time = 0


def main():
    global prev_time

    if len(sys.argv) < 2:
        print("Usage: main.py <hardware>")
        print("<hardware>: console, epaper4in2")
        sys.exit(1)

    # Dynamically import hardware module
    hardware_module_name = "hardware_" + sys.argv[1]

    # Dynamically import the specified module
    try:
        logging.info(f"Loading module: {hardware_module_name}")
        hardware_module = importlib.import_module(hardware_module_name)
    except ImportError:
        print(f"Module {hardware_module_name} not found.")
        sys.exit(1)

    display_module.set_hardware_module(hardware_module)

    # call initial user-defined setup() function
    display_module.setup()

    try:
        while True:
            current_time = time.time()
            # Check if it's time to run user-defined loop()
            if current_time - prev_time >= interval1:
                display_module.loop()
                prev_time = current_time  # Reset the timer for Function 1

    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
