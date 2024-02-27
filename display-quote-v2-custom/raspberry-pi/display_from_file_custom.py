"""
Using DATA_FILE from either environment variable or .env file, reads csv and do some additional processing.
For this example, this loads bible-quotes.csv, which contains LLM scraped Bible quotes and commentaries,
which is not always well-formed string.  Hence, we have to cleanup_text() to extract correct strings.
"""
import os
import pandas as pd
import time
import random
import re
import numpy as np
from dotenv import load_dotenv
import RPi.GPIO as GPIO
import logging

hardware_module = None

# When button will refresh the quote immediately, rather than at interval.
BUTTON_PIN = 26

# Define properties for the DISPLAY.
# For 4.2", about 55 characters per line at Font15 works OK.
max_chars = 55

# 180 = refresh automatically every 180 sec (3 minutes)
refresh_interval = 180

# Internal variables
previous_time = 0
df = None


def button_callback(channel):
    # rather than calling to redraw, set previous_time to 0
    # which will trigger redrawing by loop() function
    global previous_time
    previous_time = 0
    logging.info(f"PIN {BUTTON_PIN} pressed")


def setup_data():
    global df

    load_dotenv()
    data_file = os.environ["DATA_FILE"]

    if not data_file:
        raise ValueError("DATA_FILE environment variable not set")

    logging.info(f"Loading from {data_file}")

    # df = pd.read_csv(data_file)
    with open(data_file, "r") as f:
        lines = f.readlines()
    lines = [line.rstrip() for line in lines]
    df = pd.DataFrame({"data": lines})

    logging.info(f"Loaded {len(df)}")


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


def cleanup_text(text) -> str:
    """
    Cleanup a text string and extracts quotes and commentaries.
    This is necessary if text contains "noisy" strings, remove
    certain portions, etc.

    Args:
      text: The text string to parse.

    Returns:
      A string containing the concatenated quotes and commentaries,
      separated by newlines.
    """

    quotes = []
    commentaries = []

    line = text

    # line = re.sub(r'^[\s\n]"]+', '', line, flags=re.MULTILINE)
    # line = re.sub(r'[\s"]+$', '', line, flags=re.MULTILINE)
    line = re.sub(r'\\"', '"', line, flags=re.MULTILINE)
    line = re.sub(r"(\\n)+", "\n", line, flags=re.MULTILINE)
    line = re.sub(r"\\", "", line, flags=re.MULTILINE)
    line = re.sub(r'"', "", line, flags=re.MULTILINE)

    quote_match = re.search(r"Quote: (.*)Commentary.*", line, flags=re.DOTALL)
    commentary_match = re.search(r"Commentary: (.*?)Keywords.*$", line, flags=re.DOTALL)
    if quote_match:
        quotes.append(quote_match.group(1))
    if commentary_match:
        commentaries.append(commentary_match.group(1))

    if len(quotes) == 0 or len(commentaries) == 0:
        return None

    # Replace newline characters with spaces
    quote = quotes[0]
    commentary = commentaries[0]

    final = f"Quote: {quote}\n\nCommentary: {commentary}"
    final = final.replace("\\n", "\n")
    final += "\n"
    return final


def get_random_quote(df) -> str:
    """Returns a random quote from an array."""
    is_valid = False
    invalid_counter = 0
    while not is_valid:
        random_row = df.iloc[np.random.randint(0, len(df))]
        quote = random_row[0]
        quote = cleanup_text(quote)
        if quote is not None:
            is_valid = True

        # In case cleanup_text() cannot find valid string, just return as-is.
        invalid_counter += 1
        if invalid_counter > 10:
            return random_row[0]

    return quote


def convert_to_multiline_array(text, max_chars_per_line) -> list:
    lines = []
    line = ""

    for word in text.split():
        if word == "Commentary:":
            # start new line
            lines.append(line)
            line = word + " "
        elif len(line + word) <= max_chars_per_line:
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
    quote = get_random_quote(df)
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
