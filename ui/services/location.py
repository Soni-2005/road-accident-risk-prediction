# services/location.py
import streamlit as st
import streamlit.components.v1 as components

def get_browser_location():
    components.html(
        """
        <script>
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                Streamlit.setComponentValue({
                    lat: pos.coords.latitude,
                    lon: pos.coords.longitude
                });
            },
            (err) => {
                Streamlit.setComponentValue(null);
            }
        );
        </script>
        """,
        height=0,
    )

    if "browser_location" in st.session_state:
        return st.session_state.browser_location

    return None
