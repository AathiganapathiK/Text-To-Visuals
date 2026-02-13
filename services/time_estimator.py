import re
from config.settings import co

def estimate_step_duration(step_text, skill_level, parent_topic=None):
    multipliers = {
        "beginner": 1.5,
        "intermediate": 1.0,
        "advanced": 0.7,
        "expert": 0.5
    }

    prompt = f"""
Estimate time (minutes) for task: {step_text}
Skill level: {skill_level}
Return ONLY a number.
"""

    try:
        response = co.chat(model="command-xlarge-nightly", message=prompt, max_tokens=10)
        match = re.search(r"\d+", response.text)
        base = int(match.group()) if match else 30
    except Exception:
        base = 30

    return int(base * multipliers.get(skill_level, 1.0))
