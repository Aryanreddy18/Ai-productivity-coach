import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from streamlit_mic_recorder import speech_to_text

from database import (
    register_user, authenticate_user, add_task, get_tasks,
    update_task_status, delete_task, get_habits, add_habit, toggle_habit_day,
    get_user_profile, update_user_profile, export_user_data, add_user_xp
)
from styles import apply_neon_theme, render_score_ring_hd
from ai_engine import calculate_productivity_score, generate_rule_insights, get_ai_coach_response

st.set_page_config(page_title="Elevate - The AI Productivity Coach", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")
apply_neon_theme()

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

# --- AUTHENTICATION SCREEN ---
if not st.session_state.user_id:
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; padding: 20px 0;">
        <div class="brand-button">⚡ Elevate</div>
        <div style="color: #94a3b8; font-size: 14px; font-weight: 700;">Support: <a href="mailto:aryanreddy2668@gmail.com" style="color:#10b981; text-decoration:none;">aryanreddy2668@gmail.com</a></div>
    </div>
    """, unsafe_allow_html=True)
    
    col_left_hero, col_right_auth = st.columns([1.3, 1])
    
    with col_left_hero:
        st.markdown("""
        <div class="hd-card" style="border-left: 6px solid #10b981;">
            <div style="font-size: 44px; font-weight: 900; color: #ffffff; line-height: 1.1; letter-spacing: -1.5px;">The AI Productivity Coach</div>
            <div style="color: #94a3b8; font-size: 16px; margin-top: 14px; line-height: 1.6; font-weight: 500;">
                Enterprise multi-tenant productivity engine. Combine athletic tracking with AI deep work optimization, RPG leveling, habits, and stock-style live analytics.
            </div>
            <br>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                <div style="background: rgba(255,255,255,0.03); padding: 18px; border-radius: 18px; border: 1px solid rgba(255,255,255,0.06);">
                    <div style="font-size: 24px;">🏸</div>
                    <div style="font-weight: 800; color: #ffffff; margin-top: 6px;">Sports & Health Tasks</div>
                    <div style="font-size: 12px; color: #64748b;">Gym, Sprinting & Badminton</div>
                </div>
                <div style="background: rgba(255,255,255,0.03); padding: 18px; border-radius: 18px; border: 1px solid rgba(255,255,255,0.06);">
                    <div style="font-size: 24px;">📈</div>
                    <div style="font-weight: 800; color: #ffffff; margin-top: 6px;">Live Stock Analytics</div>
                    <div style="font-size: 12px; color: #64748b;">Real-time momentum tracking</div>
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

# --- TOP HEADER LOGO ---
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center; padding: 10px 0 20px 0;">
    <div class="brand-button">⚡ Elevate</div>
    <div style="color:#94a3b8; font-size:14px; font-weight:700;">The AI Productivity Coach</div>
</div>
""", unsafe_allow_html=True)

# --- FETCH USER PROFILE DATA ---
profile_data = get_user_profile(st.session_state.user_id)
user_xp = profile_data[6] if profile_data and len(profile_data) > 6 else 350
user_level = profile_data[7] if profile_data and len(profile_data) > 7 else 3
freeze_tokens = profile_data[8] if profile_data and len(profile_data) > 8 else 2

# --- EXPANDED SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    # RPG LEVEL & GAMIFICATION CARD
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(99, 102, 241, 0.15)); padding:16px; border-radius:16px; border:1px solid rgba(16, 185, 129, 0.3); margin-bottom:16px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-weight:900; color:#ffffff; font-size:16px;">LEVEL {user_level} ATHLETE</span>
            <span style="color:#eab308; font-size:12px; font-weight:800;">🧊 {freeze_tokens} Freeze Tokens</span>
        </div>
        <div style="font-size:12px; color:#94a3b8; margin-top:4px;">XP: {user_xp} / {(user_level)*200}</div>
        <div class="xp-bar-bg" style="margin-top:8px;">
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

    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
    
    with st.expander(f"👤 Account Hub: {st.session_state.username}", expanded=False):
        st.caption(f"User ID: #00{st.session_state.user_id}")
        st.caption("Plan: Enterprise Commercial Tier ✦")
        st.markdown("---")
        
        with st.form("settings_form"):
            st.markdown("##### ⚙️ Account Settings")
            u_email = st.text_input("Email", value=profile_data[1] if profile_data else "")
            u_tz = st.selectbox("Timezone", ["UTC", "IST", "EST", "PST"], index=1)
            u_goal = st.number_input("Weekly Goal (Hrs)", value=profile_data[4] if profile_data else 20)
            if st.form_submit_button("Save Settings"):
                update_user_profile(st.session_state.user_id, u_email, u_tz, profile_data[3], u_goal)
                st.success("Profile Updated!")
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        export_json = export_user_data(st.session_state.user_id)
        st.download_button("📥 Export My Data (JSON)", data=export_json, file_name=f"{st.session_state.username}_data.json", mime="application/json")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign Out", use_container_width=True):
            st.session_state.user_id = None
            st.rerun()

# --- FETCH USER TASKS & HABITS ---
raw_tasks = get_tasks(st.session_state.user_id)
df_tasks = pd.DataFrame(raw_tasks, columns=["ID", "Title", "Category", "Priority", "Status", "TimeSpent", "CreatedAt"])
habits = get_habits(st.session_state.user_id)
score, badge = calculate_productivity_score(df_tasks)

# --- VIEW 1: DASHBOARD ---
if menu == "Dashboard":
    
    col_main, col_side = st.columns([2.2, 1])

    with col_main:
        st.markdown("""
        <div class="hd-card">
            <div style="font-size:24px; font-weight:900; color:#ffffff; margin-bottom:18px;">📈 Performance Command Center</div>
        """, unsafe_allow_html=True)
        
        c_ring, c_stats = st.columns([1, 1.8])
        with c_ring:
            st.markdown(render_score_ring_hd(score, badge), unsafe_allow_html=True)

        with c_stats:
            st.markdown("<br>", unsafe_allow_html=True)
            completed_tasks_count = len(df_tasks[df_tasks['Status'] == 'Completed']) if not df_tasks.empty and 'Status' in df_tasks.columns else 2
            total_tasks_count = len(df_tasks) if not df_tasks.empty else 5
            
            st.markdown(f"<span style='font-size:16px; font-weight:800;'>Habits Completed</span> <span style='float:right; color:#10b981; font-size:20px; font-weight:900;'>2/3</span>", unsafe_allow_html=True)
            st.progress(0.66)
            st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
            
            st.markdown(f"<span style='font-size:16px; font-weight:800;'>Tasks Completed</span> <span style='float:right; color:#38bdf8; font-size:20px; font-weight:900;'>{completed_tasks_count}/{max(1, total_tasks_count)}</span>", unsafe_allow_html=True)
            st.progress(completed_tasks_count / max(1, total_tasks_count))

            st.markdown("<br>", unsafe_allow_html=True)
            s1, s2 = st.columns(2)
            s1.metric("🔥 Current Streak", "4 Days")
            s2.metric("🏆 Best Streak", "7 Days")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_side:
        st.markdown("""
        <div class="hd-card" style="border-left: 6px solid #10b981;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <span style="font-size:18px; font-weight:900; color:#ffffff;">AI Insights & Feed</span>
                <span style="font-size:18px;">🔔</span>
            </div>
            <div style="background: rgba(255,255,255,0.03); padding:18px; border-radius:16px; border:1px solid rgba(255,255,255,0.06);">
                <div style="font-size:12px; color:#10b981; font-weight:800; letter-spacing:1px;">LIVE FEED</div>
                <div style="font-size:15px; color:#e2e8f0; margin-top:8px; line-height:1.6; font-weight:500;">
                    """ + generate_rule_insights(df_tasks) + """
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="hd-card">
            <div style="font-size:18px; font-weight:900; color:#ffffff; margin-bottom:12px;">⚡ Quick Action Speed-Dial</div>
        """, unsafe_allow_html=True)
        qa1, qa2 = st.columns(2)
        if qa1.button("🏋️ Add Gym", key="qa_gym"):
            add_task(st.session_state.user_id, "Gym Workout Sprint", "Health", "High 🔥", 60)
            add_user_xp(st.session_state.user_id, 25)
            st.rerun()
        if qa2.button("🏸 Badminton", key="qa_bad"):
            add_task(st.session_state.user_id, "Badminton Match", "Health", "High 🔥", 45)
            add_user_xp(st.session_state.user_id, 25)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # UNLOCKABLE TROPHY BADGES SECTION
    st.markdown("""
    <div style="margin: 20px 0 12px 0;">
        <div style="font-size:24px; font-weight:900; color:#ffffff;">🏆 Achievement Trophies & Badges</div>
    </div>
    """, unsafe_allow_html=True)
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.markdown("""
        <div class="trophy-card">
            <div style="font-size:32px;">🏋️‍♂️</div>
            <div style="font-weight:900; color:#f8fafc; font-size:14px; margin-top:4px;">Iron Legs</div>
            <div style="font-size:11px; color:#10b981; font-weight:800;">UNLOCKED</div>
        </div>
        """, unsafe_allow_html=True)
    with t2:
        st.markdown("""
        <div class="trophy-card">
            <div style="font-size:32px;">🏸</div>
            <div style="font-weight:900; color:#f8fafc; font-size:14px; margin-top:4px;">Smash Master</div>
            <div style="font-size:11px; color:#10b981; font-weight:800;">UNLOCKED</div>
        </div>
        """, unsafe_allow_html=True)
    with t3:
        st.markdown("""
        <div class="trophy-card">
            <div style="font-size:32px;">🧠</div>
            <div style="font-weight:900; color:#f8fafc; font-size:14px; margin-top:4px;">Flow Titan</div>
            <div style="font-size:11px; color:#eab308; font-weight:800;">80% PROGRESS</div>
        </div>
        """, unsafe_allow_html=True)
    with t4:
        st.markdown("""
        <div class="trophy-card">
            <div style="font-size:32px;">⚡</div>
            <div style="font-weight:900; color:#f8fafc; font-size:14px; margin-top:4px;">Cyber Athlete</div>
            <div style="font-size:11px; color:#64748b; font-weight:800;">LOCKED (LVL 5)</div>
        </div>
        """, unsafe_allow_html=True)

    # 3D ATHLETIC MATRIX
    st.markdown("""
    <div style="margin: 24px 0 12px 0;">
        <div style="font-size:26px; font-weight:900; color:#ffffff;">🏋️‍♂️ 3D Athletic & Task Interactive Matrix</div>
        <div style="color:#94a3b8; font-size:14px; font-weight:600;">Click any card to smoothly expand in-place for full intelligence report</div>
    </div>
    """, unsafe_allow_html=True)

    cards_data = {
        "gym": {
            "title": "Heavy Gym Session",
            "icon": "🏋️‍♂️",
            "tag": "🔥 520 kcal | 60 mins",
            "subtitle": "Strength & Powerbuilding Training",
            "details": "• <b>Focus Muscles:</b> Chest, Shoulders, Triceps & Core.<br>• <b>Intensity:</b> Heavy Compound Lift Sprints.<br>• <b>AI Advice:</b> Consume 500ml hydration + protein within 30 minutes post-workout."
        },
        "sprint": {
            "title": "High-Speed Sprinting",
            "icon": "🏃‍♂️",
            "tag": "⚡ 410 kcal | 30 mins",
            "subtitle": "Interval Sprints & Cardio Drive",
            "details": "• <b>Intervals:</b> 10x 100m Explosive Sprints.<br>• <b>Focus:</b> Fast-Twitch Muscle Activation & VO2 Max.<br>• <b>AI Advice:</b> Perform 5 minutes of static hamstring stretching."
        },
        "badminton": {
            "title": "Badminton Doubles Match",
            "icon": "🏸",
            "tag": "🎾 480 kcal | 45 mins",
            "subtitle": "Agility, Reflexes & Footwork",
            "details": "• <b>Agility Metrics:</b> Fast footwork, smashing power & sharp reflexes.<br>• <b>Movement:</b> High lateral court movement.<br>• <b>AI Advice:</b> Stay on toes and keep ankle joints warmed up."
        },
        "deepwork": {
            "title": "Deep Work Sprint",
            "icon": "💻",
            "tag": "🧠 100% Focus | 90 mins",
            "subtitle": "Zero-Distraction Architecture",
            "details": "• <b>Cognitive Load:</b> Maximum System Logic Formulation.<br>• <b>Environment:</b> Zero notifications, single tab focus.<br>• <b>AI Advice:</b> Rest eyes for 10 minutes following session completion."
        },
        "meditation": {
            "title": "Mindful Meditation",
            "icon": "🧘‍♂️",
            "tag": "🌿 Reset | 15 mins",
            "subtitle": "Breathing & Mental Recovery",
            "details": "• <b>Protocol:</b> 4-7-8 Rhythmic Deep Breathing.<br>• <b>Impact:</b> -25% Cortisol stress reduction.<br>• <b>AI Advice:</b> Ideal immediately following high-intensity athletic sessions."
        },
        "hydration": {
            "title": "Hydration & Electrolytes",
            "icon": "💧",
            "tag": "💦 3.5 Liters Goal",
            "subtitle": "Peak Physical Conditioning",
            "details": "• <b>Target:</b> 3.5 Liters daily water intake.<br>• <b>Balance:</b> Essential Sodium + Potassium balance.<br>• <b>AI Advice:</b> Consume 250ml water every hour during work blocks."
        }
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
                <div style="font-size:18px; font-weight:900; color:#ffffff;">{info['title']}</div>
                <div style="color:#10b981; font-size:12px; font-weight:800; margin-top:4px;">{info['tag']}</div>
                <div style="color:#94a3b8; font-size:12px; margin-top:4px;">{info['subtitle']}</div>
            """, unsafe_allow_html=True)
            
            if is_expanded:
                st.markdown(f"""
                <hr style="border-color:rgba(255,255,255,0.1); margin:12px 0;">
                <div style="font-size:13px; color:#e2e8f0; line-height:1.5;">{info['details']}</div>
                <br>
                """, unsafe_allow_html=True)
                if st.button("Close / Collapse ✖️", key=f"btn_close_{key}"):
                    st.session_state.expanded_card = None
                    st.rerun()
            else:
                if st.button("Expand Intelligence 🔍", key=f"btn_exp_{key}"):
                    st.session_state.expanded_card = key
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    cols2 = st.columns(3)
    for idx, key in enumerate(["deepwork", "meditation", "hydration"]):
        info = cards_data[key]
        is_expanded = (st.session_state.expanded_card == key)
        card_class = "expandable-sport-card-active" if is_expanded else "expandable-sport-card"
        
        with cols2[idx]:
            st.markdown(f"""
            <div class="{card_class}">
                <div style="font-size:36px; margin-bottom:8px;">{info['icon']}</div>
                <div style="font-size:18px; font-weight:900; color:#ffffff;">{info['title']}</div>
                <div style="color:#10b981; font-size:12px; font-weight:800; margin-top:4px;">{info['tag']}</div>
                <div style="color:#94a3b8; font-size:12px; margin-top:4px;">{info['subtitle']}</div>
            """, unsafe_allow_html=True)
            
            if is_expanded:
                st.markdown(f"""
                <hr style="border-color:rgba(255,255,255,0.1); margin:12px 0;">
                <div style="font-size:13px; color:#e2e8f0; line-height:1.5;">{info['details']}</div>
                <br>
                """, unsafe_allow_html=True)
                if st.button("Close / Collapse ✖️", key=f"btn_close_{key}"):
                    st.session_state.expanded_card = None
                    st.rerun()
            else:
                if st.button("Expand Intelligence 🔍", key=f"btn_exp_{key}"):
                    st.session_state.expanded_card = key
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

    # AUDIO SOUNDSCAPE CENTER & BINAURAL BEATS
    st.markdown("""
    <div class="hd-card" style="margin-top:20px;">
        <div style="font-size:20px; font-weight:900; color:#ffffff; margin-bottom:8px;">🎧 Cyberpunk Focus Audio & Binaural Beats Player</div>
        <div style="font-size:13px; color:#94a3b8; margin-bottom:12px;">Select an ambient frequency to trigger peak cognitive performance</div>
    """, unsafe_allow_html=True)
    audio_choice = st.selectbox("Audio Track Frequencies", ["Alpha Waves (432Hz Deep Focus)", "Gamma Waves (High Energy Workout)", "Rain & Ambient Focus Noise"])
    st.components.v1.html("""
    <audio controls style="width: 100%; filter: invert(100%); opacity: 0.8;">
        <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>
    """, height=50)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c_hab, c_tsk = st.columns([1.8, 1])

    with c_hab:
        st.markdown("""
        <div class="hd-card">
        """, unsafe_allow_html=True)
        
        hm1, hm2 = st.columns([3, 1])
        hm1.markdown("<div style='font-size:22px; font-weight:900; color:#ffffff;'>📅 Interactive 3D Habit Matrix</div>", unsafe_allow_html=True)
        with hm2:
            with st.popover("+ New Habit"):
                nh = st.text_input("Habit Name")
                if st.button("Save Habit") and nh:
                    add_habit(st.session_state.user_id, nh)
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        day_keys = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
        
        for h in habits:
            st.markdown(f"<div style='font-size:16px; font-weight:800; color:#f8fafc; margin:12px 0 6px 0;'>{h[1]}</div>", unsafe_allow_html=True)
            h_cols = st.columns(7)
            day_labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
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
        st.markdown("""
        <div class="hd-card">
            <div style="font-size:20px; font-weight:900; color:#ffffff; margin-bottom:16px;">☑️ Today's Active Sprints</div>
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
            st.caption("No tasks yet. Create one in Tasks tab!")
            
        st.markdown("</div>", unsafe_allow_html=True)

# --- VIEW 2: TASKS ---
elif menu == "Tasks":
    st.markdown("<h2 style='color:#ffffff; font-weight:900;'>📋 Sportive Task Command</h2>", unsafe_allow_html=True)
    
    # CYBERPUNK FULL SCREEN FOCUS TIMER OVERLAY TOGGLE
    if st.session_state.focus_mode_active:
        st.markdown("""
        <div class="cyber-focus-card">
            <div style="color:#38bdf8; font-size:14px; font-weight:800; letter-spacing:2px;">CYBERPUNK FOCUS OVERLAY ACTIVE</div>
            <div style="font-size:72px; font-weight:900; color:#ffffff; margin:16px 0;">45 : 00</div>
            <div style="color:#94a3b8; font-size:16px;">Zero Distractions. Protect your focus window.</div>
        </div>
        <br>
        """, unsafe_allow_html=True)
        if st.button("Exit Focus Overlay ✖️", key="exit_focus"):
            st.session_state.focus_mode_active = False
            st.rerun()
    else:
        if st.button("🚀 Enter Cyberpunk Focus Sprint Overlay", key="enter_focus"):
            st.session_state.focus_mode_active = True
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**🎙️ Voice Sprint Recording**")
    v_text = speech_to_text(language='en', start_prompt="🎙️ Speak Sprint Input", stop_prompt="⏹️ Stop Recording", key='mic_input')
    
    with st.form("sportive_task_form", clear_on_submit=True):
        st.markdown("### 🚀 Create High-Impact Sprint")
        def_val = v_text if v_text else ""
        t_title = st.text_input("Sprint Objective Title", value=def_val)
        c1, c2, c3 = st.columns(3)
        t_cat = c1.selectbox("Domain Category", ["Deep work", "Shallow work", "Health", "Personal"])
        t_prio = c2.selectbox("Priority Intensity", ["High 🔥", "Medium ⚡", "Low 🌱"])
        t_mins = c3.number_input("Time Block (mins)", value=45, step=15)
        
        if st.form_submit_button("🔥 LOCK IN SPRINT TASK") and t_title:
            add_task(st.session_state.user_id, t_title, t_cat, t_prio, t_mins)
            add_user_xp(st.session_state.user_id, 20)
            st.success("Sprint Locked & Created! (+20 XP)")
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
            st.divider()

# --- VIEW 3: HABIT MATRIX ---
elif menu == "Habit Matrix":
    st.markdown("<h2 style='color:#ffffff; font-weight:900;'>📅 Interactive 3D Habit Matrix</h2>", unsafe_allow_html=True)
    
    with st.form("habit_3d_form", clear_on_submit=True):
        hn = st.text_input("New Habit Objective Title")
        if st.form_submit_button("➕ ADD HABIT SPRINT") and hn:
            add_habit(st.session_state.user_id, hn)
            st.rerun()

    st.markdown("---")
    day_keys = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
    day_labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    
    for h in habits:
        st.markdown(f"### {h[1]}")
        h_cols = st.columns(7)
        for d_idx in range(7):
            val = h[d_idx + 2]
            lbl = f"{day_labels[d_idx]}\n{'🔥 DONE' if val else '○ OFF'}"
            if h_cols[d_idx].button(lbl, key=f"mat_full_{h[0]}_{day_keys[d_idx]}"):
                toggle_habit_day(h[0], day_keys[d_idx], val)
                if not val:
                    add_user_xp(st.session_state.user_id, 15)
                st.rerun()
        st.divider()

# --- VIEW 4: ANALYTICS ---
elif menu == "Analytics":
    st.markdown("<h2 style='color:#ffffff; font-weight:900;'>📊 Live Performance Analytics</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='hd-card'><div style='font-size:20px; font-weight:900; color:#10b981; margin-bottom:12px;'>📈 Productivity Momentum Trend (Stock Chart View)</div>", unsafe_allow_html=True)
    
    trend_data = pd.DataFrame({
        "Session": ["Mon AM", "Mon PM", "Tue AM", "Tue PM", "Wed AM", "Wed PM", "Thu AM"],
        "Focus_Score": [42, 65, 58, 82, 75, 91, 88]
    })
    
    fig_stock = go.Figure()
    fig_stock.add_trace(go.Scatter(
        x=trend_data["Session"], y=trend_data["Focus_Score"],
        mode='lines+markers',
        line=dict(color='#10b981', width=4),
        fill='tozeroy',
        fillcolor='rgba(16, 185, 129, 0.18)'
    ))
    fig_stock.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#ffffff", margin=dict(t=20, b=20, l=10, r=10),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)')
    )
    st.plotly_chart(fig_stock, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.markdown("<div class='hd-card'><div style='font-size:20px; font-weight:900; color:#ffffff; margin-bottom:12px;'>Time Allocation Breakdown</div>", unsafe_allow_html=True)
        donut_df = pd.DataFrame({
            "Category": ["Deep Work", "Meetings", "Shallow Tasks", "Breaks"],
            "Hours": [5.0, 1.5, 2.0, 0.8]
        })
        fig_donut = px.pie(
            donut_df, names="Category", values="Hours", hole=0.6,
            color_discrete_sequence=["#10b981", "#ef4444", "#eab308", "#ffffff"]
        )
        fig_donut.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#ffffff", showlegend=True, margin=dict(t=20, b=20, l=10, r=10)
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_a2:
        st.markdown("<div class='hd-card'><div style='font-size:20px; font-weight:900; color:#ffffff; margin-bottom:12px;'>Volume Trend Comparison</div>", unsafe_allow_html=True)
        volume_df = pd.DataFrame({
            "Week": ["W1", "W2", "W3", "W4"],
            "Completed": [12, 18, 24, 21],
            "Pending": [5, 4, 2, 3]
        })
        fig_vol = px.bar(
            volume_df, x="Week", y=["Completed", "Pending"],
            color_discrete_sequence=["#10b981", "#ef4444"]
        )
        fig_vol.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#ffffff", margin=dict(t=20, b=20, l=10, r=10)
        )
        st.plotly_chart(fig_vol, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- VIEW 5: AI COACH ---
elif menu == "AI Coach":
    st.markdown("""
    <div style="display:flex; align-items:center; gap:20px; margin-bottom:24px;">
        <div style="font-size:36px; background:#10b981; width:60px; height:60px; border-radius:18px; display:flex; align-items:center; justify-content:center;">🤖</div>
        <div>
            <div style="font-size:28px; font-weight:900; color:#ffffff;">AI Productivity Coach</div>
            <div style="color:#10b981; font-size:14px; font-weight:800; letter-spacing:0.5px;">● ACTIVE & ANALYZING PERFORMANCE DATA</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": f"Hey {st.session_state.username}! I am your AI Coach. What primary focus objective are we conquering today?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask your AI Coach..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        summary = f"Total tasks in queue: {len(df_tasks)}"
        response = get_ai_coach_response(prompt, summary)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)