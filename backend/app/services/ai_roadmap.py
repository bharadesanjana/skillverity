import google.generativeai as genai
import os
import json
from typing import List, Dict, Any

from app.config import settings

# Configure API Key
API_KEY = settings.GEMINI_API_KEY

# Cache for model name
_cached_model_name = None

def get_model_name():
    global _cached_model_name
    if _cached_model_name:
        return _cached_model_name
    
    try:
        if not API_KEY:
            return 'gemini-1.5-flash'
            
        # Prioritize recent models
        preferred_order = ['gemini-flash-latest', 'gemini-pro-latest', 'gemini-2.0-flash-lite-001']
        
        # Check available models
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        # Debug: print(f"Available: {available_models}")

        # 1. Try exact matches from preferred list
        for pref in preferred_order:
            for avail in available_models:
                if avail.endswith(pref): 
                    _cached_model_name = avail
                    # Debug: print(f"Selected: {avail}")
                    return avail
        
        # 2. explicit fallback to first gemini model
        for avail in available_models:
            if 'gemini' in avail:
                _cached_model_name = avail
                return avail
                
    except Exception as e:
        print(f"WARNING: Parse models failed: {e}")
        
    return 'gemini-1.5-flash' # Ultimate fallback

def generate_roadmap_content(role: str, duration_weeks: int = 6) -> Dict[str, Any]:
    """
    Generates a rigorous, job-ready roadmap with weekly quizzes and final assessment.
    """
    if not API_KEY:
        print("WARNING: GEMINI_API_KEY not found. Using fallback data.")
        return get_fallback_data(role, duration_weeks)

    model_name = get_model_name()
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""
    You are a senior curriculum architect, technical interviewer, and certification designer.

    GOAL:
    Design a job-seeking-ready learning and evaluation system for a specific role.
    The output must be rigorous, practical, and industry-aligned.

    ROLE:
    {role}

    DURATION:
    {duration_weeks} weeks

    SYSTEM REQUIREMENTS:

    1. WEEKLY ROADMAP (HIGH QUALITY)
    - Each week must focus on job-relevant skills only.
    - Avoid generic theory.
    - Emphasize hands-on tasks, real-world scenarios, and interview relevance.

    2. WEEKLY TASKS + WEEKLY QUIZ
    For EACH week:
    - Provide practical tasks (coding, building, analyzing).
    - Provide a WEEKLY QUIZ with 5 questions.
    - Questions MUST be strictly related to that week's topics.
    - Difficulty: Medium to Hard.

    3. FINAL ASSESSMENT (MANDATORY)
    - Generate ONE FINAL TEST that covers all weeks.
    - 10 Questions total.
    - Difficulty: HARD.

    4. BADGE & EVALUATION SYSTEM
    - Define output for Beginner, Intermediate, Expert levels.

    STRICT OUTPUT RULES:
    - Output ONLY valid JSON.
    - No explanations, no markdown.
    - JSON must be parseable.

    OUTPUT STRUCTURE (STRICT):

    {{
      "role": "{role}",
      "duration_weeks": {duration_weeks},
      "roadmap": [
        {{
          "week": 1,
          "focus": "string",
          "topics": ["string"],
          "tasks": ["string"],
          "weekly_quiz": [
            {{
              "id": 1,
              "text": "Question text?",
              "type": "MCQ",
              "options": ["Option A", "Option B", "Option C", "Option D"],
              "correct_option": 0,
              "difficulty": "medium"
            }}
          ]
        }}
      ],
      "final_assessment": {{
        "total_questions": 10,
        "difficulty": "hard",
        "questions": [
            {{
              "id": 1,
              "text": "Final Question text?",
              "type": "MCQ",
              "options": ["A", "B", "C", "D"],
              "correct_option": 0
            }}
        ]
      }},
      "evaluation_levels": {{
        "beginner": "0-49%",
        "intermediate": "50-79%",
        "expert": "80-100%"
      }},
      "badges": {{
        "beginner": "Learning in Progress",
        "intermediate": "Skill-Qualified",
        "expert": "Skill-Verified"
      }},
      "improvement_guidance": {{
        "beginner": ["Daily practice", "Revisit basics"],
        "intermediate": ["Build complex projects", "Contribute to open source"]
      }}
    }}
    
    BEGIN GENERATION NOW.
    """

    try:
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        return data
    except Exception as e:
        print(f"DEBUG: Gemini generation failed: {e}")
        return get_fallback_data(role, duration_weeks)

def get_fallback_data(role: str, duration_weeks: int = 6):
    """Fallback with new structure"""
    print(f"DEBUG: Using fallback data for {role} ({duration_weeks} weeks)")
    
    weeks = []
    for i in range(1, duration_weeks + 1):
        weeks.append({
            "week": i,
            "focus": f"Week {i} Core Skills",
            "topics": ["Topic A", "Topic B", "Topic C"],
            "tasks": ["Build a small project", "Solve 5 LeetCode problems"],
            "weekly_quiz": [
                {
                    "id": 1,
                    "text": f"Fallback Question 1 for Week {i}?",
                    "type": "MCQ",
                    "options": ["Opt A", "Opt B", "Opt C", "Opt D"],
                    "correct_option": 0,
                    "difficulty": "medium"
                },
                {
                    "id": 2,
                    "text": f"Fallback Question 2 for Week {i}?",
                    "type": "MCQ",
                    "options": ["Opt A", "Opt B", "Opt C", "Opt D"],
                    "correct_option": 1,
                    "difficulty": "medium"
                },
                {
                    "id": 3,
                    "text": f"Fallback Question 3 for Week {i}?",
                    "type": "MCQ",
                    "options": ["Opt A", "Opt B", "Opt C", "Opt D"],
                    "correct_option": 2,
                    "difficulty": "medium"
                },
                {
                    "id": 4,
                    "text": f"Fallback Question 4 for Week {i}?",
                    "type": "MCQ",
                    "options": ["Opt A", "Opt B", "Opt C", "Opt D"],
                    "correct_option": 3,
                    "difficulty": "medium"
                },
                {
                    "id": 5,
                    "text": f"Fallback Question 5 for Week {i}?",
                    "type": "MCQ",
                    "options": ["Opt A", "Opt B", "Opt C", "Opt D"],
                    "correct_option": 0,
                    "difficulty": "medium"
                }
            ]
        })

    return {
        "role": role,
        "duration_weeks": duration_weeks,
        "roadmap": weeks,
        "final_assessment": {
            "total_questions": 10,
            "difficulty": "hard",
            "questions": []
        },
        "evaluation_levels": {
            "beginner": "0-49%",
            "intermediate": "50-79%",
            "expert": "80-100%"
        },
        "badges": {
            "beginner": "Learning in Progress",
            "intermediate": "Skill-Qualified",
            "expert": "Skill-Verified"
        },
        "improvement_guidance": {
            "beginner": ["Practice more"],
            "intermediate": ["Build more"]
        }
    }

def generate_weekly_quiz(role: str, week_number: int, focus: str, topics: str, tasks: str) -> List[Dict[str, Any]]:
    """
    Generates a rigorous weekly quiz based on strict topics and tasks.
    """
    if not API_KEY:
        print("WARNING: GEMINI_API_KEY not found. Using fallback quiz.")
        return get_fallback_quiz(focus)

    model_name = get_model_name()
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""
    You are a senior technical interviewer and assessment designer.

    CONTEXT:
    The learner has selected a specific ROLE and is currently in a specific WEEK of the roadmap.
    Each week already has clearly defined TOPICS and TASKS.

    TASK:
    Generate a WEEKLY QUIZ that is STRICTLY aligned to the selected topics.
    The quiz must evaluate real understanding, not surface-level memory.

    ROLE:
    {role}

    WEEK NUMBER:
    {week_number}

    WEEK FOCUS:
    {focus}

    WEEK TOPICS (IMPORTANT — DO NOT IGNORE):
    {topics}

    WEEK TASKS (for context):
    {tasks}

    QUIZ REQUIREMENTS:
    1. ALL questions MUST be directly derived from the given WEEK TOPICS.
    2. DO NOT generate generic or placeholder questions.
    3. DO NOT ask questions unrelated to the week (no future or past topics).
    4. Assume the learner has completed the week’s tasks.

    QUESTION DESIGN RULES:
    - Difficulty: Medium to Hard
    - Questions must feel like:
      - Real interview screening questions
      - Practical decision-making scenarios
      - Avoid factual recall unless necessary.

    QUESTION TYPES (MIX REQUIRED):
    - MCQ
    - Scenario-based reasoning
    - Debugging / logic-based (conceptual, not code-heavy)

    NUMBER OF QUESTIONS:
    8–10 questions

    STRICT OUTPUT RULES:
    - Output ONLY valid JSON
    - No explanations, no markdown, no filler text
    - JSON must be parseable using JSON.parse()

    OUTPUT FORMAT (STRICT):

    {{
      "role": "{role}",
      "week": {week_number},
      "focus": "{focus}",
      "quiz": [
        {{
          "question": "string",
          "options": ["string", "string", "string", "string"],
          "correct_answer_index": 0,
          "type": "MCQ | Scenario | Debugging",
          "difficulty": "medium | hard",
          "topic": "string"
        }}
      ]
    }}

    QUALITY BAR (IMPORTANT):
    If a question can be answered without understanding the given WEEK TOPICS,
    it is considered INVALID and must not be generated.

    FAIL-SAFE INSTRUCTION:
    If unsure, reduce question count but NEVER reduce relevance.

    BEGIN GENERATION NOW.
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        
        normalized_questions = []
        for i, q in enumerate(data.get("quiz", [])):
            normalized_questions.append({
                "id": i + 1,
                "text": q.get("question"),
                "options": q.get("options"),
                "correct_option": q.get("correct_answer_index"),
                "type": q.get("type"),
                "difficulty": q.get("difficulty")
            })
            
        return normalized_questions
        
    except Exception as e:
        print(f"DEBUG: Quiz generation failed: {e}")
        return get_fallback_quiz(focus)

def get_fallback_quiz(topic: str) -> List[Dict[str, Any]]:
    return [
        {
            "id": 1,
            "text": f"What is a key concept of {topic}?",
            "options": ["Concept A", "Concept B", "Concept C", "Concept D"],
            "correct_option": 0
        },
        {
            "id": 2,
            "text": "Which of these is best practice?",
            "options": ["Bad approach", "Good approach", "Worst approach", "Lazy approach"],
            "correct_option": 1
        },
        {
            "id": 3,
            "text": "How do you handle errors in this context?",
            "options": ["Ignore them", "Print them", "Try/Catch or equivalent", "Exit immediately"],
            "correct_option": 2
        },
        {
            "id": 4,
            "text": "What is the complexity of the standard algorithm?",
            "options": ["O(1)", "O(n)", "O(n^2)", "O(log n)"],
            "correct_option": 1
        },
        {
            "id": 5,
            "text": "Why is this topic important?",
            "options": ["It is not", "Scalability", "Just for fun", "Legacy reasons"],
            "correct_option": 1
        }
    ]
