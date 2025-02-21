from fastapi import FastAPI
from app.routers import router

app = FastAPI(title='API Gateway')
app.include_router(router)
