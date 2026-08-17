from fastapi import FastAPI

app = FastAPI()


@app.get("/")  # it is jsut a decorator
def root():
    return {"message": "Task Management System API is running"}
