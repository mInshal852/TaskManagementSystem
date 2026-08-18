from fastapi import FastAPI

from app.routes.auth import router as auth_router

app = FastAPI()

# Include application routers
app.include_router(auth_router)


@app.get("/")  # it is jsut a decorator
def root():
    return {"message": "Task Management System API is running"}
