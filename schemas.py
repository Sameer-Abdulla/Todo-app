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
    pass

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    user_id: int  # To indicate which user the task belongs to
    
    class Config:
        orm_mode = True  # This will make sure Pydantic models work seamlessly with SQLAlchemy models

# User Model
# User Base Schema (common fields for user)
class UserBase(BaseModel):
    username: str
    phone_number: str  # Using phone_number instead of email

# User creation schema
class UserCreate(UserBase):
    # No password or email, only name and phone_number for creating a user
    pass

# User response schema
class UserResponse(UserBase):
    id: int
    
    class Config:
        orm_mode = True
