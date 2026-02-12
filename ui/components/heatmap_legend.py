"""
Heatmap Legend Component
Displays color-coded risk level interpretation with matched height to map.
"""
import streamlit as st
import streamlit.components.v1 as components


def render_heatmap_legend():
    """
    Renders a fixed legend showing heatmap color scale.
    Height matches map (520px) for perfect alignment.
    """
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            html, body {
                height: 100%;
                margin: 0;
                padding: 0;
            }
            
            .legend-card {
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                border-radius: 12px;
                padding: 24px;
                color: white;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                box-shadow: 0 8px 24px rgba(0,0,0,0.15);
                min-height: 600px;
                display: flex;
                flex-direction: column;
            }
            
            .legend-title {
                font-size: 18px;
                font-weight: 700;
                margin-bottom: 20px;
                text-align: center;
                letter-spacing: 0.5px;
            }
            
            .legend-items {
                display: flex;
                flex-direction: column;
                gap: 16px;
                flex-grow: 1;
            }
            
            .legend-item {
                display: flex;
                align-items: center;
                gap: 14px;
                padding: 12px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                transition: all 0.2s ease;
            }
            
            .legend-item:hover {
                background: rgba(255, 255, 255, 0.15);
                transform: translateX(4px);
            }
            
            .color-box {
                width: 50px;
                height: 50px;
                border-radius: 8px;
                flex-shrink: 0;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            }
            
            .legend-label {
                display: flex;
                flex-direction: column;
                gap: 4px;
            }
            
            .risk-level {
                font-weight: 600;
                font-size: 15px;
                letter-spacing: 0.3px;
            }
            
            .risk-range {
                font-size: 12px;
                opacity: 0.85;
                font-weight: 400;
            }
            
            .legend-footer {
                margin-top: 20px;
                padding-top: 16px;
                border-top: 1px solid rgba(255, 255, 255, 0.2);
                text-align: center;
                font-size: 11px;
                opacity: 0.75;
                font-style: italic;
            }
        </style>
    </head>
    <body>
        <div class="legend-card">
            <div class="legend-title">🗺️ Risk Level Guide</div>
            
            <div class="legend-items">
                <div class="legend-item">
                    <div class="color-box" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);"></div>
                    <div class="legend-label">
                        <span class="risk-level">🟢 Very Low</span>
                        <span class="risk-range">Risk Score: 0.0 – 0.2</span>
                    </div>
                </div>
                
                <div class="legend-item">
                    <div class="color-box" style="background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);"></div>
                    <div class="legend-label">
                        <span class="risk-level">🟡 Low</span>
                        <span class="risk-range">Risk Score: 0.2 – 0.4</span>
                    </div>
                </div>
                
                <div class="legend-item">
                    <div class="color-box" style="background: linear-gradient(135deg, #fb923c 0%, #f97316 100%);"></div>
                    <div class="legend-label">
                        <span class="risk-level">🟠 Moderate</span>
                        <span class="risk-range">Risk Score: 0.4 – 0.6</span>
                    </div>
                </div>
                
                <div class="legend-item">
                    <div class="color-box" style="background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);"></div>
                    <div class="legend-label">
                        <span class="risk-level">🔴 High</span>
                        <span class="risk-range">Risk Score: 0.6 – 0.8</span>
                    </div>
                </div>
                
                <div class="legend-item">
                    <div class="color-box" style="background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);"></div>
                    <div class="legend-label">
                        <span class="risk-level">🔥 Very High</span>
                        <span class="risk-range">Risk Score: 0.8 – 1.0</span>
                    </div>
                </div>
            </div>
            
            <div class="legend-footer">
                Colors indicate predicted accident risk based on location, time, and weather conditions
            </div>
        </div>
    </body>
    </html>
    """
    
    # ✅ Height matches map (600px), scroll happens inside
    components.html(html, height=600, scrolling=True)