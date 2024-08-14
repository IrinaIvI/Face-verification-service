from fastapi import FastAPI
from app.routers import router
from app.consumer import Consumer
import asyncio

consumer = Consumer()

async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения."""
    # Запуск консюмера
    task = asyncio.create_task(consumer.start())
    try:
        # Период работы приложения
        yield
    finally:
        # Остановка консюмера
        await consumer.stop()
        await task

app = FastAPI(title='FaceVerification Service', lifespan=lifespan)

app.include_router(router)



