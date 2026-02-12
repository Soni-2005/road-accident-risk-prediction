import streamlit as st


def render_safety_ribbon():
    """
    High-contrast, subtle rolling safety ribbon.
    Works on light & dark backgrounds.
    """

    messages = [
        "🚧 Drive cautiously near junctions",
        "🌧️ Reduce speed on wet roads",
        "🌙 Night-time visibility may be reduced",
        "🚶 Watch for pedestrians in urban areas",
        "🛑 Maintain safe braking distance",
    ]

    ribbon_text = " • ".join(messages)

    st.markdown(
        f"""
        <div class="safety-ribbon">
            <div class="safety-ribbon-track">
                {ribbon_text}
            </div>
        </div>

        <style>
        /* ===============================
           SAFETY RIBBON — FINAL FIX
           =============================== */

        .safety-ribbon {{
            width: 100%;
            overflow: hidden;
            margin: 14px 0 22px 0;
            padding: 10px 0;
            border-radius: 14px;

            /* DARK GLASS BACKGROUND */
            background: rgba(15, 23, 42, 0.65); /* slate-900 */
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);

            border: 1px solid rgba(255, 255, 255, 0.18);
        }}

        .safety-ribbon-track {{
            display: inline-block;
            white-space: nowrap;
            padding-left: 100%;
            animation: ribbon-scroll 30s linear infinite;

            font-size: 15px;
            font-weight: 500;
            color: #f8fafc; /* HIGH CONTRAST TEXT */
            letter-spacing: 0.3px;
        }}

        @keyframes ribbon-scroll {{
            0% {{
                transform: translateX(0);
            }}
            100% {{
                transform: translateX(-100%);
            }}
        }}

        @media (prefers-reduced-motion: reduce) {{
            .safety-ribbon-track {{
                animation: none;
                padding-left: 0;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
