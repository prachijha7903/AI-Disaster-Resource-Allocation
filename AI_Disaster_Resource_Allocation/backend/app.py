
import requests
import sqlite3
import sys
from pathlib import Path

# Add the project root to Python's module search path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from flask import Flask, jsonify, request
from flask_cors import CORS
from ai_module.resource_allocator import recommend_allocation
from ai_module.priority_engine import calculate_priority


app = Flask(__name__)
CORS(app)

DB_PATH = Path(__file__).resolve().parent.parent / "database" / "disaster.db"


def get_db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def home():
    return jsonify({
        "message": "AI Disaster Resource Allocation API is running",
        "status": "success"
    })


@app.route("/api/dashboard")
def dashboard():
    connection = get_db_connection()

    totals = connection.execute("""
        SELECT
            COUNT(*) AS active_zones,
            COALESCE(SUM(people_affected), 0) AS people_affected,
            COALESCE(SUM(resources_available), 0) AS available_resources
        FROM disaster_zones
    """).fetchone()

    connection.close()
    return jsonify(dict(totals))



@app.route("/api/zones")
def get_zones():
    connection = get_db_connection()

    zones = connection.execute(
        "SELECT * FROM disaster_zones"
    ).fetchall()

    connection.close()

    result = []

    for row in zones:
        zone = dict(row)

        zone["priority"] = calculate_priority(
            zone["severity"],
            zone["people_affected"],
            zone["resources_available"]
        )

        result.append(zone)

    result.sort(key=lambda zone: zone["priority"], reverse=True)

    return jsonify(result)




@app.route("/api/zones", methods=["POST"])
def add_zone():
    data = request.get_json(silent=True) or {}

    required_fields = [
        "name", "location", "severity",
        "people_affected", "resources_available"
    ]

    if any(field not in data for field in required_fields):
        return jsonify({"error": "All fields are required"}), 400

    if data["severity"] not in ["Low", "Medium", "High", "Critical"]:
        return jsonify({"error": "Invalid severity"}), 400

    try:
        people = int(data["people_affected"])
        resources = int(data["resources_available"])
    except (ValueError, TypeError):
        return jsonify({"error": "People and resources must be numbers"}), 400

    if people < 0 or resources < 0:
        return jsonify({"error": "Values cannot be negative"}), 400

    priority = calculate_priority(
        data["severity"], people, resources
    )

    connection = get_db_connection()
    connection.execute("""
        INSERT INTO disaster_zones
        (name, location, severity, people_affected,
         resources_available, priority)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        str(data["name"]).strip(),
        str(data["location"]).strip(),
        data["severity"],
        people,
        resources,
        priority
    ))
    connection.commit()
    connection.close()

    return jsonify({
        "message": "Disaster zone added successfully",
        "priority": priority
    }), 201


@app.route("/api/allocate", methods=["GET"])
def allocate_resources():
    connection = get_db_connection()

    rows = connection.execute(
        "SELECT * FROM disaster_zones"
    ).fetchall()

    connection.close()

    zones = []

    for row in rows:
        zone = dict(row)
        zone["priority"] = calculate_priority(
            zone["severity"],
            zone["people_affected"],
            zone["resources_available"]
        )
        zones.append(zone)

    # Example: recommend distributing 100 relief resource units.
    recommendations = recommend_allocation(zones, 100)

    return jsonify({
        "total_resources_for_allocation": 100,
        "note": "These are planning recommendations, not actual dispatches.",
        "recommendations": recommendations
    })

@app.route("/api/weather", methods=["GET"])
def get_weather():
    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": 30.9010,
                "longitude": 75.8573,
                "current": (
                    "temperature_2m,relative_humidity_2m,"
                    "precipitation,wind_speed_10m"
                ),
                "timezone": "auto"
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        return jsonify({
            "location": "Ludhiana",
            "current_weather": data.get("current", {}),
            "units": data.get("current_units", {}),
            "source": "Open-Meteo"
        })

    except requests.RequestException as error:
        return jsonify({
            "error": "Weather service unavailable",
            "details": str(error)
        }), 502

if __name__ == "__main__":
    app.run(debug=True)

