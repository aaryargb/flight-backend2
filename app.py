from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = "1429a31d187da7dbdd146e1750867b0a"


@app.route("/")
def home():
    return "Flight Backend Running"


@app.route("/flights")
def flights():

    dep = request.args.get("dep", "").upper()
    arr = request.args.get("arr", "").upper()

    if len(dep) != 3 or len(arr) != 3:
        return jsonify({"error": "Invalid airport code"}), 400

    url = "http://api.aviationstack.com/v1/flights"

    params = {
        "access_key": API_KEY,
        "dep_iata": dep,
        "arr_iata": arr
    }

    try:
        res = requests.get(url, params=params)
        data = res.json()

        results = []

        for f in data.get("data", [])[:10]:
            results.append({
                "airline": f["airline"]["name"],
                "flight_number": f["flight"]["iata"],
                "departure_airport": f["departure"]["airport"],
                "arrival_airport": f["arrival"]["airport"],
                "departure_time": f["departure"]["scheduled"],
                "arrival_time": f["arrival"]["scheduled"],
                "status": f["flight_status"],
                "booking_link": "https://www.google.com/travel/flights"
            })

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()
