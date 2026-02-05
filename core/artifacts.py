# Save / load artifacts

from dataclasses import dataclass,asdict
from pathlib import Path
from datetime import datetime
from typing import Any, Dict
import json
import pickle

# Base directory where all artifacts are stored
ARTIFACTS_DIR=Path("output")
ARTIFACTS_DIR.mkdir(exist_ok=True)