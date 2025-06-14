'''from sqlalchemy import Column, Integer, String, Text, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    phone = Column(String)
    profile_pic = Column(String)
    recipes = relationship("Recipe", back_populates="user")

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    input_text = Column(Text)
    category = Column(String)
    cuisine = Column(String)          # ✅ NEW
    health_pref = Column(String)      # ✅ NEW
    recipe_output = Column(Text)

    user = relationship("User", back_populates="recipes")


engine = create_engine("sqlite:///database/users.db")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
'''

from sqlalchemy import Column, Integer, String, Text, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    phone = Column(String)
    profile_pic = Column(String)
    recipes = relationship("Recipe", back_populates="user")

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    input_text = Column(Text)
    category = Column(String)
    cuisine = Column(String)          # ✅ NEW
    health_pref = Column(String)      # ✅ NEW
    recipe_output = Column(Text)

    user = relationship("User", back_populates="recipes")

# ✅ Use consistent database path
DATABASE_URL = "sqlite:///users.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# ✅ Add this function for first-time creation
def create_database():
    if not os.path.exists("users.db"):
        Base.metadata.create_all(engine)
