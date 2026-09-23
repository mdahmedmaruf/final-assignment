from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import admin, authentication, parcels

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "https://final-frontend-pearl.vercel.app",
    "http://localhost:5173",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentication.router)
app.include_router(admin.router)
app.include_router(parcels.router)


@app.get("/")
def home():
    return {"message": "Courier Service API"}
