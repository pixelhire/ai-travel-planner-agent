from backend.services.trip_service import save_plan, trip_file, get_trip as get_trip_from_file
from backend.services.planner_service import generate_final_plan

import json
import uuid


def save_result(trip_id, key, data):
    print("Saving:", trip_id, key)

    file_path = trip_file(trip_id)

    trip = get_trip(trip_id)
    if not trip:
        print("Trip not found:", trip_id)
        return

    # =========================================================
    # ✅ ENSURE STRUCTURE
    # =========================================================
    trip.setdefault("results", {})
    trip.setdefault("status", {})
    trip["status"].setdefault("completed_tasks", [])
    trip["status"].setdefault("expected_tasks", [])

    # BACKWARD COMPAT
    trip.setdefault("completed_tasks", [])
    trip.setdefault("expected_tasks", [])

    # =========================================================
    # 🔥 PREVENT DUPLICATE WORKER WRITES
    # =========================================================
    if key in trip["results"]:
        print(f"⚠️ {key} already exists, skipping duplicate write")
        return

    # =========================================================
    # ✅ SAVE RESULT
    # =========================================================
    trip["results"][key] = data

    if key not in trip["status"]["completed_tasks"]:
        trip["status"]["completed_tasks"].append(key)

    if key not in trip["completed_tasks"]:
        trip["completed_tasks"].append(key)

    # SAVE IMMEDIATELY (important for streaming UI)
    with open(file_path, "w") as f:
        json.dump(trip, f, indent=2)

    # =========================================================
    # 🔥 SAFE COMPLETION CHECK (IMPORTANT FIX)
    # =========================================================
    expected = set(trip["status"].get("expected_tasks", []))
    completed = set(trip["status"].get("completed_tasks", []))

    if not expected or not expected.issubset(completed):
        return  # ❌ DO NOT CONTINUE if not fully complete

    print("All tasks complete:", trip_id)

    # =========================================================
    # 🔥 PREVENT MULTIPLE FINAL PLAN GENERATION (RACE FIX)
    # =========================================================
    if trip.get("final_plan") and trip["final_plan"].get("output"):
        print("⚠️ Final plan already exists, skipping")
        return

    # =========================================================
    # ✅ GENERATE FINAL PLAN
    # =========================================================
    final_plan = generate_final_plan(
    trip["results"],
    trip.get("destination"),
    trip.get("days"),
    trip["results"].get("transport"),
    trip["results"].get("weather")
)

    # =========================================================
    # 🔥 STORE FINAL PLAN
    # =========================================================
    trip["final_plan"] = {
        "input": trip.get("last_query"),
        "output": final_plan
    }

    # =========================================================
    # 🔥 HISTORY (STRONG DUP CHECK)
    # =========================================================
    history = trip.setdefault("history", [])

    if not any(h.get("output") == final_plan for h in history):
        history.append({
            "id": str(uuid.uuid4()),
            "input": trip.get("last_query"),
            "output": final_plan
        })

    # =========================================================
    # ✅ BACKWARD COMPAT (UI)
    # =========================================================
    save_plan(trip_id, {
        "input": trip.get("last_query"),
        "output": final_plan
    })

    # =========================================================
    # ✅ FINAL SAVE (CRITICAL FOR UI UPDATE)
    # =========================================================
    with open(file_path, "w") as f:
        json.dump(trip, f, indent=2)



def get_trip(trip_id):
    return get_trip_from_file(trip_id)


def is_trip_complete(trip_id):
    trip = get_trip_from_file(trip_id)

    if not trip:
        return False

    expected = set(trip.get("expected_tasks", []))
    completed = set(trip.keys())

    return expected.issubset(completed)


def is_trip_complete_data(trip):
    # ✅ prefer new structure
    status = trip.get("status", {})

    expected = set(status.get("expected_tasks", trip.get("expected_tasks", [])))
    completed = set(status.get("completed_tasks", trip.get("completed_tasks", [])))

    return expected.issubset(completed)

