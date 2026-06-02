from fastapi import FastAPI
from dotenv import load_dotenv
from routers import users, dummy, job_applications

load_dotenv()

app = FastAPI()
app.include_router(users.router)
app.include_router(job_applications.router)
app.include_router(dummy.private_router)


@app.get("/health")
def health():
    return {"status": "ok"}
