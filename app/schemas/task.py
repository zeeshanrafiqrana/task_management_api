from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = Field(1, ge=1, le=5, description="Priority from 1 (low) to 5 (high)")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=5)


class TaskInDBBase(TaskBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Task(TaskInDBBase):
    pass


class TaskWithLogs(TaskInDBBase):
    logs: List["TaskLogInDB"] = []


class TaskLogBase(BaseModel):
    status: str


class TaskLogCreate(TaskLogBase):
    task_id: int


class TaskLogInDB(TaskLogBase):
    id: int
    task_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Update forward references
TaskWithLogs.model_rebuild()
