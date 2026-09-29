from fastapi import FastAPI

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