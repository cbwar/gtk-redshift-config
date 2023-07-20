# -*- coding: utf-8 -*-

def validate_color_temp(value) -> str:
    try:
        value = int(value)
    except:
        value = 6400
    if value <= 0:
        value = 6400
    if value > 10000:
        value = 10000
    return str(value)


def validate_brightness(value) -> str:
    try:
        value = float(value)
    except:
        value = 1.0
    if value <= 0.1:
        value = 0.1
    if value > 1.0:
        value = 1.0
    return str(value)
