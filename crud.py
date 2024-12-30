from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User, Task
from schemas import TaskCreate, UserCreate
from fastapi import HTTPException
from datetime import datetime

# CRUD for User
async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(username=user.username, phone_number=user.phone_number)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# CRUD for Task


async def create_task(db: AsyncSession, task: TaskCreate, user_id: int):
    if not user_id:
        raise ValueError("user_id is required to create a task")
    
    # Use naive current time for created_at
    created_at = datetime.now()

    # Ensure due_at is naive
    due_at = task.due_at.replace(tzinfo=None) if task.due_at and task.due_at.tzinfo else task.due_at

    # Create the new task
    db_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=created_at,
        due_at=due_at,
        priority=task.priority,
        user_id=user_id  # Ensure this is correctly passed
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def get_tasks_by_user_and_due_date(
    db: AsyncSession, user_id: int, due_at: datetime = None
):
    query = select(Task).filter(Task.user_id == user_id)
    if due_at:
        query = query.filter(Task.due_at == due_at)
    result = await db.execute(query)
    return result.scalars().all()