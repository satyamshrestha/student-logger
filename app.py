from fastapi import FastAPI, Request
import time
from fastapi.responses import JSONResponse

from db.database import Base, engine
from utils.exceptions import AppException
from routers import auth_router, course_router, student_router, user_router
from utils.logger import logger

app = FastAPI()
Base.metadata.create_all(engine)

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(student_router.router)
app.include_router(course_router.router)

@app.get("/")
def home():
    return {"message": "API is running"}

# Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    logger.info(f"Incoming request: {request.method} {request.url}")

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        f"Completed request: {request.method} {request.url} | "
        f"Status: {response.status_code} | "
        f"Duration: {duration:.4f}s"
    )

    return response

# Global exception handler for AppException
@app.exception_handler(AppException)
def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )