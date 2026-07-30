import sqlite3
import hashlib
import os
import json

DB_NAME = "productivity_coach.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16).hex()
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"{salt}${key.hex()}"

def verify_password(stored_password, provided_password):
    try:
        salt, stored_hash = stored_password.split('$')
        key = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return key.hex() == stored_hash
    except Exception:
        return False

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    # 1. Base Users Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # AUTO-MIGRATION: Ensure Gamification, RPG, Subdomain & Subscription columns exist
    c.execute("PRAGMA table_info(users);")
    existing_columns = [col[1] for col in c.fetchall()]
    
    missing_columns = {
        "email": "TEXT DEFAULT ''",
        "timezone": "TEXT DEFAULT 'UTC'",
        "sports_preference": "TEXT DEFAULT 'Gym & Badminton'",
        "weekly_goal_hours": "INTEGER DEFAULT 20",
        "xp": "INTEGER DEFAULT 350",
        "level": "INTEGER DEFAULT 3",
        "freeze_tokens": "INTEGER DEFAULT 2",
        "subdomain": "TEXT DEFAULT 'athlete'",
        "tier": "TEXT DEFAULT 'Pro Enterprise Tier'"
    }
    
    for col_name, col_def in missing_columns.items():
        if col_name not in existing_columns:
            c.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_def};")
    
    # 2. Tasks Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            time_spent_mins INTEGER DEFAULT 0,
            created_at DATE DEFAULT CURRENT_DATE,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    # 3. Habits Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            sun INTEGER DEFAULT 0,
            mon INTEGER DEFAULT 0,
            tue INTEGER DEFAULT 1,
            wed INTEGER DEFAULT 1,
            thu INTEGER DEFAULT 0,
            fri INTEGER DEFAULT 1,
            sat INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    # 4. Boss Raid Global Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS boss_raid (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            boss_name TEXT DEFAULT 'Procrastination Behemoth',
            max_hp INTEGER DEFAULT 10000,
            current_hp INTEGER DEFAULT 6420
        )
    ''')
    
    c.execute("SELECT COUNT(*) FROM boss_raid")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO boss_raid (boss_name, max_hp, current_hp) VALUES ('Procrastination Behemoth', 10000, 6420)")

    c.execute("CREATE INDEX IF NOT EXISTS idx_tasks_user ON tasks(user_id);")
    c.execute("CREATE INDEX IF NOT EXISTS idx_habits_user ON habits(user_id);")
    
    conn.commit()
    conn.close()

def register_user(username, password, email=""):
    conn = get_connection()
    c = conn.cursor()
    try:
        hashed_p = hash_password(password)
        c.execute("INSERT INTO users (username, password, email, xp, level, freeze_tokens) VALUES (?, ?, ?, 100, 1, 2)", (username, hashed_p, email))
        user_id = c.lastrowid
        
        default_habits = [
            (user_id, "Heavy Gym Powerbuilding 🏋️‍♂️", 0, 0, 1, 1, 0, 1, 0),
            (user_id, "Badminton Match Agility 🏸", 0, 0, 1, 1, 1, 1, 1),
            (user_id, "Sprinting High-Intensity Cardio 🏃‍♂️", 0, 0, 1, 0, 1, 1, 1)
        ]
        c.executemany("INSERT INTO habits (user_id, name, sun, mon, tue, wed, thu, fri, sat) VALUES (?,?,?,?,?,?,?,?,?)", default_habits)
        
        default_tasks = [
            (user_id, "Gym Heavy Bench & Squats", "Health", "High 🔥", "Completed", 60),
            (user_id, "Badminton Match Doubles", "Health", "High 🔥", "Pending", 45),
            (user_id, "Deep Work Software Sprint", "Deep work", "High 🔥", "Completed", 90)
        ]
        c.executemany("INSERT INTO tasks (user_id, title, category, priority, status, time_spent_mins) VALUES (?,?,?,?,?,?)", default_tasks)

        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row and verify_password(row[1], password):
        return row[0]
    return None

def get_user_profile(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT username, email, timezone, sports_preference, weekly_goal_hours, created_at, xp, level, freeze_tokens, subdomain, tier FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row

def get_top_leaderboard():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT username, xp, level FROM users ORDER BY xp DESC LIMIT 5")
    rows = c.fetchall()
    conn.close()
    return rows

def add_user_xp(user_id, xp_gained):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT xp, level FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    if row:
        new_xp = row[0] + xp_gained
        new_level = (new_xp // 200) + 1
        c.execute("UPDATE users SET xp = ?, level = ? WHERE id = ?", (new_xp, new_level, user_id))
        
        # Attack the global boss!
        c.execute("UPDATE boss_raid SET current_hp = MAX(0, current_hp - ?) WHERE id = 1", (xp_gained * 2,))
        conn.commit()
    conn.close()

def get_boss_info():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT boss_name, max_hp, current_hp FROM boss_raid WHERE id = 1")
    row = c.fetchone()
    conn.close()
    return row if row else ("Procrastination Behemoth", 10000, 6420)

def update_user_profile(user_id, email, timezone, sports_pref, goal_hours, subdomain="athlete", tier="Pro Enterprise Tier"):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        UPDATE users 
        SET email = ?, timezone = ?, sports_preference = ?, weekly_goal_hours = ?, subdomain = ?, tier = ?
        WHERE id = ?
    """, (email, timezone, sports_pref, goal_hours, subdomain, tier, user_id))
    conn.commit()
    conn.close()

def add_task(user_id, title, category, priority, time_spent=0):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO tasks (user_id, title, category, priority, time_spent_mins) VALUES (?, ?, ?, ?, ?)",
        (user_id, title, category, priority, time_spent)
    )
    conn.commit()
    conn.close()

def get_tasks(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, title, category, priority, status, time_spent_mins, created_at FROM tasks WHERE user_id = ?", (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_habits(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, sun, mon, tue, wed, thu, fri, sat FROM habits WHERE user_id = ?", (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def add_habit(user_id, habit_name):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO habits (user_id, name) VALUES (?, ?)", (user_id, habit_name))
    conn.commit()
    conn.close()

def toggle_habit_day(habit_id, day_col, current_val):
    new_val = 0 if current_val == 1 else 1
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"UPDATE habits SET {day_col} = ? WHERE id = ?", (new_val, habit_id))
    conn.commit()
    conn.close()

def update_task_status(task_id, status):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def export_user_data(user_id):
    tasks = get_tasks(user_id)
    habits = get_habits(user_id)
    profile = get_user_profile(user_id)
    
    return json.dumps({
        "profile": profile,
        "tasks": tasks,
        "habits": habits
    }, indent=4)

init_db()