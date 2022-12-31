from fastapi import FastAPI, Depends, Response, status, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from src.models.data import tracker
from src.database.connector import db_engine
from src.controllers import user_management, message_management

tracker.Base.metadata.create_all(bind=db_engine)

app = FastAPI()
app = FastAPI(
    tags=["Messaging system"],
    title="API Documentation",
    description="A simple messaging system",
    version="1.0.0",
    servers= [
        {
            "url": "http://localhost:8000",
            "description": "Development Server"
        }]
    )


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", mode="r") as reqfile:
        return HTMLResponse(content=reqfile.read(), status_code=200)

@app.get("/index")
async def index():
    return JSONResponse(content={"message": "Message Tracker API"}, status_code=status.HTTP_200_OK)

app.include_router(user_management.router)
app.include_router(message_management.router)