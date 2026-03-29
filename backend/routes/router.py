from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.trip_execution_service import start_trip_execution, fetch_execution_result, check_execution_status


router = APIRouter()

class TripRequest(BaseModel):
    query: str
    trip_id: str | None = None   # ✅ ADD THIS
    budget: str | None = "medium"
    # days: int | None = 1




@router.post("/plan-trip")
def plan_trip_api(request: TripRequest):

    result = start_trip_execution(
        query=request.query,
        budget=request.budget,
        # days=request.days,
        trip_id=request.trip_id   # ✅ ADD THIS
    )

    print("Trip plan from router: ",result)

    return {
        "trip_id": result["trip_id"],
        "status": "Tasks dispatched",
        "destination": result["destination"],
        "tasks": result["tasks"]
    }


@router.get("/get-trip/{trip_id}")
def get_trip_api(trip_id: str):

    trip_data = fetch_execution_result(trip_id)

    if not trip_data:
        return {"status": "No data yet"}

    status = check_execution_status(trip_data)

    # ✅ get latest saved plan (if exists)
    plans = trip_data.get("plans", [])
    final = plans[-1]["plan"] if plans else None

    return {
        "trip_id": trip_id,
        "status": "complete" if status["is_complete"] else "processing",
        "progress": status["progress"],
        "data": trip_data,
        "final": final
    }

