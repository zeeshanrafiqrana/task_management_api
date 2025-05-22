import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.task import TaskUpdate
from app.services.task import task_service
from app.utils.notifications import send_notification

logger = logging.getLogger(__name__)


async def process_task(task_id: int, db: AsyncSession):
    """
    Process a task in the background
    
    This simulates a long-running task with status updates and notifications
    """
    logger.info(f"Starting to process task {task_id}")
    
    try:
        # Get the task
        task = await task_service.get(db, task_id)
        if not task:
            logger.error(f"Task {task_id} not found")
            return
        
        # Simulate processing steps
        logger.info(f"Processing task {task_id}: Step 1")
        await asyncio.sleep(2)  # Simulate work
        
        logger.info(f"Processing task {task_id}: Step 2")
        await asyncio.sleep(3)  # Simulate more work
        
        # Update task to completed
        task_update = TaskUpdate(status="completed")
        updated_task = await task_service.update(db, db_obj=task, obj_in=task_update)
        
        # Send notification
        await send_notification(
            f"Task {task_id} ({task.title}) has been completed successfully."
        )
        
        logger.info(f"Task {task_id} processed successfully")
        return updated_task
        
    except Exception as e:
        logger.error(f"Error processing task {task_id}: {str(e)}")
        
        # Update task to failed
        try:
            task = await task_service.get(db, task_id)
            if task:
                task_update = TaskUpdate(status="failed")
                await task_service.update(db, db_obj=task, obj_in=task_update)
                
                # Send notification about failure
                await send_notification(
                    f"Task {task_id} ({task.title}) processing failed: {str(e)}"
                )
        except Exception as inner_e:
            logger.error(f"Error updating failed task {task_id}: {str(inner_e)}")
