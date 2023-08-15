import requests
from flight_data import FlightData
import pprint
import os

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
TEQUILA_APIKEY = os.environ.get("TEQ_APIKEY")


class FlightSearch:
    """This class is responsible for talking to the Flight Search API."""

    def get_destination_code(self, city_name):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        query = {
            "term": city_name,
            "location_types": "city"
        }
        response = requests.get(
            url=location_endpoint,
            params=query,
            headers={
                "apikey": TEQUILA_APIKEY
            }
        )

        result = response.json()

        code = result["locations"][0]["code"]
        return code

    def search_flights(self, departure_city_code, destination_city_code, from_date, to_date):
        search_endpoint = f"{TEQUILA_ENDPOINT}/v2/search"
        headers = {
            "apikey": TEQUILA_APIKEY
        }

        query = {
            "fly_from": departure_city_code,
            "fly_to": destination_city_code,
            "date_from": from_date,
            "date_to": to_date,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "curr": "GBP",
            "max_stopovers": 0,
            "one_for_city": 1
        }

        response = requests.get(url=search_endpoint, params=query, headers=headers)
        result = response.json()
        try:
            data = result["data"][0]
            print(f"{destination_city_code}: £{data['price']}")
        except IndexError:
            query["max_stopovers"] = 1
            response = requests.get(url=search_endpoint, params=query, headers=headers)
            result = response.json()
            pprint.pprint(result)
            data = result["data"][0]
            pprint.pprint(data)
            # print(f"No flights found for {destination_city_code}.")
            # return None
            flight_data = FlightData(
                price=data["price"],
                dep_airport_code=data["flyFrom"],
                dep_city=data["cityFrom"],
                arr_airport_code=data["flyTo"],
                arr_city=data["cityTo"],
                out_date=data["route"][0]["utc_departure"].split("T")[0],
                return_date=data["route"][1]["utc_departure"].split("T")[0],
                stop_overs=1,
                via_city=data["route"][0]["cityTo"]
            )
            return flight_data

        else:
            flight_data = FlightData(
                price=data["price"],
                dep_airport_code=data["flyFrom"],
                dep_city=data["cityFrom"],
                arr_airport_code=data["flyTo"],
                arr_city=data["cityTo"],
                out_date=data["route"][0]["utc_departure"].split("T")[0],
                return_date=data["route"][1]["utc_departure"].split("T")[0],
            )
            return flight_data
