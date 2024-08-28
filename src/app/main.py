from fastapi import FastAPI
from app.consumer import Consumer
import asyncio

async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения."""
    consumer = Consumer()
    task = asyncio.create_task(consumer.start())
    try:
        yield
    finally:
        await consumer.stop()
        await task

app = FastAPI(title='FaceVerification Service', lifespan=lifespan)
