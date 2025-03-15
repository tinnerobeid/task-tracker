from fastapi import APIRouter, Depends, HTTPException, status
from api.models.models import Task, User
from api.schemas.schemas import GetTask, PostTask, PutTask
from auth.auth import get_current_user

task_router = APIRouter(prefix="/api", tags=["Tasks"])

@task_router.get("/")
async def all_tasks():
    data = Task.all()
    return await GetTask.from_queryset(data)

@task_router.post("/", response_model=GetTask)
async def post_task(body: PostTask, user: User = Depends(get_current_user)):
    row = await Task.create(**body.dict(exclude_unset=True), user=user)
    return await GetTask.from_tortoise_orm(row)
    

@task_router.put("/{key}")
async def update_task(key: int, body: PutTask):
    data = body.dict(exclude_unset=True)
    exists = await Task.filter(id=key).update(**data)
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {key} not found")
    await Task.filter(id=key).update(**data)
    return await GetTask.from_queryset_single(Task.get(id=key))

@task_router.delete("/{key}")
async def delete_task(key:int):
    exists = await Task.filter(id=key).exists()
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {key} not found")
    await Task.filter(id=key).delete()
    return {"Task deleted"}