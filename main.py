from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager
# from pprint import pprint


data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
user_emails = data_manager.get_email()
flight_search = FlightSearch()
notification_manager = NotificationManager()


ORIGIN_CITY_IATA = "LON"


if sheet_data[0]["iataCode"] == "":
    from flight_search import FlightSearch
    flight_search = FlightSearch()
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    print(f"sheet_data:\n {sheet_data}")
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()


today = datetime.utcnow()
tomorrow = (today + timedelta(days=1)).strftime("%d/%m/%Y")
six_months_from_today = (today + timedelta(days=(6 * 30))).strftime("%d/%m/%Y")

for destination in sheet_data:
    flight = flight_search.search_flights(
        departure_city_code=ORIGIN_CITY_IATA,
        destination_city_code=destination["iataCode"],
        from_date=tomorrow,
        to_date=six_months_from_today
    )

    if flight is None:
        continue

    if destination["lowestPrice"] >= flight.price:
        message = f"Low Price Alert! Only £{flight.price} to fly " \
                  f"from {flight.departure_city}-{flight.departure_airport_code} to " \
                  f"{flight.arrival_city}-{flight.arrival_airport_code}, " \
                  f"from {flight.out_date} to {flight.return_date}.\n" \
                  f"https://www.google.co.uk/flights?hl=en#flt={flight.departure_airport_code}.{flight.arrival_airport_code}" \
                  f".{flight.out_date}*{flight.arrival_airport_code}.{flight.departure_airport_code}.{flight.return_date}"

        for user in user_emails:
            notification_manager.send_email(email=user["email"], message=message)
