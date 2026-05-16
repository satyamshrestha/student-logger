import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from utils.exceptions import AppException
from api.v1.api import api_router
from utils.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")

    yield
    
    logger.info("Application shutting down...")

app = FastAPI(lifespan=lifespan)
app.include_router(api_router, prefix="/api/v1")

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

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Global exception handler for AppException
@app.exception_handler(AppException)
def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )