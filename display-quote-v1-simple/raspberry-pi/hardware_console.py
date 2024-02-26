#!/usr/bin/env python
# -*- coding:utf-8 -*-
# For testing purpose, outputs to screen or console

import logging

logging.basicConfig(level=logging.DEBUG)


def display_data(lines: list, start_x=10, start_y=10, y_inc=21):
    logging.info(f"epd4in2 display text: {lines}")
    print("\n".join(lines))
