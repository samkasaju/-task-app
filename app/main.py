from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Task
from .schemas import TaskCreate, TaskResponse, TaskUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management API",
    description="DevOps Task App",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Task API is running"}


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
):
    new_task = Task(
        title=task.title,
        description=task.description,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
):
    return db.query(Task).all()


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
):
    existing_task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not existing_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    update_data = task.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(existing_task, key, value)

    db.commit()
    db.refresh(existing_task)

    return existing_task


@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    existing_task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not existing_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    db.delete(existing_task)
    db.commit()

    return {"message": "Task deleted successfully"}

