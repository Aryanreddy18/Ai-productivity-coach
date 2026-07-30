import streamlit as st

def apply_neon_theme(theme_mode="Dark Cyberpunk"):
    if theme_mode == "Light Clean":
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
            -webkit-font-smoothing: antialiased;
            color: #0f172a !important;
        }

        .stApp {
            background-color: #f8fafc !important;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(79, 70, 229, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 90% 20%, rgba(16, 185, 129, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 50% 80%, rgba(236, 72, 153, 0.04) 0%, transparent 50%) !important;
            background-size: 100% 100% !important;
            background-attachment: fixed !important;
        }

        header[data-testid="stHeader"] {
            background: transparent !important;
        }

        .brand-button {
            background: linear-gradient(135deg, #4f46e5 0%, #0d9488 50%, #db2777 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 32px;
            font-weight: 900;
            letter-spacing: -1.5px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            filter: drop-shadow(0 2px 8px rgba(79, 70, 229, 0.2));
            transition: transform 0.3s ease;
        }
        .brand-button:hover {
            transform: scale(1.04);
        }

        /* LIGHT MODE CARDS */
        .hd-card {
            background: #ffffff !important;
            backdrop-filter: blur(20px);
            border: 1px solid #e2e8f0 !important;
            border-radius: 22px !important;
            padding: 24px !important;
            box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
            margin-bottom: 20px;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            color: #0f172a !important;
        }
        
        .hd-card:hover {
            border-color: rgba(79, 70, 229, 0.4) !important;
            transform: translateY(-3px);
            box-shadow: 0 20px 35px -10px rgba(79, 70, 229, 0.12);
        }

        .xp-bar-bg {
            background: #e2e8f0;
            border-radius: 14px;
            height: 16px;
            width: 100%;
            overflow: hidden;
            border: 1px solid #cbd5e1;
        }

        .xp-bar-fill {
            background: linear-gradient(90deg, #4f46e5, #0d9488, #db2777);
            height: 100%;
            border-radius: 14px;
            transition: width 0.8s ease;
        }

        .wild-streak-box {
            background: linear-gradient(135deg, rgba(249, 115, 22, 0.08), rgba(225, 29, 72, 0.08));
            border: 2px solid #f97316;
            border-radius: 18px;
            padding: 16px;
            text-align: center;
            position: relative;
            box-shadow: 0 8px 20px rgba(249, 115, 22, 0.12);
        }

        .flame-icon-animated {
            display: inline-block;
            font-size: 32px;
        }

        .trophy-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 18px;
            padding: 18px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            transition: all 0.3s ease;
        }
        .trophy-card:hover {
            border-color: #eab308;
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(234, 179, 8, 0.15);
        }

        .expandable-sport-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 20px;
            padding: 22px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            color: #0f172a !important;
        }
        .expandable-sport-card:hover {
            transform: translateY(-4px);
            border-color: #4f46e5;
            box-shadow: 0 15px 30px rgba(79, 70, 229, 0.12);
        }

        .expandable-sport-card-active {
            background: linear-gradient(145deg, #ffffff, rgba(79, 70, 229, 0.05)) !important;
            border: 2px solid #4f46e5 !important;
            border-radius: 22px;
            padding: 26px;
            box-shadow: 0 20px 40px rgba(79, 70, 229, 0.18);
            color: #0f172a !important;
        }

        .leaderboard-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 14px;
            border-radius: 12px;
            background: #f1f5f9;
            border: 1px solid #e2e8f0;
            margin-bottom: 8px;
            color: #0f172a;
        }

        .stButton>button {
            background: linear-gradient(135deg, #4f46e5 0%, #0d9488 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 14px !important;
            font-weight: 800 !important;
            padding: 0.75rem 1.5rem !important;
            box-shadow: 0 4px 14px rgba(79, 70, 229, 0.25) !important;
        }

        section[data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #e2e8f0 !important;
        }

        .stRadio > div > label {
            background: #f8fafc !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 16px !important;
            padding: 14px 18px !important;
            color: #334155 !important;
            font-weight: 700 !important;
        }
        .stRadio > div > label:hover {
            background: #f1f5f9 !important;
            border-color: #4f46e5 !important;
            color: #4f46e5 !important;
        }

        .stTextInput>div>div>input, .stSelectbox>div>div, .stNumberInput>div>div>input {
            background: #ffffff !important;
            color: #0f172a !important;
            border-radius: 14px !important;
            border: 1px solid #cbd5e1 !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        # CLEAN DARK CYBERPUNK THEME
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
            -webkit-font-smoothing: antialiased;
            color: #f8fafc;
        }

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
            color: #f8fafc !important;
        }
        
        .hd-card:hover {
            border-color: rgba(0, 243, 255, 0.4) !important;
            transform: translateY(-4px);
            box-shadow: 0 25px 60px -12px rgba(0, 243, 255, 0.25);
        }

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

        @keyframes flamePulse {
            0% { transform: scale(1) rotate(0deg); filter: drop-shadow(0 0 12px #f97316); }
            50% { transform: scale(1.12) rotate(3deg); filter: drop-shadow(0 0 24px #ff0055); }
            100% { transform: scale(1) rotate(0deg); filter: drop-shadow(0 0 12px #f97316); }
        }

        @keyframes streakGlow {
            0% { border-color: rgba(249, 115, 22, 0.4); box-shadow: 0 0 20px rgba(249, 115, 22, 0.2); }
            50% { border-color: rgba(255, 0, 85, 0.8); box-shadow: 0 0 35px rgba(255, 0, 85, 0.4); }
            100% { border-color: rgba(249, 115, 22, 0.4); box-shadow: 0 0 20px rgba(249, 115, 22, 0.2); }
        }

        .wild-streak-box {
            background: linear-gradient(135deg, rgba(249, 115, 22, 0.15), rgba(255, 0, 85, 0.15));
            border: 2px solid #f97316;
            border-radius: 18px;
            padding: 16px;
            text-align: center;
            animation: streakGlow 3s infinite ease-in-out;
            position: relative;
            overflow: hidden;
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .wild-streak-box:hover {
            transform: translateY(-5px) scale(1.03);
        }

        .flame-icon-animated {
            display: inline-block;
            font-size: 32px;
            animation: flamePulse 1.5s infinite ease-in-out;
        }

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

        .expandable-sport-card {
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.85));
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 20px;
            padding: 22px;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
            color: #f8fafc !important;
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
            color: #f8fafc !important;
        }

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
            color: #f8fafc;
        }
        .leaderboard-row:hover {
            background: rgba(0, 243, 255, 0.1);
            border-color: #00f3ff;
            transform: translateX(6px);
        }

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

def render_score_ring_hd(score, label="Good progress", is_light=False):
    stroke_offset = 314 - (314 * score / 100)
    text_color = "#0f172a" if is_light else "#ffffff"
    bg_circle = "#e2e8f0" if is_light else "rgba(255,255,255,0.06)"
    
    return f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; position:relative; padding:10px;">
        <svg width="190" height="190" viewBox="0 0 120 120">
            <circle cx="60" cy="60" r="50" fill="none" stroke="{bg_circle}" stroke-width="10" />
            <circle cx="60" cy="60" r="50" fill="none" stroke="url(#hdScoreGrad)" stroke-width="10" 
                    stroke-dasharray="314" stroke-dashoffset="{stroke_offset}" 
                    stroke-linecap="round" transform="rotate(-90 60 60)" 
                    style="transition: stroke-dashoffset 1.4s cubic-bezier(0.34, 1.56, 0.64, 1);" />
            <defs>
                <linearGradient id="hdScoreGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#4f46e5" />
                    <stop offset="40%" stop-color="#10b981" />
                    <stop offset="70%" stop-color="#a855f7" />
                    <stop offset="100%" stop-color="#ff0055" />
                </linearGradient>
            </defs>
        </svg>
        <div style="position:absolute; text-align:center; top:54px;">
            <div style="font-size:46px; font-weight:900; color:{text_color}; line-height:1; letter-spacing:-1.5px;">{score}</div>
            <div style="font-size:10px; color:#4f46e5; font-weight:800; text-transform:uppercase; letter-spacing:1.5px; margin-top:4px;">Productivity Index</div>
        </div>
        <div style="margin-top:12px; font-size:13px; font-weight:900; color:#10b981; letter-spacing:0.8px; text-transform:uppercase;">{label}</div>
    </div>
    """