# -*- coding: utf-8 -*-


def validate_color_temp(value) -> int:
    try:
        value = int(value)
    except:
        value = 6400
    if value <= 0:
        value = 6400
    if value > 10000:
        value = 10000
    return str(value)
