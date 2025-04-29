# Import external libraries
import requests

from datetime import datetime
from tabulate import tabulate

# Import necessary items from other files
from realtime_trains_py.internal.details import ServiceData, CallingPoint
from realtime_trains_py.internal.utilities import create_file, format_time, validate_date, validate_uid


# Class for getting and creating service details
class ServiceDetails:
    def __init__(self, username: str=None, password: str=None, complexity: str="s") -> None:
        self.__username = username
        self.__password = password
        self.__complexity = complexity

    # Get the service details
    def _get_service_details(self, service_uid: str, date: str=None) -> ServiceData | str:
        if not validate_uid(service_uid):
            # Check if the Service UID is valid. If not, raise an error
            raise ValueError("400: Invalid Service UID. The service UID provided did not meet requirements or fall into the valid range.")

        if date is not None and not validate_date(date):
            # If a date is provided and it isn't valid, raise an error
            raise ValueError("400: Invalid date. The date provided did not meet requirements or fall into the valid date range.")

        elif date is None:
            # If a date isn't provided, set the date to be now
            date = (datetime.now()).strftime("%Y/%m/%d")

        # Get the api response using the auth details provided
        api_response = requests.get(f"https://api.rtt.io/api/v1/json/service/{service_uid}/{date}", auth=(self.__username, self.__password))

        if api_response.status_code == 200:
            service_data = api_response.json()

            if self.__complexity == "c":
                date_parts = date.split("/")

                # Set the file name
                file_name = f"{service_uid}_on_{date_parts[0]}.{date_parts[1]}.{date_parts[2]}_service_data"

                # Create a new file
                create_file(file_name, service_data)

                return f"Service data saved to file: \n  {file_name}"

            try:
                return create_service_record(self.__complexity, service_data, service_uid)

            except:
                # If an item couldn't be found, raise an error
                raise Exception("500: An error occurred while fetching service data. This is likely because the API response didn't provide the desired data.")

        elif api_response.status_code == 404:
            # Raise an error if either status codes are 404 (Not found)
            raise Exception("404: The data you requested could not be found.")

        elif api_response.status_code == 401 or api_response.status_code == 403:
            # Raise an error if either status codes are 401 (Unauthorised) or 403 (Forbidden)
            raise Exception(f"{api_response.status_code}: Access blocked. Check your credentials.")

        else:
            # Raise an error for any other status codes
            raise Exception(f"{api_response.status_code}: Failed to connect to the RTT API server. Try again in a few minutes.")


def create_service_record(complexity: str, service_data, service_uid) -> str:  
    service_type = service_data["serviceType"]      
    calling_points: list = []
    power_type = train_class= "Unknown"

    train_id = service_data["trainIdentity"]  # Get the train ID
    operator = service_data["atocName"]  # Get the operator

    # Check if the power type is in data
    if "powerType" in service_data:
        power_type = service_data["powerType"]

    elif service_type == "bus":
        power_type = "BUS"

    # Check if the train class is in data
    if "trainClass" in service_data:
        train_class = service_data["trainClass"]

    elif service_type == "bus":
        train_class = "BUS"

    for data in service_data["origin"]:
        origin = data["description"]  # Set the origin
        start_time = format_time(data["publicTime"])  # Set the start time

    for data in service_data["destination"]:
        destination = data["description"]  # Set the destination
        end_time = format_time(data["publicTime"])  # Set the end time

    for locations in service_data["locations"]:
        calling_point = get_calling_point(locations, service_type)
        
        if complexity == "a" or complexity == "a.p":
            calling_points.append([calling_point.stop_name, calling_point.booked_arrival, calling_point.realtime_arrival, calling_point.platform, calling_point.line, calling_point.booked_departure, calling_point.realtime_departure])

        elif complexity == "s" or complexity == "s.p":
            calling_points.append([calling_point.stop_name, calling_point.booked_arrival, calling_point.realtime_arrival, calling_point.platform, calling_point.booked_departure, calling_point.realtime_departure])
        
        elif complexity.endswith("n"):
            calling_points.append(calling_point)

    if complexity == "a" or complexity == "a.p":
        print(f"{train_id} ({service_uid}) \n  {start_time} {origin} to {destination} \n  Pathed as {power_type}: train class {train_class} \n  Operated by {operator} \n\n  Generated at {datetime.now().strftime("%H:%M:%S on %d/%m/%y.")}")

        # Print the table for the service
        print(tabulate(calling_points, tablefmt="rounded_grid",
                headers=["Stop Name", "Booked Arrival", "Actual Arrival", "Platform", "Line", "Booked Departure", "Actual Departure"]
        ))

    elif complexity == "s" or complexity == "s.p":
        print(f"{train_id} ({service_uid}) \n  {start_time} {origin} to {destination} \n  Operated by {operator} \n\n  Generated at {datetime.now().strftime("%H:%M:%S on %d/%m/%y.")}")

        # Print the table for the service
        print(tabulate(calling_points, tablefmt="rounded_grid",
                headers=["Stop Name", "Booked Arrival", "Actual Arrival", "Platform", "Booked Departure", "Actual Departure"]
        ))

        return "200: Service data returned successfully."
    
    return ServiceData(train_id, service_uid, operator, origin, destination, calling_points, start_time, end_time, power_type, train_class)


def get_calling_point(location, service_type) -> CallingPoint:
    realtime_arrival = realtime_departure = booked_arrival = booked_departure = line = platform = ""

    stop_name = location["description"]
    call_type = location["displayAs"]

    if "realtimeArrival" in location:
        realtime_arrival = format_time(location["realtimeArrival"])

    if call_type == "CANCELLED_CALL" and realtime_arrival != "":
        realtime_arrival = "Cancelled"

    if "gbttBookedArrival" in location:
        booked_arrival = format_time(location["gbttBookedArrival"])

    if "realtimeDeparture" in location:
        realtime_departure = format_time(location["realtimeDeparture"])

    if call_type == "CANCELLED_CALL" and realtime_departure != "":
        realtime_departure = "Cancelled"

    if "gbttBookedDeparture" in location:
        booked_departure = format_time(location["gbttBookedDeparture"])

    if "platform" in location:
        platform = location["platform"]

    elif service_type == "bus":
        platform = "BUS"

    if "line" in location:
        line = location["line"]

    return CallingPoint(stop_name, booked_arrival, realtime_arrival, platform, line, booked_departure, realtime_departure)