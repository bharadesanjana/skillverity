import google.generativeai as genai
import json
from typing import List, Dict, Any
from app.config import settings

# Configure API Key
API_KEY = settings.GEMINI_API_KEY
if API_KEY:
    genai.configure(api_key=API_KEY)

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
        
        # 1. Try exact matches from preferred list
        for pref in preferred_order:
            for avail in available_models:
                if avail.endswith(pref): 
                    _cached_model_name = avail
                    return avail
        
        # 2. explicit fallback to first gemini model
        for avail in available_models:
            if 'gemini' in avail:
                _cached_model_name = avail
                return avail
                
    except Exception as e:
        print(f"WARNING: Parse models failed: {e}")
        
    return 'gemini-1.5-flash' # Ultimate fallback

def generate_verification_assessment(role: str, week_number: int, week_title: str, skills: List[str], tasks: List[str]) -> Dict[str, Any]:
    if not API_KEY:
        return _get_fallback_assessment(week_number)
        
    model = genai.GenerativeModel(get_model_name())
    
    skills_str = ", ".join(skills)
    tasks_str = ", ".join([str(t) for t in tasks]) # tasks might be objects or strings
    
    prompt = f"""
    You are Antigravity AI, acting as a senior software engineer and technical interviewer.

    Your task is to generate REAL skill verification assessments.

    ABSOLUTE RULES:
    - DO NOT generate MCQs or options like A/B/C/D
    - DO NOT generate generic or theoretical questions
    - DO NOT repeat roadmap text as questions
    - DO NOT be vague, motivational, or educational

    You MUST:
    - Generate practical, open-ended, scenario-based questions
    - Tailor questions strictly to the provided roadmap content
    - Assume the user wants job-ready validation, not practice quizzes
    - Think like you are deciding whether to hire this person

    If the assessment cannot verify skill in real-world conditions, it is INVALID.
    Generate a REAL-TIME skill verification assessment.

    Context:
    Role: {role}
    Week: {week_number}
    Week Title: {week_title}

    Roadmap Skills for this week:
    {skills_str}

    Tasks already assigned in roadmap:
    {tasks_str}

    Rules for quiz generation:
    - Questions must be derived DIRECTLY from the listed skills and tasks
    - No MCQs, no true/false, no one-line answers
    - Each question must require reasoning, explanation, or code
    - Include at least:
      • 1 debugging scenario
      • 1 design or architecture question
      • 1 implementation or pseudo-code question

    Question difficulty:
    - Entry to mid-level internship standard
    - Must be answerable without internet search
    - Must expose shallow understanding

    Output STRICT JSON ONLY in this structure:

    {{
      "week": {week_number},
      "assessment_type": "practical_skill_verification",
      "questions": [
        {{
          "id": 1,
          "type": "debugging | implementation | design | explanation",
          "question": "",
          "expected_skills_tested": [],
          "evaluation_criteria": [
            "What a strong answer must include"
          ]
        }}
      ]
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        return data
    except Exception as e:
        print(f"Error generating assessment: {e}")
        return _get_fallback_assessment(week_number)

def evaluate_response(role: str, week_number: int, skill_focus: str, question: str, user_answer: str) -> Dict[str, Any]:
    if not API_KEY:
        return _get_fallback_evaluation()

    model = genai.GenerativeModel(get_model_name())
    
    prompt = f"""
    You are evaluating a candidate’s response.

    Context:
    Role: {role}
    Week: {week_number}
    Skill Focus: {skill_focus}

    Question:
    {question}

    User Answer:
    {user_answer}

    Evaluation rules:
    - Be strict and realistic
    - Penalize memorized or shallow responses
    - Reward clarity, tradeoffs, and correct reasoning
    - Assume the candidate is applying for internships or entry-level roles

    Return JSON ONLY:

    {{
      "score": number (0–100),
      "level": "Beginner | Entry-Ready | Intern-Ready | Strong",
      "strengths": [],
      "weaknesses": [],
      "verdict": "Hire / Borderline / Reject",
      "feedback": "Blunt but constructive feedback"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        return data
    except Exception as e:
        print(f"Error assessing response: {e}")
        return _get_fallback_evaluation()

def generate_followup(summary: str) -> Dict[str, Any]:
    if not API_KEY:
        return {}

    model = genai.GenerativeModel(get_model_name())

    prompt = f"""
    Based on the user's performance summary below, generate ONE adaptive follow-up question.

    Performance Summary:
    {summary}

    Rules:
    - Target the weakest identified skill
    - Question must be harder than previous
    - No repetition of concepts
    - Question must expose gaps clearly

    Return JSON:

    {{
      "follow_up_question": "",
      "skill_targeted": "",
      "difficulty": "Medium | Hard"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        return data
    except Exception as e:
        print(f"Error generating follow-up: {e}")
        return {}

def _get_fallback_assessment(week_number):
    return {
        "week": week_number,
        "assessment_type": "practical_skill_verification",
        "questions": [
            {
                "id": 1,
                "type": "explanation",
                "question": "Explain the core concept of this week's topic in your own words.",
                "expected_skills_tested": ["Communication", "Core Concept"],
                "evaluation_criteria": ["Clarity", "Accuracy"]
            }
        ]
    }

def _get_fallback_evaluation():
    return {
        "score": 50,
        "level": "Beginner",
        "strengths": ["Answer provided"],
        "weaknesses": ["Could not evaluate (API Error)"],
        "verdict": "Borderline",
        "feedback": "System is currently offline, please try again."
    }
