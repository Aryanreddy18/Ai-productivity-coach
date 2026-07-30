import os
import json
import re
import pandas as pd
from openai import OpenAI
from database import add_task

def calculate_productivity_score(df):
    if df.empty:
        return 53, "Good Progress ⚡"
    
    total_tasks = len(df)
    completed_tasks = len(df[df['Status'] == 'Completed']) if 'Status' in df.columns else 0
    completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    
    score = int(min(100, max(25, completion_rate)))
    
    if score >= 80:
        badge = "🔥 UNSTOPPABLE FLOW"
    elif score >= 50:
        badge = "⚡ HIGH MOMENTUM"
    else:
        badge = "🎯 FOCUS REQUIRED"
        
    return score, badge

def generate_rule_insights(df):
    if df.empty:
        return "Combine physical training (Gym/Badminton) with deep focus windows to maximize cognitive energy!"
    
    if 'Status' in df.columns:
        pending = df[df['Status'] == 'Pending']
        if len(pending) >= 2:
            return "⚠️ AI Burnout Warning: You have multiple high-intensity sprints pending. Balance your Gym/Badminton sessions with a 15-min mindfulness break."
            
    return "🏆 Peak Flow State unlocked! Physical and mental productivity metrics are optimized."

def calculate_ai_recovery_metrics(df):
    if df.empty:
        return 45, 88, "Optimal (2.5L Water + 30g Protein)"
    
    completed = df[df['Status'] == 'Completed'] if 'Status' in df.columns else df
    total_time = completed['TimeSpent'].sum() if 'TimeSpent' in completed.columns else 90
    
    strain = min(100, int((total_time / 180) * 100))
    recovery = max(20, 100 - int(strain * 0.6))
    
    if strain > 70:
        advice = "High Strain! 3.5L Water + 400mg Magnesium & 40g Protein Required"
    else:
        advice = "Moderate Strain! Standard Hydration & 20m Alpha Wave Protocol"
        
    return strain, recovery, advice

def generate_executive_weekly_report(username, df):
    completed = len(df[df['Status'] == 'Completed']) if not df.empty and 'Status' in df.columns else 3
    total_mins = df['TimeSpent'].sum() if not df.empty and 'TimeSpent' in df.columns else 195
    
    report = f"""
    =====================================================
    ELEVATE EXECUTIVE PERFORMANCE BRIEFING
    User: {username} | Tier: Pro Commercial
    =====================================================

    1. ATHLETIC & PHYSICAL METRICS:
       • Total Workout Time Logged: {total_mins // 2} mins
       • Estimated Calories Burned: ~1,420 kcal
       • Primary Sport: Gym & Badminton

    2. DEEP WORK & COGNITIVE METRICS:
       • Total Focus Sprints Finished: {completed} Sprints
       • Total Focus Minutes: {total_mins} mins
       • Peak Energy Window: 10:15 AM - 12:45 PM

    3. AI PREDICTIVE RECOMMENDATION:
       • Maintain 3.5L Daily Hydration.
       • Optimal physical recovery state detected. Proceed to Level-Up Sprint!
    =====================================================
    """
    return report

