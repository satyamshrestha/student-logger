from fastapi import APIRouter

from routers import (
    auth_router,
    student_router,
    course_router,
    user_router
)

api_router = APIRouter()

api_router.include_router(auth_router.router)
api_router.include_router(student_router.router)
api_router.include_router(course_router.router)
api_router.include_router(user_router.router)