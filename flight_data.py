class FlightData:
    """This class is responsible for structuring the flight data."""
    def __init__(self, price, dep_airport_code, dep_city, arr_airport_code, arr_city, out_date, return_date, stop_overs=0, via_city=""):
        self.price = price
        self.departure_airport_code = dep_airport_code
        self.departure_city = dep_city
        self.arrival_airport_code = arr_airport_code
        self.arrival_city = arr_city
        self.out_date = out_date
        self.return_date = return_date

        self.stop_overs = stop_overs
        self.via_city = via_city