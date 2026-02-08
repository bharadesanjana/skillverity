import sys
import os

sys.path.append(os.getcwd())

try:
    print("Importing schemas...")
    from app import schemas
    print("Schemas imported. Checking TokenData...")
    print(f"TokenData: {schemas.TokenData}")
    
    print("Importing deps...")
    from app import deps
    print("Deps imported.")
    
except Exception as e:
    print(f"IMPORT ERROR: {e}")
    import traceback
    traceback.print_exc()
