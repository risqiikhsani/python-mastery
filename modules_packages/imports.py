"""
Modules and Packages: Import system
"""

# Import styles
import os
from pathlib import Path

# From import
from collections import defaultdict, OrderedDict

# Alias import
import numpy as np
import pandas as pd

# Selective function import
from math import sqrt, pi

# Relative imports in packages
# from . import module  (same package)
# from .. import module (parent package)
# from ..sibling import func


# Dynamic imports
def dynamic_import(module_name: str):
    module = __import__(module_name)
    return module


# Importlib for runtime imports
import importlib


def reload_module(module_name: str):
    module = importlib.import_module(module_name)
    importlib.reload(module)
    return module


# Inspecting imports
def list_imports():
    import sys
    return list(sys.modules.keys())


# Package __init__.py example structure
"""
mypackage/
    __init__.py      # Package initialization
    module1.py       # Submodule
    subpackage/
        __init__.py
        module2.py
"""

# __all__ controls what's exported with "from package import *"
__all__ = ['public_function', 'PublicClass']


# Module attributes
def module_info():
    import sys
    this_module = __import__(__name__)
    print(f"Module: {this_module.__name__}")
    print(f"File: {this_module.__file__}")
    print(f"Doc: {this_module.__doc__}")
    print(f"Package: {getattr(this_module, '__package__', None)}")


# Lazy imports for heavy modules
def lazy_import_pandas():
    if not hasattr(lazy_import_pandas, '_pd'):
        import pandas as pd
        lazy_import_pandas._pd = pd
    return lazy_import_pandas._pd


# Version checking
def check_module_version(module_name: str, min_version: str):
    import importlib
    module = importlib.import_module(module_name)
    version = getattr(module, '__version__', '0.0.0')
    from packaging.version import parse
    return parse(version) >= parse(min_version)