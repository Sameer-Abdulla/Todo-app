from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import engine, Base, get_db
from models import Task, User
from schemas import TaskCreate, TaskUpdate, TaskResponse, UserCreate, UserResponse
import crud

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from the frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize the database
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Routes for User
@app.post("/register/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db=db, user=user)

# Routes for Task
@app.post("/tasks/", response_model=TaskResponse)
async def create_task(task: TaskCreate, user_id: int, db: AsyncSession = Depends(get_db)):
    print(f"Received task: {task}")  # Log the incoming data for debugging
    
    # Create a new task object and associate it with the user
    new_task = await crud.create_task(db=db, task=task, user_id=user_id)
    
    return new_task



@app.get("/tasks/user/{user_id}", response_model=list[TaskResponse])
async def get_user_tasks(
    user_id: int,
    due_at: str = None,
    db: AsyncSession = Depends(get_db)
):
    if due_at:
        try:
            due_date = datetime.strptime(due_at, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid date format. Please use YYYY-MM-DD."
            )
    else:
        due_date = None

    tasks = await crud.get_tasks_by_user_and_due_date(
        db=db, user_id=user_id, due_at=due_date
    )
    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found for this user")
    return tasks

@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_data: TaskUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)
    
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await db.delete(task)
    await db.commit()
