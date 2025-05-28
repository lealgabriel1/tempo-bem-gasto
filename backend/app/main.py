from fastapi import FastAPI
from app.database import engine, Base
from app.routers.auth import router as auth_router
from app.routers.ngo import router as ngo_router
from app.routers.volunteer import router as volunteer_router

# Cria todas as tabelas no startup
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)
app.include_router(ngo_router)
app.include_router(volunteer_router)