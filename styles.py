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

    .stApp {
        background-color: #030712 !important;
        background-image: 
            radial-gradient(circle at 10% 10%, rgba(16, 185, 129, 0.12) 0%, transparent 45%),
            radial-gradient(circle at 90% 10%, rgba(99, 102, 241, 0.15) 0%, transparent 45%),
            radial-gradient(circle at 50% 90%, rgba(168, 85, 247, 0.1) 0%, transparent 50%) !important;
        background-attachment: fixed !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Brand Logo Gradient */
    .brand-button {
        background: linear-gradient(135deg, #10b981 0%, #6366f1 50%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 30px;
        font-weight: 900;
        letter-spacing: -1.5px;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        filter: drop-shadow(0 0 12px rgba(99, 102, 241, 0.3));
    }

    /* Core Container Cards */
    .hd-card {
        background: rgba(15, 23, 42, 0.65) !important;
        backdrop-filter: blur(24px) saturate(180%);
        -webkit-backdrop-filter: blur(24px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px !important;
        padding: 24px !important;
        box-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.7);
        margin-bottom: 20px;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .hd-card:hover {
        border-color: rgba(16, 185, 129, 0.3) !important;
    }

    /* XP & Level Bar Styling */
    .xp-bar-bg {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        height: 14px;
        width: 100%;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .xp-bar-fill {
        background: linear-gradient(90deg, #10b981, #38bdf8, #a855f7);
        height: 100%;
        border-radius: 12px;
        transition: width 0.8s ease-in-out;
    }

    /* Trophy Badge Cards */
    .trophy-card {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 16px;
        text-align: center;
        transition: all 0.3s ease;
    }

    .trophy-card:hover {
        border-color: #eab308;
        transform: translateY(-4px);
        box-shadow: 0 10px 25px -5px rgba(234, 179, 8, 0.3);
    }

    /* Expandable Sport Cards */
    .expandable-sport-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.6));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 20px;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }

    .expandable-sport-card:hover {
        transform: translateY(-4px);
        border-color: rgba(16, 185, 129, 0.5);
        box-shadow: 0 16px 35px -10px rgba(16, 185, 129, 0.25);
    }

    .expandable-sport-card-active {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.98), rgba(16, 185, 129, 0.15)) !important;
        border: 1.5px solid #10b981 !important;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 20px 45px -10px rgba(16, 185, 129, 0.35);
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Cyberpunk Focus Overlay Card */
    .cyber-focus-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(10, 15, 30, 0.98));
        border: 2px solid #38bdf8;
        border-radius: 24px;
        padding: 32px;
        text-align: center;
        box-shadow: 0 0 50px rgba(56, 189, 248, 0.3);
    }

    /* Primary Action Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        font-size: 13px !important;
        letter-spacing: 0.5px !important;
        padding: 0.65rem 1.4rem !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 6px 18px rgba(16, 185, 129, 0.3) !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.5) !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #02040a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    .stRadio > div > label {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #cbd5e1 !important;
        transition: all 0.25s ease !important;
    }

    .stRadio > div > label:hover {
        background: linear-gradient(90deg, rgba(99, 102, 241, 0.15), rgba(16, 185, 129, 0.15)) !important;
        border-color: rgba(16, 185, 129, 0.5) !important;
        color: #ffffff !important;
        transform: translateX(4px);
    }

    /* Inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div, .stNumberInput>div>div>input {
        background: rgba(15, 23, 42, 0.9) !important;
        color: #f8fafc !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def render_score_ring_hd(score, label="Good progress"):
    stroke_offset = 314 - (314 * score / 100)
    return f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; position:relative; padding:10px;">
        <svg width="180" height="180" viewBox="0 0 120 120">
            <circle cx="60" cy="60" r="50" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="10" />
            <circle cx="60" cy="60" r="50" fill="none" stroke="url(#hdScoreGrad)" stroke-width="10" 
                    stroke-dasharray="314" stroke-dashoffset="{stroke_offset}" 
                    stroke-linecap="round" transform="rotate(-90 60 60)" 
                    style="transition: stroke-dashoffset 1.2s ease-out;" />
            <defs>
                <linearGradient id="hdScoreGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#10b981" />
                    <stop offset="50%" stop-color="#38bdf8" />
                    <stop offset="100%" stop-color="#a855f7" />
                </linearGradient>
            </defs>
        </svg>
        <div style="position:absolute; text-align:center; top:52px;">
            <div style="font-size:44px; font-weight:900; color:#ffffff; line-height:1; letter-spacing:-1.5px;">{score}</div>
            <div style="font-size:11px; color:#94a3b8; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-top:4px;">Productivity Index</div>
        </div>
        <div style="margin-top:12px; font-size:13px; font-weight:800; color:#10b981; letter-spacing:0.5px; text-transform:uppercase;">{label}</div>
    </div>
    """