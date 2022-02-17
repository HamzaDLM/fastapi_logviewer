from fastapi import APIRouter
from fastapi.responses import JSONResponse

from worker import celery
from worker import test_task


router = APIRouter()


@router.post("/", response_description="Alerts Report")
async def get_excess_speed():

    task = test_task.delay(5, 1 ,2)

    return JSONResponse(content={"task_id": task.id}, status_code=201)


@router.get("/status/{task_id}")
async def get_status(task_id):

    task_result = celery.AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status
    }

    return JSONResponse(content=result, status_code=200)


@router.get("/result/{task_id}")
async def get_result(task_id):

    task_result = celery.AsyncResult(task_id)

    return JSONResponse(content={"result": task_result.result}, status_code=200)
