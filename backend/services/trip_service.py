import json
import os
import uuid

from backend.utils.config import TRIPS_DIR


def trip_file(trip_id):
    return os.path.join(TRIPS_DIR, f"{trip_id}.json")


def list_trips():

    trips = []

    for file in os.listdir(TRIPS_DIR):

        if file.endswith(".json"):

            with open(os.path.join(TRIPS_DIR, file)) as f:

                data = json.load(f)

                trips.append({
    "id": data["id"],
    "title": data["title"],
    "plans": data.get("plans", [])
})
                

                # print("Trips data:\n",trips)

    return trips


def create_trip():

    trip_id = str(uuid.uuid4())

    data = {
        "id": trip_id,
        "title": "New Trip",
        "plans": [],
        "chat": []
    }

    with open(trip_file(trip_id), "w") as f:
        json.dump(data, f, indent=2)

    return data


def get_trip(trip_id):

    # print(f"[get_trip] Requested trip_id: {trip_id}")

    file = trip_file(trip_id)

    # print(f"[get_trip] File path: {file}")

    if not os.path.exists(file):
        print(f"[get_trip] File NOT found for trip_id: {trip_id}")
        return None

    try:
        with open(file) as f:
            data = json.load(f)

        # print(f"[get_trip] Trip loaded successfully:")
        # print(data)

        return data

    except Exception as e:
        print(f"[get_trip] Error loading trip: {e}")
        return None


def save_plan(trip_id, plan):

    trip = get_trip(trip_id)

    if not trip:
        return None

    if "plans" not in trip:
        trip["plans"] = []

    plan_entry = {
        "id": str(uuid.uuid4()),
        "plan": plan
    }

    trip["plans"].append(plan_entry)

    trip["title"] = plan.get("destination", trip["title"])

    with open(trip_file(trip_id), "w") as f:
        json.dump(trip, f, indent=2)

    return plan_entry


def rename_trip(trip_id, title):

    trip = get_trip(trip_id)

    if not trip:
        return None

    trip["title"] = title

    with open(trip_file(trip_id), "w") as f:
        json.dump(trip, f, indent=2)

    return trip


def delete_trip(trip_id):

    file = trip_file(trip_id)

    if os.path.exists(file):
        os.remove(file)

        return True

    return False