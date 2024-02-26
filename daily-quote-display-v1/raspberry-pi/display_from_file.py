"""
Hardware
"""
import time
import random
from dotenv import load_dotenv
import RPi.GPIO as GPIO
import logging

hardware_module = None

# Configurable
data_file = "quotes.csv"

# When button will refresh the quote immediately, rather than at interval.
BUTTON_PIN = 26

# Define properties for the DISPLAY.
# For 4.2", about 50 characters per line at Font15 works OK.
max_chars = 50

# 180 = refresh automatically every 180 sec (3 minutes)
refresh_interval = 180

# Internal variables
previous_time = 0
quote_list = []


def button_callback(channel):
    # rather than calling to redraw, set previous_time to 0
    # which will trigger redrawing by loop() function
    global previous_time
    previous_time = 0
    logging.info(f"PIN {BUTTON_PIN} Pressed")


def setup_data():
    global quote_list

    logging.info(f"Loading from {data_file}")

    # df = pd.read_csv(data_file)
    with open(data_file, "r") as f:
        lines = f.readlines()
    quote_list = [line.rstrip() for line in lines]

    logging.info(f"Loaded {len(quote_list)}")


def setup_GPIO():
    """Setup GPIO pins"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Add event detection on the BUTTON_PIN, falling edge.
    GPIO.add_event_detect(
        BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=1000
    )


def setup():
    """Reads environment variables and loads quotes from CSV."""
    setup_data()

    setup_GPIO()


def convert_to_multiline_array(text, max_chars_per_line) -> list:
    lines = []
    line = ""

    for word in text.split():
        if len(line + word) <= max_chars_per_line:
            line += word + " "
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)  # add any remaining text

    return lines


def display_random_quote():
    """Displays the given quote on the Waveshare 4in2 display."""
    # Assuming waveshare_4in2 library has a method to display text
    # waveshare_4in2.display_text(quote)
    # print(quote)
    quote = random.choice(quote_list)
    logging.debug(quote)

    # Convert long string into an array, since display hardware cannot
    # do automatic word wrap.
    lines = convert_to_multiline_array(quote, max_chars)
    hardware_module.display_data(lines, start_x=10, start_y=10, y_inc=21)


def loop():
    """main loop with interval checking"""
    global previous_time
    current_time = time.time()
    if current_time - previous_time >= refresh_interval:
        previous_time = current_time
        try:
            display_random_quote()
        except Exception as e:
            print("Error occurred:", e)


def set_hardware_module(module):
    global hardware_module
    hardware_module = module
