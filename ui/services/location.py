import streamlit as st
from gps_component import get_gps_location


def get_browser_location():
    """
    Uses the custom Streamlit GPS component to fetch browser location.
    Returns:
        (lat, lon, location_name) or None
    """

    # Cache location for the session
    if "gps_location" in st.session_state:
        return st.session_state["gps_location"]

    # Call custom component (triggers browser permission)
    result = get_gps_location()

    # Component not ready yet
    if result is None:
        return None

    # User denied permission or browser error
    if isinstance(result, dict) and "error" in result:
        st.warning("📍 Location access denied. Please allow location permission.")
        return None

    # Successful GPS read
    try:
        lat = float(result["latitude"])
        lon = float(result["longitude"])
    except Exception:
        return None

    st.session_state["gps_location"] = (lat, lon, "Current Location")
    return st.session_state["gps_location"]
