from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    phone_number = Column(String(15), unique=True, nullable=False)  # Phone number as the identifier
    
    tasks = relationship("Task", back_populates="owner")  # One-to-many relationship with tasks

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    due_at = Column(DateTime(timezone=True), nullable=True)  
    priority = Column(String, default="medium")
    
    user_id = Column(Integer, ForeignKey("users.id"))  # Foreign key to associate task with user
    owner = relationship("User", back_populates="tasks")  # Relationship with User model
