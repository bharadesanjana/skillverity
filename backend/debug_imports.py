import sys
import os
# Ensure current dir is in path
sys.path.append(os.getcwd()) 
print(f"Sys Path: {sys.path}")

try:
    from main import app
    print("Importing app SUCCESS")
except Exception as e:
    import traceback
    traceback.print_exc()
