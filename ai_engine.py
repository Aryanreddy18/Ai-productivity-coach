import os
import pandas as pd
from openai import OpenAI

def calculate_productivity_score(df):
    if df.empty:
        return 53, "Good Progress ⚡"
    
    total_tasks = len(df)
    # Check for 'Status' (matching the column name created in app.py)
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
            return "⚡ High Velocity Notice: Pending sprints detected. Execute your top athletic or work task now!"
            
    return "🏆 Peak Flow State unlocked! Physical and mental productivity metrics are optimized."

def get_ai_coach_response(prompt, user_tasks_summary):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        return "🤖 [Elevate AI 3D]: Maintain athletic hydration, lock in your primary sprint (Gym, Badminton, or Deep Work), and work in 45-minute focus intervals!"
    
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are Elevate, an elite commercial AI Productivity Coach. Professional, highly motivating tone. Summary: {user_tasks_summary}"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"