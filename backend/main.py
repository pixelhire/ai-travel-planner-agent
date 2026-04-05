import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.router import router as request_router
from backend.routes.trips_routes import router as trips_request_router
from backend.db.postgres_db import init_db
from backend.db.redis import init_redis

import uvicorn
import socket
from contextlib import asynccontextmanager
import subprocess

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting FastAPI app...")

    # DB init
    try:
        await init_db()
        print("✅ PostgreSQL connected")
    except Exception as e:
        print(f"❌ DB connection failed: {e}")
        raise e

    # Redis init
    try:
        await init_redis()
        print("✅ Redis connected")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        raise e

    if not os.environ.get("WORKERS_STARTED"):
        os.environ["WORKERS_STARTED"] = "1"

        print("🚀 Launching workers process...")

        subprocess.Popen(
            [sys.executable, "backend/messaging/run_workers.py"]
        )

    yield

    print("🛑 Shutting down FastAPI app...")


app = FastAPI(lifespan=lifespan)


# ---------- CORS ----------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- REGISTER ROUTES ----------

app.include_router(request_router)
app.include_router(trips_request_router)


# ---------- SERVE FRONTEND ----------

app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static"
)


@app.get("/")
async def serve_frontend():
    return FileResponse("frontend/index.html")


@app.get("/whoami")
def whoami():
    return {"server": socket.gethostname()}

@app.on_event("startup")
async def startup():
    await init_db()


# ---------- RUN SERVER ----------

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )