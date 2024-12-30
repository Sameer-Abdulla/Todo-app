from pydantic import BaseModel
from datetime import datetime, date
from enum import Enum

# Enum for Priority
class Priority(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"

# Base task model
class TaskBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False
    due_at: datetime | None = None  # Optional due datetime (full timestamp)
    priority: Priority = Priority.medium  # Default priority is medium

# Model for creating a task
class TaskCreate(TaskBase):
    pass

# Model for updating a task (you can add validation rules here if needed)
class TaskUpdate(TaskBase):
    pass

# Model for the task response (after creation or retrieval)
class TaskResponse(TaskCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True  # Ensure compatibility with SQLAlchemy ORM

