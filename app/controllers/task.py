from fastapi import APIRouter, status, HTTPException
from app.data import schemas
from app.data.database import task_collection, get_next_task_id

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

VALID_STATUSES = {"todo", "in-progress", "done"}



@router.get("/", status_code=status.HTTP_200_OK, summary="Get all tasks")
async def get_all_tasks(limit: int = 100):
    tasks_cursor = task_collection.find().limit(limit)
    tasks = []
    async for task in tasks_cursor:
        tasks.append({
            "task_id": task['task_id'],
            "title": task['title'],
            "description": task.get('description', ''),
            "status": task.get('status', 'todo'),
            "due_date": task.get('due_date', None)
        })
    return {"detail": "success", "tasks": tasks}


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create a new task")
async def create_task(task: schemas.Task):
    if task.status and task.status not in VALID_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status '{task.status}'. Must be one of {VALID_STATUSES}"
        )

    if task.task_id is None:
        task.task_id = await get_next_task_id()

    existing = await task_collection.find_one({"task_id": task.task_id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Task with id {task.task_id} already exists"
        )

    result = await task_collection.insert_one(task.dict())
    if result.acknowledged:
        return {"detail": "Task successfully created", "task": task.dict()}


@router.get("/{task_id}", status_code=status.HTTP_200_OK, response_model=schemas.Task, summary="Get a task by ID")
async def get_task(task_id: int):
    task = await task_collection.find_one({"task_id": task_id}, {"_id": 0})
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return {"detail": "success", "task": task}


@router.put("/{task_id}", status_code=status.HTTP_200_OK, summary="Update a task")
async def update_task(task_id: int, task_update: schemas.TaskUpdate):
    task = await task_collection.find_one({"task_id": task_id})
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    update_data = {k: v for k, v in task_update.dict().items() if v is not None}

    if "status" in update_data and update_data["status"] not in VALID_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status '{update_data['status']}'. Must be one of {VALID_STATUSES}"
        )

    if update_data:
        await task_collection.update_one({"task_id": task_id}, {"$set": update_data})
    return {"detail": "Task successfully updated", "updated_fields": update_data}


@router.delete("/{task_id}", status_code=status.HTTP_200_OK, summary="Delete a task")
async def delete_task(task_id: int):
    task = await task_collection.find_one({"task_id": task_id})
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    await task_collection.delete_one({"task_id": task_id})
    return {"detail": "Task successfully deleted", "task_id": task_id}
