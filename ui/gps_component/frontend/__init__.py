import streamlit.components.v1 as components
from pathlib import Path

_component_func = components.declare_component(
    "gps_location",
    path=str(Path(__file__).parent / "frontend"),
)

def get_gps_location():
    return _component_func()
