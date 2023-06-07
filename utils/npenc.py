"""
Custom JSON encoder for NumPy data types.

This module contains a custom JSON encoder class `NpEncoder` 
that extends the default JSONEncoder to handle NumPy data types.

Classes:
    NpEncoder: A custom JSON encoder class that can handle NumPy data types.
"""
import json
import numpy as np


class NpEncoder(json.JSONEncoder):
    """
    A custom JSON encoder that extends the default JSONEncoder to handle NumPy data types.

    Overrides the default method to convert NumPy integers, floats, arrays, and booleans
    to their Python equivalents before encoding to JSON.

    Args:
        json.JSONEncoder (class): The default JSON encoder class to extend.

    Returns:
        JSONEncoder: A custom JSON encoder class that can handle NumPy data types.
    """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.bool_):
            return bool(obj)
        return super(NpEncoder, self).default(obj)
