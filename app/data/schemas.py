from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Task(BaseModel):
    task_id: Optional[int]  
    title: str
    description: Optional[str] = ""
    status: Optional[str] = "todo"  
    due_date: Optional[datetime] = None

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]
    due_date: Optional[datetime]
