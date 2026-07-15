from fastapi import FastAPI

app = FastAPI(
    title="Manufacturing Production Planning System",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Manufacturing Planning System API is running."
    }