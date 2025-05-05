from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db import engine
from database import models
from routes import signup
from routes import login

# Create FastAPI app instance
app = FastAPI()

# CORS setup (frontend → backend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(signup.router)
app.include_router(login.router)

# Optional: auto-create tables when running this file directly
def create_tables():
    print("Creating all tables in the database...")
    models.Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

if __name__ == "__main__":
    create_tables()