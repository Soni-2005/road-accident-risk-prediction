import streamlit as st

def apply_global_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background: rgba(0,0,0,0);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
