import pandas as pd

def color_zero_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for zero
    strings, white otherwise.
    """
    color = 'red' if val == 0 else 'white'
    return 'color: %s' % color

