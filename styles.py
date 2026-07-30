import streamlit as st

def apply_neon_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        -webkit-font-smoothing: antialiased;
        color: #f8fafc;
    }

    /* Ambient Pulsing Background Animation */
    @keyframes ambientPulse {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background-color: #030712 !important;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(0, 243, 255, 0.15) 0%, transparent 45%),
            radial-gradient(circle at 90% 20%, rgba(168, 85, 247, 0.18) 0%, transparent 45%),
            radial-gradient(circle at 50% 80%, rgba(255, 0, 85, 0.12) 0%, transparent 50%),
            radial-gradient(circle at 20% 80%, rgba(16, 185, 129, 0.15) 0%, transparent 40%) !important;
        background-size: 200% 200% !important;
        animation: ambientPulse 15s ease infinite !important;
        background-attachment: fixed !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Brand Logo Gradient */
    .brand-button {
        background: linear-gradient(135deg, #00f3ff 0%, #a855f7 50%, #ff0055 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 32px;
        font-weight: 900;
        letter-spacing: -1.5px;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        filter: drop-shadow(0 0 16px rgba(0, 243, 255, 0.4));
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .brand-button:hover {
        transform: scale(1.04) rotate(-1deg);
    }

    /* Core Container Cards with 3D Depth */
    .hd-card {
        background: rgba(15, 23, 42, 0.75) !important;
        backdrop-filter: blur(24px) saturate(200%);
        -webkit-backdrop-filter: blur(24px) saturate(200%);
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 22px !important;
        padding: 24px !important;
        box-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.8), inset 0 1px 1px rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .hd-card:hover {
        border-color: rgba(0, 243, 255, 0.4) !important;
        transform: translateY(-4px);
        box-shadow: 0 25px 60px -12px rgba(0, 243, 255, 0.25);
    }

    /* XP & Level Bar Styling */
    .xp-bar-bg {
        background: rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        height: 16px;
        width: 100%;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
    }

    .xp-bar-fill {
        background: linear-gradient(90deg, #00f3ff, #10b981, #a855f7, #ff0055);
        background-size: 200% 100%;
        animation: ambientPulse 3s ease infinite;
        height: 100%;
        border-radius: 14px;
        transition: width 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    /* Trophy Badge Cards */
    .trophy-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.8));
        border: 1px solid rgba(234, 179, 8, 0.25);
        border-radius: 18px;
        padding: 18px;
        text-align: center;
        transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
    }

    .trophy-card:hover {
        border-color: #eab308;
        transform: translateY(-6px) scale(1.03);
        box-shadow: 0 15px 30px -5px rgba(234, 179, 8, 0.4);
    }

    /* Expandable Vivid Sport Cards */
    .expandable-sport-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.85));
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        padding: 22px;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
    }

    .expandable-sport-card:hover {
        transform: translateY(-6px) scale(1.015);
        border-color: #00f3ff;
        box-shadow: 0 20px 40px -10px rgba(0, 243, 255, 0.35);
    }

    .expandable-sport-card-active {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.98), rgba(0, 243, 255, 0.2)) !important;
        border: 2px solid #00f3ff !important;
        border-radius: 22px;
        padding: 26px;
        box-shadow: 0 25px 50px -10px rgba(0, 243, 255, 0.45);
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Leaderboard Item Micro-Animation */
    .leaderboard-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 14px;
        border-radius: 12px;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 8px;
        transition: all 0.3s ease;
    }
    .leaderboard-row:hover {
        background: rgba(0, 243, 255, 0.1);
        border-color: #00f3ff;
        transform: translateX(6px);
    }

    /* Cyberpunk Focus Overlay Card */
    .cyber-focus-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.98), rgba(10, 15, 30, 0.99));
        border: 2px solid #00f3ff;
        border-radius: 26px;
        padding: 36px;
        text-align: center;
        box-shadow: 0 0 60px rgba(0, 243, 255, 0.4);
        animation: focusPulse 2s ease-in-out infinite alternate;
    }

    @keyframes focusPulse {
        from { box-shadow: 0 0 30px rgba(0, 243, 255, 0.3); }
        to { box-shadow: 0 0 70px rgba(0, 243, 255, 0.6); }
    }

    /* Primary Animated Action Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #00f3ff 0%, #10b981 100%) !important;
        color: #02040a !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 900 !important;
        font-size: 13px !important;
        letter-spacing: 0.5px !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 6px 20px rgba(0, 243, 255, 0.35) !important;
    }

    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 12px 28px rgba(0, 243, 255, 0.55) !important;
        color: #ffffff !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #02040a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    .stRadio > div > label {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 14px 18px !important;
        font-size: 15px !important;
        font-weight: 800 !important;
        color: #cbd5e1 !important;
        transition: all 0.3s ease !important;
    }

    .stRadio > div > label:hover {
        background: linear-gradient(90deg, rgba(0, 243, 255, 0.2), rgba(168, 85, 247, 0.2)) !important;
        border-color: #00f3ff !important;
        color: #ffffff !important;
        transform: translateX(6px);
        box-shadow: 0 6px 15px rgba(0, 243, 255, 0.2);
    }

    /* Vivid Inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div, .stNumberInput>div>div>input {
        background: rgba(15, 23, 42, 0.95) !important;
        color: #f8fafc !important;
        border-radius: 14px !important;
        border: 1px solid rgba(0, 243, 255, 0.2) !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput>div>div>input:focus, .stSelectbox>div>div:focus {
        border-color: #00f3ff !important;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

def render_score_ring_hd(score, label="Good progress"):
    stroke_offset = 314 - (314 * score / 100)
    return f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; position:relative; padding:10px;">
        <svg width="190" height="190" viewBox="0 0 120 120">
            <circle cx="60" cy="60" r="50" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="10" />
            <circle cx="60" cy="60" r="50" fill="none" stroke="url(#hdScoreGrad)" stroke-width="10" 
                    stroke-dasharray="314" stroke-dashoffset="{stroke_offset}" 
                    stroke-linecap="round" transform="rotate(-90 60 60)" 
                    style="transition: stroke-dashoffset 1.4s cubic-bezier(0.34, 1.56, 0.64, 1);" />
            <defs>
                <linearGradient id="hdScoreGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#00f3ff" />
                    <stop offset="40%" stop-color="#10b981" />
                    <stop offset="70%" stop-color="#a855f7" />
                    <stop offset="100%" stop-color="#ff0055" />
                </linearGradient>
            </defs>
        </svg>
        <div style="position:absolute; text-align:center; top:54px;">
            <div style="font-size:46px; font-weight:900; color:#ffffff; line-height:1; letter-spacing:-1.5px; filter: drop-shadow(0 0 8px rgba(0, 243, 255, 0.5));">{score}</div>
            <div style="font-size:10px; color:#00f3ff; font-weight:800; text-transform:uppercase; letter-spacing:1.5px; margin-top:4px;">Productivity Index</div>
        </div>
        <div style="margin-top:12px; font-size:13px; font-weight:900; color:#10b981; letter-spacing:0.8px; text-transform:uppercase;">{label}</div>
    </div>
    """