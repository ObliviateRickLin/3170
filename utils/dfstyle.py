import pandas as pd

def color_zero_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    if val == 0:
        color = 'red'
    return 'color: %s' % color

