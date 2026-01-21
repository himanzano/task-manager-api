from fastapi import FastAPI

from app.api.routes import auth, tasks

app = FastAPI(title="Task Manager API")

app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Hello from task-manager-api!"}
