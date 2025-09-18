from fastapi import FastAPI
from .routers import k8s_queries

app = FastAPI(title="K8s NLP Query Service")
app.include_router(k8s_queries.router, prefix="/api/k8s")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
