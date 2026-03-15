import requests

API_KEY = "1429a31d187da7dbdd146e1750867b0a"

BASE_URL = "http://api.aviationstack.com/v1/flights"


def search_flights(dep, arr):

    params = {
        "access_key": API_KEY,
        "dep_iata": dep,
        "arr_iata": arr
    }

    response = requests.get(BASE_URL, params=params, timeout=15)

    data = response.json()

    flights = []

    for f in data.get("data", [])[:20]:

        flights.append({
            "airline": f["airline"]["name"],
            "flight_number": f["flight"]["iata"],
            "departure_airport": f["departure"]["airport"],
            "arrival_airport": f["arrival"]["airport"],
            "departure_time": f["departure"]["scheduled"],
            "arrival_time": f["arrival"]["scheduled"],
            "status": f["flight_status"],
            "booking_link": "https://www.google.com/travel/flights"
        })

    return flights


def sort_by_departure(flights):
    return sorted(flights, key=lambda x: str(x["departure_time"]))