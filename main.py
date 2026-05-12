from fastapi import FastAPI
import models
from database import engine
from routes import router

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fish Freshness AI Backend")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Fish Freshness Scanner API is online. Visit /docs for Swagger UI."}