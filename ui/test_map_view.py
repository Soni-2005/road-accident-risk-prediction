import streamlit as st
from components.map_view import render_map

st.set_page_config(layout="wide")

# Example: Bangalore Electronic City
render_map(
    latitude=12.8399,
    longitude=77.6770,
)
