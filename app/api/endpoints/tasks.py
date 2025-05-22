from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_task_by_id
from app.db.base import get_db
from app.models.task import Task
from app.schemas.task import Task as TaskSchema, TaskCreate, TaskUpdate, TaskWithLogs
from app.services.task import task_service
from app.tasks.worker import process_task

router = APIRouter()


@router.post("/", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new task"""
    return await task_service.create(db, task_in)


@router.get("/", response_model=List[TaskSchema])
async def list_tasks(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    title: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[int] = None,
):
    """List all tasks with optional filtering and pagination"""
    filters = {}
    if title:
        filters["title"] = title
    if status:
        filters["status"] = status
    if priority:
        filters["priority"] = priority
    
    return await task_service.get_multi(db, skip=skip, limit=limit, filters=filters)


@router.get("/{task_id}", response_model=TaskWithLogs)
async def get_task(
    task: Task = Depends(get_task_by_id),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific task by ID with its logs"""
    return await task_service.get_with_logs(db, task.id)


@router.put("/{task_id}", response_model=TaskSchema)
async def update_task(
    task_update: TaskUpdate,
    task: Task = Depends(get_task_by_id),
    db: AsyncSession = Depends(get_db),
):
    """Update a task"""
    return await task_service.update(db, db_obj=task, obj_in=task_update)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task: Task = Depends(get_task_by_id),
    db: AsyncSession = Depends(get_db),
):
    """Delete a task"""
    await task_service.delete(db, id=task.id)
    return None


@router.post("/{task_id}/process", response_model=TaskSchema)
async def start_processing(
    background_tasks: BackgroundTasks,
    task: Task = Depends(get_task_by_id),
    db: AsyncSession = Depends(get_db),
):
    """Start background processing for a task"""
    # Update task status to in_progress
    task_update = TaskUpdate(status="in_progress")
    updated_task = await task_service.update(db, db_obj=task, obj_in=task_update)
    
    # Add the background task
    background_tasks.add_task(process_task, task.id, db)
    
    return updated_task
