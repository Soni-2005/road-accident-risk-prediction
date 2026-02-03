import streamlit as st
from ui.gps_component import get_gps_location


def get_browser_location():
    if "gps_location" in st.session_state:
        return st.session_state["gps_location"]

    result = get_gps_location()

    if result is None:
        return None

    if "error" in result:
        st.warning("Location access denied. Please allow GPS access.")
        return None

    lat = result["latitude"]
    lon = result["longitude"]

    st.session_state["gps_location"] = (lat, lon, "Current Location")
    return st.session_state["gps_location"]
