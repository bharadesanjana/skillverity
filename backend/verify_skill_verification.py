import requests
import json

BASE_URL = "http://localhost:8000"

def run_verification():
    print("--- Verifying Real Skill Verification ---")
    
    # 1. Generate Assessment
    print("\n1. Generating Assessment...")
    payload = {
        "role": "Frontend Developer",
        "week": 1,
        "title": "Component Architecture",
        "skills": ["React Components", "Props", "State"],
        "tasks": ["Build a reusable button", "Refactor a class component"]
    }
    
    try:
        resp = requests.post(f"{BASE_URL}/verification/generate", json=payload)
        if resp.status_code == 200:
            assessment = resp.json()
            print("✅ Assessment Generated:")
            print(json.dumps(assessment, indent=2))
        else:
            print(f"❌ Generation Failed: {resp.text}")
            return
    except Exception as e:
        print(f"❌ Generation Error: {e}")
        return

    # 2. Evaluate Response
    print("\n2. Evaluating Mock Response...")
    # Use a question from the generated assessment if possible, or a mock one
    question_text = "Explain how you would design a reusable Button component that supports variants."
    if assessment.get("questions"):
        question_text = assessment["questions"][0]["question"]

    eval_payload = {
        "role": "Frontend Developer",
        "week": 1,
        "skill_focus": "React Components",
        "question": question_text,
        "answer": "I would use props for variants like primary and secondary. I'd use a switch statement to apply classes."
    }

    try:
        eval_resp = requests.post(f"{BASE_URL}/verification/evaluate", json=eval_payload)
        if eval_resp.status_code == 200:
            evaluation = eval_resp.json()
            print("✅ Evaluation Received:")
            print(json.dumps(evaluation, indent=2))
        else:
            print(f"❌ Evaluation Failed: {eval_resp.text}")
            return
    except Exception as e:
        print(f"❌ Evaluation Error: {e}")
        return

    # 3. Generate Follow-up
    print("\n3. Generating Follow-up...")
    followup_payload = {
        "summary": "Candidate understands props but relies on switch statements for styling. Suggests weak knowledge of composition or modern CSS-in-JS patterns."
    }

    try:
        follow_resp = requests.post(f"{BASE_URL}/verification/followup", json=followup_payload)
        if follow_resp.status_code == 200:
            followup = follow_resp.json()
            print("✅ Follow-up Generated:")
            print(json.dumps(followup, indent=2))
        else:
            print(f"❌ Follow-up Failed: {follow_resp.text}")
            return
    except Exception as e:
        print(f"❌ Follow-up Error: {e}")
        return

if __name__ == "__main__":
    run_verification()
