from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import main_router

app = FastAPI(
    title="WaterTime API",
    description="API para gestão de hidratação",
)

origins = ["http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    main_router
)