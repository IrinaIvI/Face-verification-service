from fastapi import FastAPI
from app.routers import router

app = FastAPI(title='FaceVerification Service')
app.include_router(router)
