import streamlit as st
from pathlib import Path
import base64


def get_base64_image(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def render_welcome():
    UI_ROOT = Path(__file__).parent.parent
    BG_IMAGE = UI_ROOT / "assets" / "road3.jpg"

    # Safety guard for image path
    if BG_IMAGE.exists():
        bg_base64 = get_base64_image(BG_IMAGE)
        bg_style = f"background: url('data:image/jpeg;base64,{bg_base64}') no-repeat center center fixed;"
    else:
        st.error(f"Background image not found: {BG_IMAGE}")
        bg_style = "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);"

    st.markdown(
        f"""
        <style>
        .stApp {{
            {bg_style}
            background-size: cover;
            min-height: 100vh;
        }}

        /* Make ALL Streamlit containers completely transparent */
        .main {{
            background: transparent !important;
        }}

        .block-container {{
            background: transparent !important;
            padding-top: 4rem !important;
            padding-bottom: 1rem !important;
        }}

        section[data-testid="stSidebar"] {{
            background: transparent !important;
        }}

        /* Title Container - Pushed down */
        .title-container {{
            background: transparent;
            padding: 25px 20px;
            text-align: center;
            margin-bottom: 25px;
            margin-top: 30px;
        }}

        .welcome-title {{
            font-size: 42px;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 10px;
            text-shadow: 
                3px 3px 8px rgba(0,0,0,0.95),
                -1px -1px 2px rgba(0,0,0,0.8),
                0 0 20px rgba(0,0,0,0.7);
            letter-spacing: 1px;
            line-height: 1.1;
        }}

        .welcome-sub {{
            font-size: 18px;
            color: #ffffff;
            font-weight: 500;
            text-shadow: 
                2px 2px 6px rgba(0,0,0,0.95),
                -1px -1px 2px rgba(0,0,0,0.8),
                0 0 15px rgba(0,0,0,0.6);
        }}

        /* Mode Selection Container */
        .mode-container {{
            background: transparent;
            padding: 15px 20px;
            text-align: center;
            margin-bottom: 18px;
        }}

        .welcome-highlight {{
            font-size: 18px;
            color: #ffd700;
            font-weight: 700;
            margin-bottom: 18px;
            text-shadow: 
                3px 3px 10px rgba(0,0,0,1),
                -2px -2px 4px rgba(0,0,0,0.9),
                0 0 25px rgba(0,0,0,0.9);
        }}

        /* Radio buttons styling - SAME GREY COLOR, HORIZONTAL */
        div[data-testid="stRadio"] {{
            background: transparent !important;
            margin-bottom: 18px !important;
        }}

        div[data-testid="stRadio"] > div {{
            background: transparent !important;
            justify-content: center !important;
            display: flex !important;
            flex-direction: row !important;
            gap: 20px !important;
            align-items: center !important;
        }}

        /* Both radio buttons - SAME GREY */
        div[data-testid="stRadio"] > div > label {{
            background: #5a5a5a !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            font-size: 18px !important;
            padding: 14px 32px !important;
            border-radius: 10px !important;
            border: 3px solid rgba(255, 255, 255, 0.9) !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            min-width: 170px !important;
            text-align: center !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            box-shadow: 
                0 4px 15px rgba(0,0,0,0.7),
                inset 0 1px 2px rgba(255,255,255,0.15) !important;
        }}

        div[data-testid="stRadio"] > div > label:hover {{
            background: #707070 !important;
            border-color: rgba(255, 255, 255, 1) !important;
            box-shadow: 
                0 6px 20px rgba(0,0,0,0.8),
                0 0 25px rgba(255,255,255,0.5),
                inset 0 1px 2px rgba(255,255,255,0.2) !important;
            transform: translateY(-2px) !important;
        }}

        /* Radio button input styling */
        div[data-testid="stRadio"] input[type="radio"] {{
            width: 20px !important;
            height: 20px !important;
            margin-right: 10px !important;
            accent-color: #ffd700 !important;
            cursor: pointer !important;
        }}

        /* Selected state - More visible */
        div[data-testid="stRadio"] > div > label:has(input:checked) {{
            background: #ffd700 !important;
            color: #000000 !important;
            font-weight: 900 !important;
            border-color: #ffd700 !important;
            box-shadow: 
                0 6px 25px rgba(255,215,0,0.8),
                0 0 40px rgba(255,215,0,0.7),
                inset 0 1px 3px rgba(0,0,0,0.2) !important;
            text-shadow: none !important;
        }}

        /* Button styling */
        .stButton > button {{
            background: rgba(0, 0, 0, 0.7) !important;
            border: 3px solid rgba(255, 255, 255, 0.9) !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            font-size: 18px !important;
            padding: 12px 35px !important;
            text-shadow: 
                3px 3px 8px rgba(0,0,0,1),
                -2px -2px 3px rgba(0,0,0,0.9) !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.6) !important;
        }}

        .stButton > button:hover {{
            background: rgba(0, 0, 0, 0.85) !important;
            border-color: #ffffff !important;
            box-shadow: 
                0 6px 20px rgba(0,0,0,0.8),
                0 0 25px rgba(255,255,255,0.4) !important;
            transform: translateY(-2px) !important;
        }}

        /* Bottom message */
        .welcome-positive {{
            font-size: 17px;
            color: #2ecc71;
            font-weight: 800;
            text-align: center;
            margin-top: 15px;
            text-shadow: 
                3px 3px 10px rgba(0,0,0,1),
                -2px -2px 4px rgba(0,0,0,0.9),
                0 0 25px rgba(0,0,0,0.9);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Title Container
    st.markdown(
        """
        <div class="title-container">
            <div class="welcome-title">🚦 Road Accident Risk Predictor</div>
            <div class="welcome-sub">AI-powered road safety insights for safer journeys</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Mode Selection Prompt
    st.markdown(
        '<div class="mode-container"><div class="welcome-highlight">Please select a mode to proceed</div></div>',
        unsafe_allow_html=True,
    )

    # Radio buttons (horizontal, centered)
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        mode = st.radio(
            "Mode selector",
            ["Default Mode", "Manual Mode"],
            horizontal=True,
            label_visibility="collapsed",
        )

    # Continue button (centered)
    col1, col2, col3 = st.columns([1.5, 2, 1.5])
    with col2:
        if st.button("Continue →", use_container_width=True):
            st.session_state.selected_mode = mode
            st.rerun()

    # Bottom positive message
    st.markdown(
        '<div class="welcome-positive">🌱 Have a safe and pleasant journey</div>',
        unsafe_allow_html=True,
    )