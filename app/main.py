import logging

from fastapi import FastAPI

from app.routers.upload import router as upload_router
from app.routers.analysis import router as analysis_router


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(message)s"
)


app = FastAPI(
    title="Bioinformatics Backend API",
    description="Backend API untuk aplikasi bioinformatika",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Bioinformatics Backend API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


app.include_router(upload_router)
app.include_router(analysis_router)