import hashlib
import os

def hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((password + salt).encode()).hexdigest()

def generate_salt():
    return os.urandom(16).hex()
