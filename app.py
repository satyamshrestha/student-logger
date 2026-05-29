import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

from utils.rate_limiter import limiter
from utils.exceptions import AppException
from api.v1.api import api_router
from utils.logger import logger
from middleware.request_context import RequestContextMiddleware
from middleware.logging_middleware import LoggingMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")

    yield
    
    logger.info("Application shutting down...")

app = FastAPI(lifespan=lifespan)
app.include_router(api_router, prefix="/api/v1")

app.state.limiter = limiter

app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestContextMiddleware)
app.add_middleware(SlowAPIMiddleware)
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

@app.get("/")
def home():
    return {"message": "API is running"}

# Global exception handler for AppException
@app.exception_handler(AppException)
def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "type": exc.error_type,
                "message": exc.message
            }
        }
    )