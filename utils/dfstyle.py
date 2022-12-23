import pandas as pd

def color_zero(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for zero
    strings, white otherwise.
    """
    color = 'green' if val == 0 else 'white'
    return 'color: %s' % color

