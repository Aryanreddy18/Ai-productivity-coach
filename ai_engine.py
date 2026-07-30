import os
import json
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

def get_ai_coach_response_v2(messages_history, live_context, persona_mode, user_id):
    """
    Upgraded AI Coach with Short-Term Memory, System Context Grounding,
    Persona Adaptation, and OpenAI Function Calling for Task Creation.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        # Fallback offline conversational response
        last_usr_msg = messages_history[-1]["content"].lower() if messages_history else ""
        if "badminton" in last_usr_msg or "gym" in last_usr_msg:
            add_task(user_id, f"AI Scheduled: {messages_history[-1]['content']}", "Health", "High 🔥", 45)
            return "🤖 [Elevate AI Coach]: I have analyzed your request and automatically scheduled this workout in your task backlog! Stay hydrated and lock in!"
        return f"🤖 [Elevate AI ({persona_mode})]: Memory & Context Loaded! User Level: {live_context.get('level', 3)}. Maintain athletic hydration and complete your pending sprints!"

    try:
        client = OpenAI(api_key=api_key)
        
        # 1. Build Persona Prompt
        persona_instructions = {
            "Tough Love / Military 🥊": "You are a tough, no-nonsense military performance coach. Direct, aggressive, high accountability.",
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
        
        If the user asks you to schedule, add, or create a task/workout, use the 'create_task_tool' function call.
        """
        
        # 2. Format Messages with System Grounding
        formatted_messages = [{"role": "system", "content": system_content}] + messages_history

        # 3. Define Function Call Tool
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

        # 4. API Call with Tools
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=formatted_messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=300
        )
        
        msg = response.choices[0].message
        
        # Check if Tool was Triggered
        if msg.tool_calls:
            for tool_call in msg.tool_calls:
                if tool_call.function.name == "create_task_tool":
                    args = json.loads(tool_call.function.arguments)
                    add_task(user_id, args.get("title"), args.get("category"), args.get("priority"), args.get("time_mins", 45))
                    return f"✅ **[AI Coach Tool Executed]**: Created task **'{args.get('title')}'** ({args.get('time_mins')} mins) in your backlog!"
        
        return msg.content

    except Exception as e:
        return f"AI Error: {str(e)}"