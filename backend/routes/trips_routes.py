from typing import Optional
from fastapi import APIRouter, Body
from pydantic import BaseModel

from fastapi import HTTPException

from backend.services.trip_service import (
    list_trips,
    create_trip,
    get_trip,
    save_plan,
    rename_trip,
    delete_trip
)

router = APIRouter(prefix="/trips")


class PlanRequest(BaseModel):
    trip_id: str
    plan: Optional[dict] = None


class RenameRequest(BaseModel):
    title: str


@router.get("/")
def get_trips():
    return list_trips()


@router.post("/")
def new_trip():
    return create_trip()


@router.get("/{trip_id}")
def load_trip(trip_id: str):
    return get_trip(trip_id)


@router.put("/{trip_id}/plan")
def save_trip_plan(trip_id: str, request: PlanRequest):
    if not request.plan:
        raise HTTPException(status_code=400, detail="Plan missing")

    return save_plan(trip_id, request.plan)


@router.put("/{trip_id}/rename")
def rename_trip_api(trip_id: str, request: RenameRequest):
    return rename_trip(trip_id, request.title)


@router.delete("/{trip_id}")
def delete_trip_api(trip_id: str):
    return {"deleted": delete_trip(trip_id)}

