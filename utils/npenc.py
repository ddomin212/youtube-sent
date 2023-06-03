import numpy as np
import json

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