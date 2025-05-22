from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.models.task import Task
from app.services.task import task_service


async def get_task_by_id(
    task_id: int, db: AsyncSession = Depends(get_db)
) -> Task:
    """Get a task by ID or raise 404"""
    task = await task_service.get(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return task
