from unittest.mock import patch
from graph_io.test import MODE, UNIT


def clever_patch_method(object, attribute_name, return_value=None):
    wrapped = (lambda *args, **kwargs: return_value) if MODE == UNIT else getattr(object, attribute_name)
    return patch.object(object, attribute_name, wraps=wrapped)