import json
import os

DATA_FILE = os.getenv("DATA_FILE", "data/lockers.json")


def _ensure_file():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)


def load_all():
    _ensure_file()
    with open(DATA_FILE) as f:
        return json.load(f)


def save_all(data):
    _ensure_file()
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get(locker_id):
    return load_all().get(locker_id)


def put(locker_id, payload):
    data = load_all()
    data[locker_id] = payload
    save_all(data)
    return payload
