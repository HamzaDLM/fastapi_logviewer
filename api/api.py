from fastapi import APIRouter

from api.endpoints import test_task, logviewer


api_router = APIRouter()

api_router.include_router(test_task.router, prefix="/test", tags=["TestTask"])
api_router.include_router(logviewer.router, prefix="/logs", tags=["LogViewer"])
