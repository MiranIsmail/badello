from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import asyncpg
import os

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "taskdb")

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost",
    "http://127.0.0.1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Task(BaseModel):
    title: str
    description: str
    completed: bool = False
    id: int | None = None

async def get_db():
    conn = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
    )
    return conn

@app.on_event("startup")
async def startup():
    conn = await get_db()
    await conn.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        completed BOOLEAN DEFAULT FALSE
    )
    ''')
    await conn.close()

@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    conn = await get_db()
    result = await conn.fetchrow('''
        INSERT INTO tasks (title, description, completed)
        VALUES ($1, $2, $3) RETURNING id, title, description, completed
    ''', task.title, task.description, task.completed)
    await conn.close()
    return Task(id=result['id'], title=result['title'], description=result['description'], completed=result['completed'])

@app.get("/tasks/", response_model=List[Task])
async def get_tasks():
    conn = await get_db()
    tasks = await conn.fetch('SELECT id, title, description, completed FROM tasks')
    await conn.close()
    return [Task(id=task['id'], title=task['title'], description=task['description'], completed=task['completed']) for task in tasks]

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    conn = await get_db()
    result = await conn.fetchrow('''
        UPDATE tasks SET title=$1, description=$2, completed=$3
        WHERE id=$4 RETURNING id, title, description, completed
    ''', task.title, task.description, task.completed, task_id)
    await conn.close()
    return Task(id=result['id'], title=result['title'], description=result['description'], completed=result['completed'])

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    conn = await get_db()
    await conn.execute('DELETE FROM tasks WHERE id=$1', task_id)
    await conn.close()
    return {"message": f"Task {task_id} deleted successfully"}


