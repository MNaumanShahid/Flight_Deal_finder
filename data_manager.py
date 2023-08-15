import requests
import os
from pprint import pprint


URL = os.environ.get("SH_URL")
USER_URL = os.environ.get("USER_URL")
TOKEN = {
            "authorization": os.environ.get("SH_TOKEN")
        }


class DataManager:
    """This class is responsible for talking to the Google Sheet."""
    def __init__(self):
        self.destination_data = {}
        self.users_email = {}

    def get_destination_data(self):
        response = requests.get(url=URL, headers=TOKEN)
        result = response.json()
        self.destination_data = result["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{URL}/{city['id']}",
                json=new_data,
                headers=TOKEN
            )
            print(response.text)

    def get_email(self):
        response = requests.get(url=USER_URL, headers=TOKEN)
        result = response.json()
        self.users_email = result["users"]
        return self.users_email
