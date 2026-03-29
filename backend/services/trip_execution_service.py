import re
import uuid
import json

from backend.services.planner_service import plan_trip
from backend.messaging.producer import send_task
from backend.memory.trip_store import get_trip, trip_file
import os


# 🔥 Create trip execution (NOT DB trip)
def start_trip_execution(query: str, budget: str, days: int = None, trip_id: str = None):

    plan = plan_trip(query)
    print("Plan for days : ",plan)

    destination = plan.get("destination") or query
    tasks = plan.get("tasks", [])

    # ✅ reuse trip if exists
    if trip_id and os.path.exists(trip_file(trip_id)):
        trip = get_trip(trip_id)

        if not trip:
            # fallback safety (file exists but failed to load)
            trip = {}

        # ✅ ensure history exists
        trip.setdefault("history", [])

        # 🔥 PRESERVE previous final plan BEFORE reset (NO DUPLICATES)
        last = trip.get("final_plan", {})
        if last and last.get("output"):
            if not any(
                h.get("output") == last.get("output")
                for h in trip["history"]
            ):
                trip["history"].append({
                    "id": str(uuid.uuid4()),
                    "input": last.get("input"),
                    "output": last.get("output")
                })

        # =========================================================
        # ✅ UPDATE CURRENT EXECUTION CONTEXT
        # =========================================================
        trip["destination"] = destination
        trip["days"] = plan.get("days", days)
        trip["last_query"] = query

        # ✅ NEW STRUCTURE
        trip["status"] = {
            "expected_tasks": tasks,
            "completed_tasks": []
        }

        # ✅ BACKWARD COMPAT (DO NOT REMOVE)
        trip["expected_tasks"] = tasks
        trip["completed_tasks"] = []

        # =========================================================
        # 🔥 RESET ONLY EXECUTION STATE (CRITICAL)
        # =========================================================
        trip["results"] = {}

        # 🔥 IMPORTANT: clear old result to prevent UI showing stale data
        trip["final_plan"] = {}

        # =========================================================
        # SAVE
        # =========================================================
        with open(trip_file(trip_id), "w") as f:
            json.dump(trip, f, indent=2)

    else:
        # =========================================================
        # ✅ CREATE NEW TRIP
        # =========================================================
        trip_id = str(uuid.uuid4())

        trip = {
            "id": trip_id,
            "title": f"Trip to {destination}",
            "destination": destination,
            "days": days,

            # ✅ NEW STRUCTURE
            "status": {
                "expected_tasks": tasks,
                "completed_tasks": []
            },

            "results": {},
            "final_plan": {},
            "history": [],

            # ✅ BACKWARD COMPAT
            "plans": [],
            "chat": [],
            "expected_tasks": tasks,
            "completed_tasks": [],
            "last_query": query
        }

        with open(trip_file(trip_id), "w") as f:
            json.dump(trip, f, indent=2)

    # =========================================================
    # ✅ SEND TASKS TO KAFKA
    # =========================================================
    for task in tasks:
        send_task(task, {
            "trip_id": trip_id,
            "destination": destination,
            "budget": budget,
            "days": days,
            "query": query
        })

    return {
        "trip_id": trip_id,
        "destination": destination,
        "tasks": tasks
    }




def fetch_execution_result(trip_id: str):
    return get_trip(trip_id)


def check_execution_status(trip_data: dict):
    expected = set(trip_data.get("expected_tasks", []))
    completed = set(trip_data.get("completed_tasks", []))  # ✅ correct

    return {
        "is_complete": expected.issubset(completed),
        "progress": f"{len(completed)}/{len(expected)}"
    }


# def generate_execution_output(trip_data: dict):
#     final = build_final_response(trip_data)
#     return final.content if hasattr(final, "content") else final




# def extract_days(query: str) -> int | None:
#     match = re.search(r"(\d+)\s*day", query.lower())
#     if match:
#         return int(match.group(1))
#     return None