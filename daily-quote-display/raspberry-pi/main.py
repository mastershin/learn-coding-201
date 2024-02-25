import sys
import importlib
import RPi.GPIO as GPIO
import time

# Define the intervals (in seconds)
interval1 = 0.01  # Function 1 interval
interval2 = 5  # Function 2 interval

# Initialize previous time for each function
prev_time = 0


def main():
    global prev_time
    if len(sys.argv) < 2:
        print("Usage: main.py <module_name>")
        print("<module_name>: display_quote_epaper4in2")
        sys.exit(1)

    module_name = sys.argv[1]  # Get module name from command-line arguments

    # Dynamically import the specified module
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        print(f"Module {module_name} not found.")
        sys.exit(1)

    # call initial user-defined setup() function
    module.setup()

    try:
        while True:
            current_time = time.time()
            # Check if it's time to run user-defined loop()
            if current_time - prev_time >= interval1:
                module.loop()
                prev_time = current_time  # Reset the timer for Function 1

    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
