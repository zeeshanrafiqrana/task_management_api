from typing import List, Optional, Dict, Any
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.task import Task, TaskLog
from app.schemas.task import TaskCreate, TaskUpdate, TaskLogCreate


class TaskService:
    async def create(self, db: AsyncSession, obj_in: TaskCreate) -> Task:
        """Create a new task"""
        db_obj = Task(
            title=obj_in.title,
            description=obj_in.description,
            status="pending",
            priority=obj_in.priority,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, id: int) -> Optional[Task]:
        """Get a task by ID"""
        query = select(Task).where(Task.id == id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_with_logs(self, db: AsyncSession, id: int) -> Optional[Task]:
        """Get a task with its logs by ID"""
        query = select(Task).options(selectinload(Task.logs)).where(Task.id == id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_multi(
        self, 
        db: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Task]:
        """Get multiple tasks with optional filtering"""
        query = select(Task)
        
        if filters:
            if title := filters.get("title"):
                query = query.filter(Task.title.ilike(f"%{title}%"))
            if status := filters.get("status"):
                query = query.filter(Task.status == status)
            if priority := filters.get("priority"):
                query = query.filter(Task.priority == priority)
        
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def update(
        self, db: AsyncSession, *, db_obj: Task, obj_in: TaskUpdate
    ) -> Task:
        """Update a task"""
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # If status is being updated, create a log entry
        if "status" in update_data and update_data["status"] != db_obj.status:
            log = TaskLog(task_id=db_obj.id, status=update_data["status"])
            db.add(log)
        
        # Update the task
        stmt = (
            update(Task)
            .where(Task.id == db_obj.id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(stmt)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, id: int) -> None:
        """Delete a task"""
        stmt = delete(Task).where(Task.id == id)
        await db.execute(stmt)
        await db.commit()

    async def create_log(self, db: AsyncSession, obj_in: TaskLogCreate) -> TaskLog:
        """Create a new task log"""
        db_obj = TaskLog(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


task_service = TaskService()
