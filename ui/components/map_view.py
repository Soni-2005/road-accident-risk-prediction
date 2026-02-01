# ==================================================
# UI COMPONENT — OSM MAP VIEW
# Phase 14.2.3b
# ==================================================

import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium


def render_map(
    latitude: float,
    longitude: float,
    zoom: int = 14,
    height: int = 420,
):
    """
    Renders an OpenStreetMap centered on user's location.

    Parameters
    ----------
    latitude : float
        User latitude
    longitude : float
        User longitude
    zoom : int
        Initial zoom level
    height : int
        Map height in pixels
    """

    # --------------------------------------------------
    # Create base map
    # --------------------------------------------------
    m = folium.Map(
        location=[latitude, longitude],
        zoom_start=zoom,
        control_scale=True,
        tiles="OpenStreetMap",
    )

    # --------------------------------------------------
    # User location marker
    # --------------------------------------------------
    folium.Marker(
        location=[latitude, longitude],
        popup="📍 You are here",
        tooltip="Current Location",
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(m)

    # --------------------------------------------------
    # Placeholder: cluster layer (future accidents / hotspots)
    # --------------------------------------------------
    MarkerCluster(name="Hotspots (future)").add_to(m)

    # --------------------------------------------------
    # Render map in Streamlit
    # --------------------------------------------------
    st_folium(
        m,
        height=height,
        use_container_width=True,
    )
