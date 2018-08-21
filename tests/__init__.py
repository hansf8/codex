import os
import sys

# Add app package to path as recommended by Kenneth Reitz.
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '../src/')))