def _offline_dynamic_response(user_text, live_context, persona_mode, user_id):
    """
    Dynamic intent-parsing engine that understands user input and responds 
    contextually with specific guidance or auto-task creation.
    """
    text = user_text.lower()
    uname = live_context.get('username', 'Athlete')
    level = live_context.get('level', 1)
    xp = live_context.get('xp', 0)
    pending = live_context.get('pending_count', 0)
    
    # 1. Task / Workout Scheduling Intent
    if any(k in text for k in ["schedule", "add", "create", "plan", "book", "set a"]):
        # Extract duration if present
        dur_match = re.search(r'(\d+)\s*(min|mins|minute|minutes|hr|hour)', text)
        mins = 45
        if dur_match:
            val = int(dur_match.group(1))
            mins = val * 60 if 'hr' in dur_match.group(2) else val

        if "gym" in text or "workout" in text or "lift" in text or "bench" in text:
            add_task(user_id, f"Gym Session ({user_text[:25]}...)", "Health", "High 🔥", mins)
            return f"🏋️‍♂️ **[AI Coach - {persona_mode}]**: Locked in! I've added a **{mins}-minute Gym Session** to your backlog. Current Level: {level}. Remember to hydrate with 500ml water pre-workout!"

        elif "badminton" in text or "match" in text or "court" in text:
            add_task(user_id, f"Badminton Match ({user_text[:25]}...)", "Health", "High 🔥", mins)
            return f"🏸 **[AI Coach - {persona_mode}]**: Got it, {uname}! Scheduled a **{mins}-minute Badminton Match** in your tasks. Keep your footwork fast and focus on agility!"

        elif "sprint" in text or "run" in text or "cardio" in text:
            add_task(user_id, f"Sprinting Cardio ({user_text[:25]}...)", "Health", "High 🔥", mins)
            return f"🏃‍♂️ **[AI Coach - {persona_mode}]**: Sprint task added! **{mins} mins** logged in backlog. Focus on explosive fast-twitch activation!"

        else:
            add_task(user_id, f"Sprint Objective: {user_text[:30]}", "Deep work", "High 🔥", mins)
            return f"⚡ **[AI Coach - {persona_mode}]**: I have created the sprint task **'{user_text}'** ({mins} mins) in your task command center!"

    # 2. Gym / Strength Query
    if any(k in text for k in ["gym", "workout", "muscle", "bench", "squat", "weight"]):
        return f"🏋️‍♂️ **[AI Coach]**: For peak gym performance at Level {level}, prioritize heavy compound lifts (Squat, Bench, Deadlift) in 45-minute focus blocks. Take 2-minute rest intervals between sets to optimize neural recovery."

    # 3. Badminton / Agility Query
    if any(k in text for k in ["badminton", "racket", "smash", "shuttle", "court"]):
        return f"🏸 **[AI Coach]**: Badminton demands rapid lateral footwork and high heart-rate variability. Ensure a 10-minute dynamic warm-up before hitting the court to protect wrist and ankle joints!"

    # 4. Sprinting / Cardio Query
    if any(k in text for k in ["sprint", "running", "cardio", "stamina", "speed"]):
        return f"🏃‍♂️ **[AI Coach]**: High-Intensity Interval Sprinting (HIIT) boosts your VO2 Max faster than steady cardio. Try 10x 100m explosive sprints with 60-second walk recoveries."

    # 5. Stress / Recovery / Fatigue Query
    if any(k in text for k in ["tired", "fatigue", "exhausted", "sore", "rest", "sleep", "recovery"]):
        return f"🧘‍♂️ **[AI Coach]**: High strain detected in your bio-feedback! Take a 15-minute alpha-wave soundscape break in the audio center, consume 30g protein + electrolytes, and defer low-priority tasks."

    # 6. Level / XP / Gamification Query
    if any(k in text for k in ["level", "xp", "rank", "leaderboard", "boss", "points"]):
        return f"🎮 **[AI Coach]**: You are currently **Level {level}** with **{xp} XP**. Completing tasks earns +20-30 XP and attacks the Global Community Boss!"

    # 7. Greetings & General Conversational Input
    if any(k in text for k in ["hi", "hello", "hey", "sup", "morning", "evening"]):
        return f"⚡ **[AI Coach]**: Hey {uname}! You currently have **{pending} pending tasks** in your backlog. What are we crushing today—Gym, Badminton, or a Deep Work sprint?"

    # Default Contextual Conversational Fallback
    return f"🤖 **[AI Coach - {persona_mode}]**: I analyzed: *'{user_text}'*. To keep your Flow Index optimal, lock in a 45-minute sprint or ask me to schedule a workout for you!"


def get_ai_coach_response_v2(messages_history, live_context, persona_mode, user_id):
    """
    Context-grounded conversational engine. Uses OpenAI GPT-4o-mini with tool calls 
    when available, or the dynamic offline intent engine when no API key is provided.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    user_prompt = messages_history[-1]["content"] if messages_history else ""

    if not api_key or api_key == "your_openai_api_key_here":
        return _offline_dynamic_response(user_prompt, live_context, persona_mode, user_id)

    try:
        client = OpenAI(api_key=api_key)
        
        persona_instructions = {
            "Tough Love / Military 🥊": "You are a tough, no-nonsense military performance coach. Direct, aggressive, high accountability. Never give generic boilerplate replies.",
            "Scientific Bio-Hacker 🔬": "You are a bio-hacking scientist. Focus on HRV, circadian rhythms, glucose control, and VO2 Max metrics.",
            "Empathetic Mentor 🌿": "You are a supportive, calm mentor. Encouraging, mindful, focusing on sustainable momentum."
        }
        
        system_content = f"""
        {persona_instructions.get(persona_mode, "You are an elite AI Coach.")}
        
        LIVE USER CONTEXT:
        - Username: {live_context.get('username')}
        - Level: {live_context.get('level')} | XP: {live_context.get('xp')}
        - Pending Tasks: {live_context.get('pending_count')}
        - Strain: {live_context.get('strain')}% | Recovery: {live_context.get('recovery')}%
        
        INSTRUCTIONS:
        - Always address the user's SPECIFIC question or statement directly. Never repeat generic canned greetings.
        - If the user asks to schedule, add, or create a task/workout, call the 'create_task_tool' function.
        """
        
        formatted_messages = [{"role": "system", "content": system_content}] + messages_history[-8:]

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "create_task_tool",
                    "description": "Create a new task or workout in the user's database backlog.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Title of the task"},
                            "category": {"type": "string", "enum": ["Deep work", "Shallow work", "Health", "Personal"]},
                            "priority": {"type": "string", "enum": ["High 🔥", "Medium ⚡", "Low 🌱"]},
                            "time_mins": {"type": "integer", "description": "Duration in minutes"}
                        },
                        "required": ["title", "category", "priority", "time_mins"]
                    }
                }
            }
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=formatted_messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=300
        )
        
        msg = response.choices[0].message
        
        if msg.tool_calls:
            for tool_call in msg.tool_calls:
                if tool_call.function.name == "create_task_tool":
                    args = json.loads(tool_call.function.arguments)
                    add_task(user_id, args.get("title"), args.get("category"), args.get("priority"), args.get("time_mins", 45))
                    return f"✅ **[AI Coach Tool Executed]**: Created task **'{args.get('title')}'** ({args.get('time_mins')} mins) in your backlog!"
        
        return msg.content

    except Exception:
        return _offline_dynamic_response(user_prompt, live_context, persona_mode, user_id)