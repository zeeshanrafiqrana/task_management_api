# tests/test_tasks.py

import pytest
from fastapi import status
from app.models.task import Task


@pytest.mark.asyncio
async def test_create_task(test_db, async_client):
    payload = {
        "title": "Test Task",
        "description": "Test Description",
        "priority": 3,
    }
    response = await async_client.post("/api/v1/tasks/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["priority"] == 3
    assert data["status"] == "pending"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_task(test_db, async_client):
    task = Task(title="Get Task Test", description="Test", status="pending", priority=2)
    test_db.add(task)
    await test_db.commit()
    await test_db.refresh(task)

    response = await async_client.get(f"/api/v1/tasks/{task.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Get Task Test"
    assert data["id"] == task.id
    assert "logs" in data


@pytest.mark.asyncio
async def test_list_tasks(test_db, async_client):
    tasks = [
        Task(title="Task 1", description="Test 1", status="pending", priority=1),
        Task(title="Task 2", description="Test 2", status="in_progress", priority=2),
        Task(title="Task 3", description="Test 3", status="completed", priority=3),
    ]
    test_db.add_all(tasks)
    await test_db.commit()

    response = await async_client.get("/api/v1/tasks/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 3

    response = await async_client.get("/api/v1/tasks/?status=in_progress")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(task["status"] == "in_progress" for task in data)

    response = await async_client.get("/api/v1/tasks/?title=Task 1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all("Task 1" in task["title"] for task in data)


@pytest.mark.asyncio
async def test_update_task(test_db, async_client):
    task = Task(title="Update Test", description="Test", status="pending", priority=1)
    test_db.add(task)
    await test_db.commit()
    await test_db.refresh(task)

    response = await async_client.put(
        f"/api/v1/tasks/{task.id}",
        json={"title": "Updated Title", "status": "in_progress"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["status"] == "in_progress"

    # Re-fetch task from DB to verify update
    updated_task = await test_db.get(Task, task.id)
    assert updated_task.title == "Updated Title"
    assert updated_task.status == "in_progress"



@pytest.mark.asyncio
async def test_delete_task(test_db, async_client):
    task = Task(title="Delete Test", description="Test", status="pending", priority=1)
    test_db.add(task)
    await test_db.commit()
    await test_db.refresh(task)

    response = await async_client.delete(f"/api/v1/tasks/{task.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    result = await test_db.get(Task, task.id)
    assert result is None


@pytest.mark.asyncio
async def test_process_task(test_db, async_client):
    task = Task(title="Process Test", description="Test", status="pending", priority=1)
    test_db.add(task)
    await test_db.commit()
    await test_db.refresh(task)

    response = await async_client.post(f"/api/v1/tasks/{task.id}/process")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "in_progress"


@pytest.mark.asyncio
async def test_task_not_found(async_client):
    response = await async_client.get("/api/v1/tasks/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()