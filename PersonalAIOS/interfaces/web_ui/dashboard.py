from fastapi import FastAPI

app = FastAPI(title="PersonalAIOS Web Dashboard")

@app.get("/")
def read_root():
    return {"message": "Welcome to the unconstrained Personal AI OS."}

# Placeholder for websocket endpoints to handle real-time streaming
