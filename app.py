from flask import Flask, request, jsonify
from services.flight_service import search_flights, sort_by_departure
from utils.validator import validate_airport

app = Flask(__name__)


@app.route("/")
def home():
    return "✈ Flight Comparison Backend Running"


# ONE WAY SEARCH
@app.route("/flights")
def flights():

    dep = request.args.get("dep", "").upper()
    arr = request.args.get("arr", "").upper()

    if not validate_airport(dep) or not validate_airport(arr):
        return jsonify({
            "error": "Invalid airport code"
        }), 400

    try:
        flights = search_flights(dep, arr)

        if not flights:
            return jsonify({
                "message": "No flights found"
            }), 404

        flights = sort_by_departure(flights)

        return jsonify(flights)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ROUND TRIP SEARCH ⭐
@app.route("/roundtrip")
def roundtrip():

    dep = request.args.get("dep", "").upper()
    arr = request.args.get("arr", "").upper()

    if not validate_airport(dep) or not validate_airport(arr):
        return jsonify({
            "error": "Invalid airport code"
        }), 400

    try:
        onward = search_flights(dep, arr)
        return_back = search_flights(arr, dep)

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