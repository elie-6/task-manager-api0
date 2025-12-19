from app.controllers.task import router as task_router

def include_routers(app):
    app.include_router(
        task_router, prefix="/api/v1/tasks", tags=["Tasks"]
    )
