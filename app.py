from fastapi import FastAPI

app = FastAPI(title="CI/CD Demo Service")

@app.get("/")
def read_root():
    return {"status": "healthy", "service": "active", "environment": "github-actions"}

@app.get("/health")
def health_check():
    return {"status": "UP"}
