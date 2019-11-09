import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
if os.path.exists(os.path.join(os.path.dirname(__file__), 'py_modules')):
    sys.path.append(os.path.join(os.path.dirname(__file__), 'py_modules'))
