from fastapi import FastAPI
from dotenv import load_dotenv
from routers import users

load_dotenv()

app = FastAPI()
app.include_router(users.router)


@app.get("/health")
def health():
    return {"status": "ok"}
