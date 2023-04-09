#backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.profile.routes import router as profile_router
from app.auth.routes import router as auth_router
from app.training_plan.routes import router as training_plan_router
from app.database import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(auth_router, prefix='/api/auth', tags=['auth'])
app.include_router(profile_router, prefix="/api", tags=["profile"])
app.include_router(training_plan_router, prefix='/api/training_plan', tags=['training_plan'])

# Configuración de CORS
origins = [
    "http://localhost",  # Asegúrate de cambiar esto para que coincida con el dominio de tu frontend
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ...
