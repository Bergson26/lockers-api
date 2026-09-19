import os

from flask import Flask, jsonify, request

from app import service

app = Flask(__name__)

API_TOKEN = os.getenv("API_TOKEN", "dev-token")


def _authorized():
    return request.headers.get("X-Api-Token") == API_TOKEN


@app.get("/lockers")
def list_lockers():
    return jsonify(service.list_lockers())


@app.get("/lockers/<locker_id>")
def get_locker(locker_id):
    locker = service.get_locker(locker_id)
    if locker is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(locker)


@app.post("/lockers/<locker_id>/status")
def set_status(locker_id):
    if not _authorized():
        return jsonify({"error": "unauthorized"}), 401
    body = request.get_json()
    try:
        return jsonify(service.set_status(locker_id, body["status"]))
    except service.UnknownStatus:
        return jsonify({"error": "unknown status"}), 400


@app.get("/stats")
def stats():
    return jsonify({"occupancy_rate": service.occupancy_rate()})


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug, host="0.0.0.0", port=int(os.getenv("PORT", "5000")))  # nosec B104
