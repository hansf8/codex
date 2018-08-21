import os
import sys

# Explicitly add parent package to path to enable imports to work in interactive
# sessions.
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__))))
