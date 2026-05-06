from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from db.database import Base, engine
from utils.exceptions import AppException
from routers import auth_router, course_router, student_router, user_router

app = FastAPI()
Base.metadata.create_all(engine)

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(student_router.router)
app.include_router(course_router.router)

@app.get("/")
def home():
    return {"message": "API is running"}

# Global exception handler for AppException
@app.exception_handler(AppException)
def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )