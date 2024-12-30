from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User, Task
from schemas import TaskCreate, UserCreate
from fastapi import HTTPException

# CRUD for User
async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(username=user.username, phone_number=user.phone_number)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# CRUD for Task
async def create_task(db: AsyncSession, task: TaskCreate, user_id: int):
    db_task = Task(**task.dict(), user_id=user_id)  # Assign user_id to task
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def get_tasks_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(Task).filter(Task.user_id == user_id))
    tasks = result.scalars().all()
    return tasks
