from fastapi import FastAPI
from app.routers import router
from app.consumer import Consumer
import asyncio

consumer = Consumer()

app = FastAPI(title='FaceVerification Service')
app.include_router(router)

@app.lifespan
async def lifespan(app: FastAPI):
    # Запуск консюмера
    task = asyncio.create_task(consumer.start())

    # При завершении работы приложения
    yield

    # Остановка консюмера
    await consumer.stop()
    await task

