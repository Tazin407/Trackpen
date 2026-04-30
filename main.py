from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def root():
    return {"Success": "Project running successfully"}
