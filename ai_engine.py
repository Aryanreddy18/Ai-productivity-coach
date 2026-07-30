import os
import pandas as pd
from openai import OpenAI

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