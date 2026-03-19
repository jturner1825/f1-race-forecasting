import sys
from pathlib import Path
import streamlit as st
sys.path.insert(0, str(Path(__file__).parents[2] / "src" / "simulator"))

from services.loader import load_teams, load_drivers, load_circuits

