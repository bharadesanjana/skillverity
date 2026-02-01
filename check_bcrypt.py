from passlib.context import CryptContext

try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hash = pwd_context.hash("secret")
    print(f"Hash success: {hash}")
    print("Bcrypt is working correctly.")
except Exception as e:
    print(f"Error: {e}")
