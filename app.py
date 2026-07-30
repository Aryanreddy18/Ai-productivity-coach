import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from streamlit_mic_recorder import speech_to_text

from database import (
    register_user, authenticate_user, add_task, get_tasks,
    update_task_status, delete_task, get_habits, add_habit, toggle_habit_day,
    get_user_profile, update_user_profile, export_user_data, add_user_xp, get_boss_info, get_top_leaderboard
)
from styles import apply_neon_theme, render_score_ring_hd
from ai_engine import (
    calculate_productivity_score, generate_rule_insights, get_ai_coach_response_v2, 
    calculate_ai_recovery_metrics, generate_executive_weekly_report
)

st.set_page_config(page_title="Elevate - The AI Productivity Coach", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# SESSION THEME CONTROLLER
if 'app_theme' not in st.session_state:
    st.session_state.app_theme = "Dark Cyberpunk"

apply_neon_theme(st.session_state.app_theme)
is_light = (st.session_state.app_theme == "Light Clean")

if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'nav_page' not in st.session_state:
    st.session_state.nav_page = "Dashboard"
if 'expanded_card' not in st.session_state:
    st.session_state.expanded_card = None
if 'focus_mode_active' not in st.session_state:
    st.session_state.focus_mode_active = False
if 'connected_ble_device' not in st.session_state:
    st.session_state.connected_ble_device = "Apple Watch Ultra 2 (BLE)"

# --- AUTHENTICATION SCREEN ---
if not st.session_state.user_id:
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; padding: 20px 0;">
        <div class="brand-button">⚡ Elevate</div>
        <div style="color: #94a3b8; font-size: 14px; font-weight: 700;">Support: <a href="mailto:aryanreddy2668@gmail.com" style="color:#4f46e5; text-decoration:none;">aryanreddy2668@gmail.com</a></div>
    </div>
    """, unsafe_allow_html=True)
    
    col_left_hero, col_right_auth = st.columns([1.3, 1])
    
    with col_left_hero:
        text_color = "#0f172a" if is_light else "#ffffff"
        subtext_color = "#475569" if is_light else "#94a3b8"
        st.markdown(f"""
        <div class="hd-card" style="border-left: 6px solid #4f46e5;">
            <div style="font-size: 44px; font-weight: 900; color: {text_color}; line-height: 1.1; letter-spacing: -1.5px;">The AI Productivity Coach</div>
            <div style="color: {subtext_color}; font-size: 16px; margin-top: 14px; line-height: 1.6; font-weight: 500;">
                Enterprise multi-tenant productivity engine. Combine athletic tracking with AI deep work optimization, RPG leveling, habits, and stock-style live analytics.
            </div>
            <br>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                <div style="background: rgba(79,70,229,0.05); padding: 18px; border-radius: 18px; border: 1px solid rgba(79,70,229,0.12); transition: transform 0.3s ease;">
                    <div style="font-size: 28px;">🏸</div>
                    <div style="font-weight: 800; color: {text_color}; margin-top: 6px;">Sports & Health Tasks</div>
                    <div style="font-size: 12px; color: #4f46e5;">Gym, Sprinting & Badminton</div>
                </div>
                <div style="background: rgba(16,185,129,0.05); padding: 18px; border-radius: 18px; border: 1px solid rgba(16,185,129,0.12); transition: transform 0.3s ease;">
                    <div style="font-size: 28px;">📈</div>
                    <div style="font-weight: 800; color: {text_color}; margin-top: 6px;">Live Stock Analytics</div>
                    <div style="font-size: 12px; color: #10b981;">Real-time momentum tracking</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right_auth:
        tab1, tab2 = st.tabs(["🔒 Access Workspace", "📝 Register User"])
        with tab1:
            username = st.text_input("Username", key="l_u")
            password = st.text_input("Password", type="password", key="l_p")
            if st.button("🚀 ENTER DASHBOARD", use_container_width=True):
                user_id = authenticate_user(username, password)
                if user_id:
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
        with tab2:
            new_u = st.text_input("Choose Username", key="r_u")
            new_p = st.text_input("Choose Password", type="password", key="r_p")
            new_e = st.text_input("Email (Optional)", key="r_e")
            if st.button("🔥 CREATE WORKSPACE", use_container_width=True):
                if register_user(new_u, new_p, new_e):
                    st.success("Workspace ready! Please Sign In.")
                else:
                    st.error("Username taken.")
    st.stop()

# --- TOP HEADER & THEME TOGGLE BAR ---
profile_data = get_user_profile(st.session_state.user_id)
user_subdomain = profile_data[9] if profile_data and len(profile_data) > 9 else "athlete"
user_tier = profile_data[10] if profile_data and len(profile_data) > 10 else "Pro Enterprise Tier"

h_col1, h_col2 = st.columns([2.5, 1])
with h_col1:
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:16px;">
        <div class="brand-button">⚡ Elevate</div>
        <span style="background:rgba(79,70,229,0.1); color:#4f46e5; border:1px solid rgba(79,70,229,0.3); border-radius:8px; padding:6px 12px; font-weight:900; font-size:12px;">{user_subdomain}.elevate.ai</span>
        <span style="color:{'#0f172a' if is_light else '#ffffff'}; font-weight:800; font-size:13px;">{user_tier} ✦</span>
    </div>
    """, unsafe_allow_html=True)

with h_col2:
    selected_theme = st.selectbox("🎨 Mode", ["Dark Cyberpunk", "Light Clean"], index=0 if st.session_state.app_theme == "Dark Cyberpunk" else 1, label_visibility="collapsed")
    if selected_theme != st.session_state.app_theme:
        st.session_state.app_theme = selected_theme
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# --- FETCH USER DATA ---
user_xp = profile_data[6] if profile_data and len(profile_data) > 6 else 350
user_level = profile_data[7] if profile_data and len(profile_data) > 7 else 3
freeze_tokens = profile_data[8] if profile_data and len(profile_data) > 8 else 2
boss_name, boss_max_hp, boss_cur_hp = get_boss_info()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(79, 70, 229, 0.12), rgba(16, 185, 129, 0.12)); padding:18px; border-radius:18px; border:1px solid rgba(79, 70, 229, 0.3); margin-bottom:16px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-weight:900; color:{'#0f172a' if is_light else '#ffffff'}; font-size:15px;">LEVEL {user_level} ATHLETE</span>
            <span style="color:#eab308; font-size:12px; font-weight:800;">🧊 {freeze_tokens} Tokens</span>
        </div>
        <div style="font-size:12px; color:{'#475569' if is_light else '#cbd5e1'}; margin-top:6px; font-weight:700;">XP: {user_xp} / {(user_level)*200}</div>
        <div class="xp-bar-bg" style="margin-top:10px;">
            <div class="xp-bar-fill" style="width: {min(100, int((user_xp % 200)/2))}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "Navigation", 
        ["Dashboard", "Tasks", "Habit Matrix", "Analytics", "AI Coach"], 
        index=["Dashboard", "Tasks", "Habit Matrix", "Analytics", "AI Coach"].index(st.session_state.nav_page) if st.session_state.nav_page in ["Dashboard", "Tasks", "Habit Matrix", "Analytics", "AI Coach"] else 0,
        label_visibility="collapsed"
    )
    st.session_state.nav_page = menu

    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    with st.expander(f"👤 Account Hub: {st.session_state.username}", expanded=False):
        st.caption(f"User ID: #00{st.session_state.user_id}")
        st.caption(f"Plan: {user_tier}")
        st.markdown("---")
        
        with st.form("settings_form"):
            st.markdown("##### ⚙️ Commercial Settings")
            u_email = st.text_input("Email", value=profile_data[1] if profile_data else "")
            u_tz = st.selectbox("Timezone", ["UTC", "IST", "EST", "PST"], index=1)
            u_goal = st.number_input("Weekly Goal (Hrs)", value=profile_data[4] if profile_data else 20)
            u_subd = st.text_input("Custom Subdomain", value=user_subdomain)
            if st.form_submit_button("Save Settings"):
                update_user_profile(st.session_state.user_id, u_email, u_tz, profile_data[3], u_goal, u_subd, user_tier)
                st.success("Settings Saved!")
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        export_json = export_user_data(st.session_state.user_id)
        st.download_button("📥 Export My Data (JSON)", data=export_json, file_name=f"{st.session_state.username}_data.json", mime="application/json")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign Out", use_container_width=True):
            st.session_state.user_id = None
            st.rerun()

# --- FETCH TASKS & HABITS ---
raw_tasks = get_tasks(st.session_state.user_id)
df_tasks = pd.DataFrame(raw_tasks, columns=["ID", "Title", "Category", "Priority", "Status", "TimeSpent", "CreatedAt"])
habits = get_habits(st.session_state.user_id)
score, badge = calculate_productivity_score(df_tasks)
strain, recovery, rec_advice = calculate_ai_recovery_metrics(df_tasks)

# --- VIEW 1: DASHBOARD ---
if menu == "Dashboard":
    
    # GLOBAL BOSS RAID BANNER
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.12), rgba(168, 85, 247, 0.12)); border:2px solid #ef4444; border-radius:20px; padding:18px 26px; margin-bottom:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="font-size:13px; font-weight:900; color:#ef4444; letter-spacing:1px;">⚔️ GLOBAL COMMUNITY RAID BOSS</span>
                <div style="font-size:24px; font-weight:900; color:{'#0f172a' if is_light else '#ffffff'};">{boss_name}</div>
            </div>
            <div style="text-align:right;">
                <span style="font-size:22px; font-weight:900; color:{'#0f172a' if is_light else '#ffffff'};">{boss_cur_hp} / {boss_max_hp} HP</span>
                <div style="font-size:12px; color:{'#64748b' if is_light else '#cbd5e1'}; font-weight:600;">Completing tasks attacks the boss!</div>
            </div>
        </div>
        <div class="xp-bar-bg" style="margin-top:12px;">
            <div style="background: linear-gradient(90deg, #ef4444, #f97316); height:100%; width: {int((boss_cur_hp/boss_max_hp)*100)}%; border-radius:12px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_main, col_side = st.columns([2.2, 1])

    with col_main:
        st.markdown(f"""
        <div class="hd-card">
            <div style="font-size:24px; font-weight:900; color:{'#0f172a' if is_light else '#ffffff'}; margin-bottom:18px;">📈 Performance Command Center</div>
        """, unsafe_allow_html=True)
        
        c_ring, c_stats = st.columns([1, 1.8])
        with c_ring:
            st.markdown(render_score_ring_hd(score, badge, is_light), unsafe_allow_html=True)

        with c_stats:
            st.markdown("<br>", unsafe_allow_html=True)
            completed_tasks_count = len(df_tasks[df_tasks['Status'] == 'Completed']) if not df_tasks.empty and 'Status' in df_tasks.columns else 2
            total_tasks_count = len(df_tasks) if not df_tasks.empty else 5
            
            st.markdown(f"<span style='font-size:15px; font-weight:800; color:{'#0f172a' if is_light else '#ffffff'};'>Habits Completed</span> <span style='float:right; color:#10b981; font-size:18px; font-weight:900;'>2/3</span>", unsafe_allow_html=True)
            st.progress(0.66)
            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            
            st.markdown(f"<span style='font-size:15px; font-weight:800; color:{'#0f172a' if is_light else '#ffffff'};'>Tasks Completed</span> <span style='float:right; color:#4f46e5; font-size:18px; font-weight:900;'>{completed_tasks_count}/{max(1, total_tasks_count)}</span>", unsafe_allow_html=True)
            st.progress(completed_tasks_count / max(1, total_tasks_count))

            # ANIMATED STREAKS
            st.markdown("<br>", unsafe_allow_html=True)
            s1, s2 = st.columns(2)
            with s1:
                st.markdown(f"""
                <div class="wild-streak-box">
                    <span class="flame-icon-animated">🔥</span>
                    <div style="font-size:11px; color:#f97316; font-weight:900; letter-spacing:1px; margin-top:2px;">CURRENT STREAK</div>
                    <div style="font-size:26px; font-weight:900; color:{'#0f172a' if is_light else '#ffffff'}; line-height:1.1;">4 DAYS</div>
                </div>
                """, unsafe_allow_html=True)
            with s2:
                st.markdown(f"""
                <div class="wild-streak-box" style="border-color:#db2777;">
                    <span class="flame-icon-animated">⚡</span>
                    <div style="font-size:11px; color:#db2777; font-weight:900; letter-spacing:1px; margin-top:2px;">BEST RECORD</div>
                    <div style="font-size:26px; font-weight:900; color:{'#0f172a' if is_light else '#ffffff'}; line-height:1.1;">7 DAYS</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # RE-DESIGNED PREMIUM WEARABLE & BLE DISCOVERY HUB
        st.markdown(f"""
        <div class="hd-card" style="border-left: 6px solid #4f46e5;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-size:18px; font-weight:900; color:{'#0f172a' if is_light else '#ffffff'};">⌚ Smart Wearable Telemetry & BLE Discovery</div>
                    <div style="font-size:12px; color:#4f46e5; font-weight:800; margin-top:2px;">Connected: {st.session_state.connected_ble_device}</div>
                </div>
                <span style="background:rgba(16,185,129,0.12); color:#10b981; border:1px solid #10b981; border-radius:8px; padding:4px 10px; font-size:11px; font-weight:900;">● ACTIVE SYNC</span>
            </div>
            <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:12px; margin-top:16px; text-align:center;">
                <div style="background:{'#f8fafc' if is_light else 'rgba(255,255,255,0.03)'}; padding:12px; border-radius:14px; border:1px solid {'#e2e8f0' if is_light else 'rgba(255,255,255,0.06)'};">
                    <div style="font-size:11px; color:{'#64748b' if is_light else '#94a3b8'}; font-weight:800;">HEART RATE</div>
                    <div style="font-size:22px; font-weight:900; color:#ef4444;">134 BPM</div>
                </div>
                <div style="background:{'#f8fafc' if is_light else 'rgba(255,255,255,0.03)'}; padding:12px; border-radius:14px; border:1px solid {'#e2e8f0' if is_light else 'rgba(255,255,255,0.06)'};">
                    <div style="font-size:11px; color:{'#64748b' if is_light else '#94a3b8'}; font-weight:800;">HRV VARIABILITY</div>
                    <div style="font-size:22px; font-weight:900; color:#4f46e5;">68 ms</div>
                </div>
                <div style="background:{'#f8fafc' if is_light else 'rgba(255,255,255,0.03)'}; padding:12px; border-radius:14px; border:1px solid {'#e2e8f0' if is_light else 'rgba(255,255,255,0.06)'};">
                    <div style="font-size:11px; color:{'#64748b' if is_light else '#94a3b8'}; font-weight:800;">CALORIES</div>
                    <div style="font-size:22px; font-weight:900; color:#10b981;">620 kcal</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📶 Wearable BLE Device Pairing Command Center", expanded=False):
            b_col1, b_col2 = st.columns([1.5, 1])
            with b_col1:
                st.markdown("##### 🔍 Available Nearby Bluetooth Devices")
                device_choice = st.selectbox(
                    "Discovered Fitness Devices",
                    ["Apple Watch Ultra 2 (BLE)", "Garmin Forerunner 965 (Wi-Fi)", "Polar H10 Heart Rate Strap", "Fitbit Charge 6 (BLE)"],
                    index=0
                )
                if st.button("🔗 Pair Selected Wearable"):
                    st.session_state.connected_ble_device = device_choice
                    st.success(f"Successfully paired and synched telemetry with **{device_choice}**!")
                    st.rerun()

            with b_col2:
                st.markdown("##### 🌐 Direct Browser BLE Pairing")
                st.components.v1.html("""
                <div style="text-align:center; font-family:sans-serif;">
                    <button id="bleConnect" style="background:#4f46e5; color:#fff; font-weight:bold; padding:10px 14px; border:none; border-radius:10px; cursor:pointer; font-size:12px;">
                        📶 Scan via Web Bluetooth API
                    </button>
                    <div id="bleOut" style="font-size:11px; color:#4f46e5; margin-top:8px; font-weight:bold;">Status: Ready to discover</div>
                </div>
                <script>
                    document.getElementById('bleConnect').addEventListener('click', async () => {
                        const out = document.getElementById('bleOut');
                        try {
                            out.innerText = 'Scanning for BLE devices...';
                            const device = await navigator.bluetooth.requestDevice({ filters: [{ services: ['heart_rate'] }] });
                            out.innerText = 'Paired: ' + device.name;
                        } catch(e) {
                            out.innerText = 'Browser Scan Ready (Web BLE)';
                        }
                    });
                </script>
                """, height=70)

    with col_side:
        st.markdown(f"""
        <div class="hd-card" style="border-left: 6px solid #10b981;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <span style="font-size:18px; font-weight:900; color:{'#0f172a' if is_light else '#ffffff'};">AI Insights</span>
                <span style="font-size:18px;">🔔</span>
            </div>
            <div style="background:{'#f8fafc' if is_light else 'rgba(255,255,255,0.03)'}; padding:16px; border-radius:16px; border:1px solid {'#e2e8f0' if is_light else 'rgba(255,255,255,0.06)'};">
                <div style="font-size:12px; color:#10b981; font-weight:800; letter-spacing:1px;">LIVE FEED</div>
                <div style="font-size:14px; color:{'#334155' if is_light else '#e2e8f0'}; margin-top:8px; line-height:1.6; font-weight:500;">
                    """ + generate_rule_insights(df_tasks) + """
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # LEADERBOARD
        st.markdown(f"""
        <div class="hd-card">
            <div style="font-size:18px; font-weight:900; color:{'#0f172a' if is_light else '#ffffff'}; margin-bottom:12px;">🥇 Top 0.1% Global Leaderboard</div>
        """, unsafe_allow_html=True)
        leaderboard_data = get_top_leaderboard()
        for rank, (u_name, u_xp_val, u_lvl) in enumerate(leaderboard_data, 1):
            badge_icon = "👑" if rank == 1 else ("🥈" if rank == 2 else "🥉")
            st.markdown(f"""
            <div class="leaderboard-row">
                <span style="font-weight:800; font-size:13px;">{badge_icon} #{rank} {u_name}</span>
                <span style="font-size:12px; color:#4f46e5; font-weight:900;">Lvl {u_lvl} | {u_xp_val} XP</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # TROPHY BADGES
    st.markdown(f"""
    <div style="margin: 20px 0 12px 0;">
        <div style="font-size:24px; font-weight:900; color:{'#0f172a' if is_light else '#ffffff'};">🏆 Achievement Badges</div>
    </div>
    """, unsafe_allow_html=True)
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.markdown(f"""
        <div class="trophy-card">
            <div style="font-size:36px;">🏋️‍♂️</div>
            <div style="font-weight:900; color:{'#0f172a' if is_light else '#f8fafc'}; font-size:14px; margin-top:4px;">Iron Legs</div>
            <div style="font-size:11px; color:#10b981; font-weight:800;">UNLOCKED</div>
        </div>
        """, unsafe_allow_html=True)
    with t2:
        st.markdown(f"""
        <div class="trophy-card">
            <div style="font-size:36px;">🏸</div>
            <div style="font-weight:900; color:{'#0f172a' if is_light else '#f8fafc'}; font-size:14px; margin-top:4px;">Smash Master</div>
            <div style="font-size:11px; color:#10b981; font-weight:800;">UNLOCKED</div>
        </div>
        """, unsafe_allow_html=True)
    with t3:
        st.markdown(f"""
        <div class="trophy-card">
            <div style="font-size:36px;">🧠</div>
            <div style="font-weight:900; color:{'#0f172a' if is_light else '#f8fafc'}; font-size:14px; margin-top:4px;">Flow Titan</div>
            <div style="font-size:11px; color:#eab308; font-weight:800;">80% PROGRESS</div>
        </div>
        """, unsafe_allow_html=True)
    with t4:
        st.markdown(f"""
        <div class="trophy-card">
            <div style="font-size:36px;">⚡</div>
            <div style="font-weight:900; color:{'#0f172a' if is_light else '#f8fafc'}; font-size:14px; margin-top:4px;">Cyber Athlete</div>
            <div style="font-size:11px; color:#64748b; font-weight:800;">LOCKED</div>
        </div>
        """, unsafe_allow_html=True)

    # 3D ATHLETIC MATRIX
    st.markdown(f"""
    <div style="margin: 24px 0 12px 0;">
        <div style="font-size:26px; font-weight:900; color:{'#0f172a' if is_light else '#ffffff'};">🏋️‍♂️ Athletic & Task Matrix</div>
    </div>
    """, unsafe_allow_html=True)

    cards_data = {
        "gym": {"title": "Heavy Gym Session", "icon": "🏋️‍♂️", "tag": "🔥 520 kcal | 60 mins", "subtitle": "Strength Training", "details": "Focus on compound lifts and hypertrophy."},
        "sprint": {"title": "High-Speed Sprinting", "icon": "🏃‍♂️", "tag": "⚡ 410 kcal | 30 mins", "subtitle": "Interval Sprints", "details": "Fast-twitch fiber stimulation and cardio."},
        "badminton": {"title": "Badminton Match", "icon": "🏸", "tag": "🎾 480 kcal | 45 mins", "subtitle": "Agility & Reflexes", "details": "High agility movement and court coverage."},
        "deepwork": {"title": "Deep Work Sprint", "icon": "💻", "tag": "🧠 100% Focus | 90 mins", "subtitle": "Zero Distraction", "details": "Uninterrupted deep focus logic window."},
        "meditation": {"title": "Mindful Meditation", "icon": "🧘‍♂️", "tag": "🌿 Reset | 15 mins", "subtitle": "Mental Recovery", "details": "4-7-8 rhythmic breathing recovery."},
        "hydration": {"title": "Hydration Goal", "icon": "💧", "tag": "💦 3.5 Liters Goal", "subtitle": "Conditioning", "details": "Electrolyte and fluid replenishment."}
    }

    cols1 = st.columns(3)
    for idx, key in enumerate(["gym", "sprint", "badminton"]):
        info = cards_data[key]
        is_expanded = (st.session_state.expanded_card == key)
        card_class = "expandable-sport-card-active" if is_expanded else "expandable-sport-card"
        
        with cols1[idx]:
            st.markdown(f"""
            <div class="{card_class}">
                <div style="font-size:36px; margin-bottom:8px;">{info['icon']}</div>
                <div style="font-size:18px; font-weight:900; color:{'#0f172a' if is_light else '#ffffff'};">{info['title']}</div>
                <div style="color:#4f46e5; font-size:12px; font-weight:800; margin-top:4px;">{info['tag']}</div>
                <div style="color:{'#64748b' if is_light else '#94a3b8'}; font-size:12px; margin-top:4px;">{info['subtitle']}</div>
            """, unsafe_allow_html=True)
            
            if is_expanded:
                st.markdown(f"<div style='font-size:13px; margin-top:10px; color:{'#334155' if is_light else '#e2e8f0'};'>{info['details']}</div><br>", unsafe_allow_html=True)
                if st.button("Collapse ✖️", key=f"btn_close_{key}"):
                    st.session_state.expanded_card = None
                    st.rerun()
            else:
                if st.button("Expand Intelligence 🔍", key=f"btn_exp_{key}"):
                    st.session_state.expanded_card = key
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    cols2 = st.columns(3)
    for idx, key in enumerate(["deepwork", "meditation", "hydration"]):
        info = cards_data[key]
        is_expanded = (st.session_state.expanded_card == key)
        card_class = "expandable-sport-card-active" if is_expanded else "expandable-sport-card"
        
        with cols2[idx]:
            st.markdown(f"""
            <div class="{card_class}">
                <div style="font-size:36px; margin-bottom:8px;">{info['icon']}</div>
                <div style="font-size:18px; font-weight:900; color:{'#0f172a' if is_light else '#ffffff'};">{info['title']}</div>
                <div style="color:#4f46e5; font-size:12px; font-weight:800; margin-top:4px;">{info['tag']}</div>
                <div style="color:{'#64748b' if is_light else '#94a3b8'}; font-size:12px; margin-top:4px;">{info['subtitle']}</div>
            """, unsafe_allow_html=True)
            
            if is_expanded:
                st.markdown(f"<div style='font-size:13px; margin-top:10px; color:{'#334155' if is_light else '#e2e8f0'};'>{info['details']}</div><br>", unsafe_allow_html=True)
                if st.button("Collapse ✖️", key=f"btn_close_{key}"):
                    st.session_state.expanded_card = None
                    st.rerun()
            else:
                if st.button("Expand Intelligence 🔍", key=f"btn_exp_{key}"):
                    st.session_state.expanded_card = key
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

    # HABIT & TASK COLUMNS
    st.markdown("<br>", unsafe_allow_html=True)
    c_hab, c_tsk = st.columns([1.8, 1])

    with c_hab:
        st.markdown("<div class='hd-card'>", unsafe_allow_html=True)
        hm1, hm2 = st.columns([3, 1])
        hm1.markdown(f"<div style='font-size:20px; font-weight:900; color:{'#0f172a' if is_light else '#ffffff'};'>📅 Interactive Habit Matrix</div>", unsafe_allow_html=True)
        with hm2:
            with st.popover("+ New Habit"):
                nh = st.text_input("Habit Name")
                if st.button("Save Habit") and nh:
                    add_habit(st.session_state.user_id, nh)
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        day_keys = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
        day_labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        
        for h in habits:
            st.markdown(f"<div style='font-size:15px; font-weight:800; color:{'#0f172a' if is_light else '#f8fafc'}; margin:10px 0 4px 0;'>{h[1]}</div>", unsafe_allow_html=True)
            h_cols = st.columns(7)
            for d_idx in range(7):
                is_active = h[d_idx + 2]
                btn_label = f"{day_labels[d_idx]}\n{'🔥 DONE' if is_active else '○ OFF'}"
                if h_cols[d_idx].button(btn_label, key=f"dash_h3d_{h[0]}_{day_keys[d_idx]}"):
                    toggle_habit_day(h[0], day_keys[d_idx], is_active)
                    if not is_active:
                        add_user_xp(st.session_state.user_id, 15)
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with c_tsk:
        st.markdown(f"""
        <div class="hd-card">
            <div style="font-size:18px; font-weight:900; color:{'#0f172a' if is_light else '#ffffff'}; margin-bottom:14px;">☑️ Today's Active Tasks</div>
        """, unsafe_allow_html=True)
        
        if not df_tasks.empty:
            for idx, row in df_tasks.iterrows():
                tc1, tc2 = st.columns([4, 1])
                is_done = (row['Status'] == 'Completed') if 'Status' in row else False
                if tc1.checkbox(row['Title'], value=is_done, key=f"dash_chk_{row['ID']}"):
                    if not is_done:
                        update_task_status(row['ID'], 'Completed')
                        add_user_xp(st.session_state.user_id, 30)
                        st.rerun()
                if tc2.button("🗑️", key=f"dash_del_{row['ID']}"):
                    delete_task(row['ID'])
                    st.rerun()
        else:
            st.caption("No tasks yet.")
            
        st.markdown("</div>", unsafe_allow_html=True)

# --- VIEW 2: TASKS ---
elif menu == "Tasks":
    st.markdown(f"<h2 style='color:{'#0f172a' if is_light else '#ffffff'}; font-weight:900;'>📋 Task Command Center</h2>", unsafe_allow_html=True)
    
    with st.form("sportive_task_form", clear_on_submit=True):
        st.markdown("### 🚀 Create High-Impact Sprint")
        t_title = st.text_input("Sprint Objective Title")
        c1, c2, c3 = st.columns(3)
        t_cat = c1.selectbox("Domain Category", ["Deep work", "Shallow work", "Health", "Personal"])
        t_prio = c2.selectbox("Priority Intensity", ["High 🔥", "Medium ⚡", "Low 🌱"])
        t_mins = c3.number_input("Time Block (mins)", value=45, step=15)
        
        if st.form_submit_button("🔥 LOCK IN TASK") and t_title:
            add_task(st.session_state.user_id, t_title, t_cat, t_prio, t_mins)
            add_user_xp(st.session_state.user_id, 20)
            st.success("Task Created! (+20 XP)")
            st.rerun()

    st.markdown("---")
    st.markdown("### Active Backlog")
    if not df_tasks.empty:
        for idx, row in df_tasks.iterrows():
            tc1, tc2, tc3, tc4, tc5 = st.columns([3, 1.2, 1, 1, 1])
            tc1.markdown(f"**{row['Title']}**")
            tc2.caption(f"📁 {row['Category']}")
            tc3.caption(f"⚡ {row['Priority']}")
            tc4.caption(f"⏱️ {row['TimeSpent']}m")
            if tc5.button("Delete", key=f"sp_del_{row['ID']}"):
                delete_task(row['ID'])
                st.rerun()

# --- VIEW 3: HABIT MATRIX ---
elif menu == "Habit Matrix":
    st.markdown(f"<h2 style='color:{'#0f172a' if is_light else '#ffffff'}; font-weight:900;'>📅 Habit Matrix</h2>", unsafe_allow_html=True)
    
    with st.form("habit_3d_form", clear_on_submit=True):
        hn = st.text_input("New Habit Objective Title")
        if st.form_submit_button("➕ ADD HABIT") and hn:
            add_habit(st.session_state.user_id, hn)
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    day_keys = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
    day_labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    
    for h in habits:
        st.markdown(f"""
        <div style="background:{'#ffffff' if is_light else 'rgba(15, 23, 42, 0.7)'}; border:1px solid {'#e2e8f0' if is_light else 'rgba(255,255,255,0.08)'}; border-radius:18px; padding:18px; margin-bottom:16px;">
            <div style="font-size:18px; font-weight:900; color:{'#0f172a' if is_light else '#ffffff'}; margin-bottom:12px;">{h[1]}</div>
        """, unsafe_allow_html=True)
        
        h_cols = st.columns(7)
        for d_idx in range(7):
            val = h[d_idx + 2]
            lbl = f"{day_labels[d_idx]}\n{'🔥 DONE' if val else '○ OFF'}"
            if h_cols[d_idx].button(lbl, key=f"mat_full_{h[0]}_{day_keys[d_idx]}"):
                toggle_habit_day(h[0], day_keys[d_idx], val)
                if not val:
                    add_user_xp(st.session_state.user_id, 15)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- VIEW 4: ANALYTICS ---
elif menu == "Analytics":
    st.markdown(f"<h2 style='color:{'#0f172a' if is_light else '#ffffff'}; font-weight:900;'>📊 Live Analytics & Briefings</h2>", unsafe_allow_html=True)
    
    pdf_report_txt = generate_executive_weekly_report(st.session_state.username, df_tasks)
    st.download_button("📄 Download Weekly Executive Performance Briefing (TXT)", data=pdf_report_txt, file_name=f"{st.session_state.username}_executive_briefing.txt", mime="text/plain")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div class='hd-card'><div style='font-size:18px; font-weight:900; color:#4f46e5; margin-bottom:12px;'>📈 Pace Chart (You vs Record)</div>", unsafe_allow_html=True)
    
    trend_data = pd.DataFrame({
        "Session": ["Mon AM", "Mon PM", "Tue AM", "Tue PM", "Wed AM", "Wed PM"],
        "Your_Focus": [42, 65, 58, 82, 75, 91],
        "Ghost_Best": [50, 60, 70, 75, 80, 85]
    })
    
    fig_stock = go.Figure()
    fig_stock.add_trace(go.Scatter(x=trend_data["Session"], y=trend_data["Your_Focus"], mode='lines+markers', name="Current Pace", line=dict(color='#4f46e5', width=3)))
    fig_stock.add_trace(go.Scatter(x=trend_data["Session"], y=trend_data["Ghost_Best"], mode='lines', name="Ghost Record", line=dict(color='#a855f7', width=2, dash='dash')))
    fig_stock.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#0f172a" if is_light else "#ffffff")
    st.plotly_chart(fig_stock, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- VIEW 5: AI COACH ---
elif menu == "AI Coach":
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:16px; margin-bottom:20px;">
        <div style="font-size:32px; background:#4f46e5; color:#fff; width:54px; height:54px; border-radius:16px; display:flex; align-items:center; justify-content:center;">🤖</div>
        <div>
            <div style="font-size:24px; font-weight:900; color:{'#0f172a' if is_light else '#ffffff'};">AI Coach Chatbot</div>
            <div style="color:#4f46e5; font-size:12px; font-weight:800;">● CONTEXT GROUNDED & UNDERSTANDING INTERACTOR</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    persona = st.selectbox("Coach Persona", ["Tough Love / Military 🥊", "Scientific Bio-Hacker 🔬", "Empathetic Mentor 🌿"])

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": f"Hey {st.session_state.username}! I am your AI Coach. I have your live metrics loaded. Tell me what task or workout to schedule!"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask your AI Coach..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        pending_count = len(df_tasks[df_tasks['Status'] == 'Pending']) if not df_tasks.empty and 'Status' in df_tasks.columns else 0
        live_context = {
            "username": st.session_state.username,
            "level": user_level,
            "xp": user_xp,
            "pending_count": pending_count,
            "strain": strain,
            "recovery": recovery
        }
        
        response = get_ai_coach_response_v2(st.session_state.messages, live_context, persona, st.session_state.user_id)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)
        
        if "Tool Executed" in response or "scheduled" in response.lower():
            st.rerun()