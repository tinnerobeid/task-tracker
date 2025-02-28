from fastapi import FastAPI
from api.routes.routes import task_router
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()
app.include_router(task_router)

register_tortoise(
    app = app,
    db_url = "sqlite://task.db",
    add_exception_handlers = True,
    generate_schemas= True,
    modules = {"models": ["api.models.models"]},
    
)

@app.get("/")
def index():
    return {"status": "Task tracker"}