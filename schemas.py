from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional

# Enum for Priority
class Priority(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"

# Create Task Model
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    due_at: Optional[datetime] = None  # Due date (optional)
    priority: Priority = Priority.medium  # Default priority value

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    priority: Priority | None = None
    due_at: datetime | None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    due_at: Optional[datetime]
    priority: Priority
    user_id: int  # Ensure this is defined as an integer
    
    class Config:
        orm_mode = True
  # This will make sure Pydantic models work seamlessly with SQLAlchemy models

# User Model
class UserBase(BaseModel):
    username: str
    phone_number: str

class UserCreate(UserBase):
    pass  # You would need to handle password hashing here

class UserResponse(UserBase):
    id: int
    
    class Config:
        orm_mode = True
