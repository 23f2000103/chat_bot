from fastapi import FastAPI
from routes.ask import router

app = FastAPI()

app.include_router(router)

@app.get("/")

def home():
    return {
        "status": "running"
        }