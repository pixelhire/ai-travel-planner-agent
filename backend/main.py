import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.router import router as request_router
from backend.routes.trips_routes import router as trips_request_router

import uvicorn
import socket


app = FastAPI()


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


# ---------- RUN SERVER ----------

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )