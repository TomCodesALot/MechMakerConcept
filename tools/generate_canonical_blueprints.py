import os
import json

BLUEPRINTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datafiles', 'blueprints')
os.makedirs(BLUEPRINTS_DIR, exist_ok=True)
