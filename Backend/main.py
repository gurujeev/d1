from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import Base, engine

from auth.routes import router as auth_router

from routes.student import router as student_router
from routes.mentor import router as mentor_router
from routes.coordinator import router as coordinator_router
from routes.weekly_report import router as weekly_report_router


# Create directories
Path("data").mkdir(exist_ok=True)


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="College RBAC Attendance Demo",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API routes
app.include_router(auth_router)

app.include_router(student_router)
app.include_router(mentor_router)
app.include_router(coordinator_router)
app.include_router(weekly_report_router)


@app.get("/api/health")
def health_check():

    return {
        "status": "ok",
        "application": "College RBAC Demo"
    }


# Frontend
app.mount(
    "/",
    StaticFiles(
        directory="../frontend",
        html=True
    ),
    name="frontend"
)