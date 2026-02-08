import os
import sys

# Clean logs
print("Cleaning logs...")
for f in ["gen_error.log", "debug_models.txt"]:
    if os.path.exists(f):
        try:
            os.remove(f)
            print(f"Removed {f}")
        except Exception as e:
            print(f"Failed to remove {f}: {e}")

# Run verify
print("Running verification...")
import verify_hq_quiz
# verify_hq_quiz runs automatically if main, but here we import it.
# The script verify_hq_quiz.py has `if __name__ == "__main__": run_verification()`
# But it also calls `run_verification()` at the end?
# Let's check verify_hq_quiz.py content.
# It has `if __name__ == "__main__": run_verification()`? 
# No, my last write to it (Step 992) had:
# `...from app.services import ai_roadmap... print... try...`
# It has high-level code, not a function.
# So importing it runs it.
