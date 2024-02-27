#!/usr/bin/env python
# For waveshare 4.2" e-Paper Module
# -*- coding:utf-8 -*-
import sys
import os

picdir = os.path.join(os.path.dirname((os.path.realpath(__file__))), "pic")
libdir = os.path.join(os.path.dirname((os.path.realpath(__file__))), "lib")
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd4in2_V2
import time
from PIL import Image, ImageDraw, ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)


def display_data(lines, start_x=10, start_y=10, y_inc=21):
    logging.info(f"epd4in2 display text: {lines}")
    epd = epd4in2_V2.EPD()
    try:
        logging.info("init and Clear")
        epd.init()
        epd.Clear()

        font15 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 15)
        font18 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 18)
        font24 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 24)
        font35 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 35)

        font_to_use = font15

        logging.info("6.4Gray display--------------------------------")
        epd.Init_4Gray()

        Limage = Image.new("L", (epd.width, epd.height), 0)  # 255: clear the frame
        draw = ImageDraw.Draw(Limage)

        x = start_x
        y = start_y
        for line in lines:
            draw.text((x, y), line, font=font_to_use, fill=epd.GRAY1)
            y += y_inc

        epd.display_4Gray(epd.getbuffer_4Gray(Limage))
        epd.sleep()
    except:
        epd4in2_V2.epdconfig.module_exit(cleanup=True)
