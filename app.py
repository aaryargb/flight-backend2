from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import date, timedelta

app = Flask(__name__)
CORS(app)

# Get your free key at https://www.searchapi.io — no credit card, instant signup
SERPAPI_KEY = "6Sm9HCd6s5bZhSZFgRnaHtvG"
BASE_URL = "https://www.searchapi.io/api/v1/search"


def search_flights(dep, arr, travel_date):
    res = requests.get(BASE_URL, params={
        "engine": "google_flights",
        "departure_id": dep,
        "arrival_id": arr,
        "outbound_date": travel_date,
        "flight_type": "one_way",
        "currency": "INR",
        "hl": "en",
        "api_key": SERPAPI_KEY
    })
    data = res.json()
    all_offers = data.get("best_flights", []) + data.get("other_flights", [])

    results = []
    for offer in all_offers:
        seg = offer["flights"][0]
        results.append({
            "airline": seg.get("airline", "Unknown"),
            "airline_logo": seg.get("airline_logo", ""),
            "flight_number": seg.get("flight_number", ""),
            "departure_airport": seg["departure_airport"]["name"],
            "departure_code": seg["departure_airport"]["id"],
            "arrival_airport": seg["arrival_airport"]["name"],
            "arrival_code": seg["arrival_airport"]["id"],
            "departure_time": seg["departure_airport"]["time"],
            "arrival_time": seg["arrival_airport"]["time"],
            "duration_mins": offer.get("total_duration", 0),
            "stops": len(offer["flights"]) - 1,
            "price": offer.get("price", 0),
            "currency": "INR",
            "booking_link": f"https://www.google.com/travel/flights?q=flights+{dep}+to+{arr}+on+{travel_date}"
        })
    return results


def sort_by_departure(flights):
    return sorted(flights, key=lambda x: x["departure_time"])


def validate_airport(code):
    return bool(code) and len(code) == 3


@app.route("/")
def home():
    return "✈ Flight Comparison Backend Running"


# ONE WAY SEARCH
@app.route("/flights")
def flights():
    dep = request.args.get("dep", "").upper()
    arr = request.args.get("arr", "").upper()
    travel_date = request.args.get("date", str(date.today() + timedelta(days=7)))

    if not validate_airport(dep) or not validate_airport(arr):
        return jsonify({
            "error": "Invalid airport code"
        }), 400

    try:
        results = search_flights(dep, arr, travel_date)

        if not results:
            return jsonify({
                "message": "No flights found"
            }), 404

        results = sort_by_departure(results)

        return jsonify(results)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ROUND TRIP SEARCH
@app.route("/roundtrip")
def roundtrip():
    dep = request.args.get("dep", "").upper()
    arr = request.args.get("arr", "").upper()
    outbound_date = request.args.get("date", str(date.today() + timedelta(days=7)))
    return_date = request.args.get("return_date", str(date.today() + timedelta(days=14)))

    if not validate_airport(dep) or not validate_airport(arr):
        return jsonify({
            "error": "Invalid airport code"
        }), 400

    try:
        onward = search_flights(dep, arr, outbound_date)
        return_back = search_flights(arr, dep, return_date)

        return jsonify({
            "onward": onward,
            "return": return_back
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
