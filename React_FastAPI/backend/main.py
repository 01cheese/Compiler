import logging
import asyncio
from fastapi import FastAPI, WebSocket, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from celery.result import AsyncResult
from celery_worker import execute_task

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

# Разрешаем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/execute")
async def execute_code(request: dict, background_tasks: BackgroundTasks):
    """Принимает код, отправляет в Celery"""
    logging.info(f"Получен запрос: {request}")

    print(request)

    task = execute_task.delay(request)
    return {"task_id": task.id}


@app.get("/result/{task_id}")
async def get_result(task_id: str):
    """Получает результат выполнения задачи"""
    task_result = AsyncResult(task_id)
    if task_result.ready():
        return task_result.get()
    return {"status": "processing"}


@app.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    """WebSocket для получения результата в реальном времени"""
    await websocket.accept()
    while True:
        task_result = AsyncResult(task_id)
        if task_result.ready():
            await websocket.send_json(task_result.get())
            break
        await asyncio.sleep(1)
    await websocket.close()
