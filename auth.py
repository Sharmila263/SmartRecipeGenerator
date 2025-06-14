from db import SessionLocal, User
from utils.hashing import hash_password, generate_salt
import os

def register_user(name, email, password, phone, profile_pic):
    db = SessionLocal()
    if db.query(User).filter(User.email == email).first():
        return False, "Email already registered"
    
    salt = generate_salt()
    hashed = hash_password(password, salt)
    full_password = f"{salt}${hashed}"
    
    new_user = User(name=name, email=email, password=full_password, phone=phone, profile_pic=profile_pic)
    db.add(new_user)
    db.commit()
    return True, "Registered successfully"

def login_user(email, password):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    if user:
        salt, stored_hash = user.password.split('$')
        if hash_password(password, salt) == stored_hash:
            return True, user
    return False, None
