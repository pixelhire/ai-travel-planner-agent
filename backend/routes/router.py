from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.planner_service import plan_trip


router = APIRouter()

class TripRequest(BaseModel):
    query : str


@router.post("/plan-trip")
def plan_trip_api(request: TripRequest):
    # print("Inside backend api")
    result = plan_trip(request.query)
    # print("Planned Trip : \n", result)
    return {"result": result}



