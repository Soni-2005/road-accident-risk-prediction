import streamlit as st
from components.risk_cards import render_risk_cards

st.set_page_config(layout="wide")

render_risk_cards(
    probability=0.42,
    severity=0.71,
    risk_level="High",
)
