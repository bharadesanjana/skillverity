import sys
import os

# Add the current directory to sys.path so we can import app
sys.path.append(os.getcwd())

from app.services import ai_verification
from app.config import settings

result = []
result.append(f"API Key present: {bool(settings.GEMINI_API_KEY)}")

try:
    result.append("Testing generate_verification_assessment...")
    assessment = ai_verification.generate_verification_assessment(
        role="Frontend Developer",
        week_number=1,
        week_title="Test Week",
        skills=["React", "CSS"],
        tasks=["Build a button"]
    )
    result.append(f"Assessment result: {assessment}")
except Exception as e:
    result.append(f"Assessment failed with error: {e}")

try:
    result.append("\nTesting evaluate_response...")
    evaluation = ai_verification.evaluate_response(
        role="Frontend Developer",
        week_number=1,
        skill_focus="React",
        question="Explain Props",
        user_answer="Props are arguments passed into React components."
    )
    result.append(f"Evaluation result: {evaluation}")
except Exception as e:
    result.append(f"Evaluation failed with error: {e}")

with open("debug_result.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(result))
