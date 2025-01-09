import requests

from datetime import datetime
from tabulate import tabulate

# Import functions from utilities
try:
    from realtime_trains_py.services.utilities import create_file, format_time, validate_date, validate_uid
except:
    from services.utilities import create_file, format_time, validate_date, validate_uid


# Simple version of the service
class ServiceSimple():
    def __init__(self, train_id, service_uid, operator, origin, destination, all_calling_points, start_time):
        self.train_id = train_id
        self.service_uid = service_uid
        self.operator = operator
        self.origin = origin
        self.destination = destination
        self.all_calling_points = all_calling_points
        self.start_time = start_time

# Simple version of calling points
class CallingPointsSimple():
    def __init__(self, stop_name, booked_arrival, realtime_arrival, platform, booked_departure, realtime_departure):
        self.stop_name = stop_name
        self.booked_arrival = booked_arrival
        self.realtime_arrival = realtime_arrival
        self.platform = platform
        self.booked_departure = booked_departure
        self.realtime_departure = realtime_departure

# Advanced version of the service
class ServiceAdvanced():
    def __init__(self, train_id, service_uid, operator, origin, destination, all_calling_points, start_time, end_time, power, train_class):
        self.train_id = train_id
        self.service_uid = service_uid
        self.operator = operator
        self.origin = origin
        self.destination = destination
        self.all_calling_points = all_calling_points
        self.start_time = start_time
        self.end_time = end_time
        self.power = power
        self.train_class = train_class

# Advanced version of calling points
class CallingPointsAdvanced():
    def __init__(self, stop_name, booked_arrival, realtime_arrival, platform, line, booked_departure, realtime_departure):
        self.stop_name = stop_name
        self.booked_arrival = booked_arrival
        self.realtime_arrival = realtime_arrival
        self.platform = platform
        self.line = line
        self.booked_departure = booked_departure
        self.realtime_departure = realtime_departure


class ServiceDetails():
    def __init__(self, username: str = None, password: str = None, complexity: str = "s") -> None:
        self.__username = username
        self.__password = password
        self.__complexity = complexity

    # Get the service details
    def _get_service_details(self, service_uid: str, date: str | None) -> ServiceAdvanced | ServiceSimple | str:
        if not validate_uid(service_uid):
            # Check if the Service UID is valid. If not, raise an error 
            raise ValueError("Invalid Service UID. The service UID provided did not meet requirements or fall into the valid range.")
        
        if date is not None and not validate_date(date):
            # If a date is provided and it isn't valid, raise an error
            raise ValueError("Invalid date. The date provided did not meet requirements or fall into the valid date range.")
        
        elif date is None:
            # If a date isn't provided, set the date to be now
            date = (datetime.now()).strftime("%Y/%m/%d")

        # Get the api response using the auth details provided
        api_response =  requests.get(f"https://api.rtt.io/api/v1/json/service/{service_uid}/{date}", auth = (self.__username, self.__password))

        if api_response.status_code == 200:
            service_data = api_response.json()
            
            if self.__complexity == "c":
                # Split the date by each "/"
                date_parts = date.split("/")

                # Set the file name
                file_name = f"{service_uid}_on_{date_parts[0]}.{date_parts[1]}.{date_parts[2]}_service_data"

                # Create a new file
                create_file(file_name, service_data)

                return f"Service data saved to file: \n  {file_name}" 
            
            try:
                if self.__complexity == "a.p" or self.__complexity == "a":
                    # If complexity is advanced (prettier), run advanced_prettier for data
                    return self.__advanced_prettier(service_data, service_uid)

                elif self.__complexity == "a.n":
                    # If complexity is advanced (normal), run advanced_normal for data
                    return self.__advanced_normal(service_data, service_uid)
                
                elif self.__complexity == "s.p" or self.__complexity == "s":
                    # If complexity is simple (prettier), run simple_prettier for data
                    return self.__simple_prettier(service_data, service_uid)

                elif self.__complexity == "s.n":
                    # If complexity is simple (normal), run simple_normal for data
                    return self.__simple_normal(service_data, service_uid)
            
            except:
                # If an item couldn't be found, raise an error
                raise Exception("An error occurred while fetching service data. This is likely because the API response didn't provide the desired data.")
        
        elif api_response.status_code == 404:
            # Raise an error if either status codes are 404 (Not found)
            raise Exception(f"The data you requested could not be found. Status codes: {api_response.status_code}")
        
        elif api_response.status_code == 401 or api_response.status_code == 403:
            # Raise an error if either status codes are 401 (Unauthorised) or 403 (Forbidden)
            raise Exception(f"Access blocked: check your credentials. Status code: {api_response.status_code}")

        else:
            # Raise an error for any other status codes
            raise Exception(f"Failed to connect to the RTT API server. Try again in a few minutes. Status code: {api_response.status_code}")

    # Advanced Normal
    def __advanced_normal(self, service_data, service_uid) -> None | ServiceAdvanced | str:
        service_type = service_data["serviceType"] # Type of service

        # Check for the type of service
        if service_type == "train":
            train_id = service_data["trainIdentity"] # Get the train ID
            operator = service_data["atocName"] # Get the operator
            
            # Check if the power type is in the data    
            if "powerType" in service_data:
                power_type = service_data["powerType"]
            else:
                power_type = "unknown"

            # Check if the train class is in the data    
            if "trainClass" in service_data:
                train_class = service_data["trainClass"]
            else:
                train_class = "unknown"

            for data in service_data["origin"]:
                origin = data["description"] # Set the origin
                start_time = format_time(data["publicTime"]) # Set the start time

            for data in service_data["destination"]:
                destination = data["description"] # Set the destination
                end_time = format_time(data["publicTime"]) # Set the end time

            # Create a new calling points list
            all_calling_points: list = []

            for locations in service_data["locations"]:
                stop_name = locations["description"] # Set the stop name
                call_type = locations["displayAs"] # Set the type of call

                # Check if realtime arrival is in locations
                if "realtimeArrival" in locations:
                    # Format the time of the realtime arrival
                    realtime_arrival = format_time(locations["realtimeArrival"])
                else:
                    realtime_arrival = ""

                # Check if the call type is cancelled and realtime arrival is not null
                if call_type == "CANCELLED_CALL" and realtime_arrival != "":
                    realtime_arrival = "Cancelled"

                # Check if booked arrival is in locations
                if "gbttBookedArrival" in locations:
                    # Format the time of the booked arrival
                    booked_arrival = format_time(locations["gbttBookedArrival"])
                else:
                    booked_arrival = ""

                # Check if realtime departure is in locations
                if "realtimeDeparture" in locations:
                    # Format the time of the realtime departure
                    realtime_departure = format_time(locations["realtimeDeparture"])
                else:
                    realtime_departure = ""

                # Check if the call type is cancelled and realtime departure is not null
                if call_type == "CANCELLED_CALL" and realtime_departure != "":
                    realtime_departure = "Cancelled"

                # Check if booked departure is in locations
                if "gbttBookedDeparture" in locations:
                    # Format the time of the booked departure
                    booked_departure = format_time(locations["gbttBookedDeparture"])
                else:
                    booked_departure = ""

                # Check if platform is in locations
                if "platform" in locations:
                    platform = locations["platform"]
                else:
                    platform = "-"

                # Check if line is in locations
                if "line" in locations:
                    line = locations["line"]
                else:
                    line = "-"

                # Append new CallingPointsAdvanced to the all calling points list
                all_calling_points.append(CallingPointsAdvanced(stop_name, booked_arrival, realtime_arrival, platform, line, booked_departure, realtime_departure))

            return ServiceAdvanced(train_id, service_uid, operator, origin, destination, all_calling_points, start_time, end_time, power_type, train_class)
        
        elif service_type == "bus":
            train_id = service_data["trainIdentity"] # Get the train ID
            operator = service_data["atocName"] # Get the operator

            for data in service_data["origin"]:
                origin = data["description"] # Set the origin
                start_time = format_time(data["publicTime"]) # Set the start time

            for data in service_data["destination"]:
                destination = data["description"] # Set the destination
                end_time = format_time(data["publicTime"]) # Set the end time

            # Create a new calling points list
            all_calling_points: list = []

            for locations in service_data["locations"]:
                stop_name = locations["description"] # Set the stop name
                call_type = locations["displayAs"] # Set the type of call

                # Check if realtime arrival is in locations
                if "realtimeArrival" in locations:
                    # Format the time of the realtime arrival
                    realtime_arrival = format_time(locations["realtimeArrival"])
                else:
                    realtime_arrival = ""

                # Check if the call type is cancelled and realtime arrival is not null
                if call_type == "CANCELLED_CALL" and realtime_arrival != "":
                    realtime_arrival = "Cancelled"

                # Check if booked arrival is in locations
                if "gbttBookedArrival" in locations:
                    # Format the time of the booked arrival
                    booked_arrival = format_time(locations["gbttBookedArrival"])
                else:
                    booked_arrival = ""

                # Check if realtime departure is in locations
                if "realtimeDeparture" in locations:
                    # Format the time of the realtime departure
                    realtime_departure = format_time(locations["realtimeDeparture"])
                else:
                    realtime_departure = ""

                # Check if the call type is cancelled and realtime departure is not null
                if call_type == "CANCELLED_CALL" and realtime_departure != "":
                    realtime_departure = "Cancelled"

                # Check if booked departure is in locations
                if "gbttBookedDeparture" in locations:
                    # Format the time of the booked departure
                    booked_departure = format_time(locations["gbttBookedDeparture"])
                else:
                    booked_departure = ""

                all_calling_points.append(CallingPointsAdvanced(stop_name, booked_arrival, realtime_arrival, "BUS", "-", booked_departure, realtime_departure))

            return ServiceAdvanced(train_id, service_uid, operator, origin, destination, all_calling_points, start_time, end_time, "BUS", "BUS")
        
        else:
            raise Exception("The service type of this service wasn't recognised.")
        
    # Advanced Prettier
    def __advanced_prettier(self, service_data, service_uid) -> None | str:
        service_type = service_data["serviceType"] # Type of service

        # Check for the type of service
        if service_type == "train":
            train_id = service_data["trainIdentity"] # Get the train ID
            operator = service_data["atocName"] # Get the operator

            # Check if the power type is in data
            if "powerType" in service_data:
                power_type = service_data["powerType"]
            else:
                power_type = "unknown"

            # Check if the train class is in data
            if "trainClass" in service_data:
                train_class = service_data["trainClass"]
            else:
                train_class = "unknown"

            for data in service_data["origin"]:
                origin = data["description"] # Set the origin
                start_time = format_time(data["publicTime"]) # Set the start time

            for data in service_data["destination"]:
                destination = data["description"] # Set the destination

            # Create a new calling points list
            all_calling_points: list = []

            for locations in service_data["locations"]:
                stop_name = locations["description"] # Set the stop name
                call_type = locations["displayAs"] # Set the type of call

                # Check if realtime arrival is in locations
                if "realtimeArrival" in locations:
                    # Format the time of the realtime arrival
                    realtime_arrival = format_time(locations["realtimeArrival"])
                else:
                    realtime_arrival = ""

                # Check if the call type is cancelled and realtime arrival is not null
                if call_type == "CANCELLED_CALL" and realtime_arrival != "":
                    realtime_arrival = "Cancelled"

                # Check if booked arrival is in locations
                if "gbttBookedArrival" in locations:
                    # Format the time of the booked arrival
                    booked_arrival = format_time(locations["gbttBookedArrival"])
                else:
                    booked_arrival = ""

                # Check if realtime departure is in locations
                if "realtimeDeparture" in locations:
                    # Format the time of the realtime departure
                    realtime_departure = format_time(locations["realtimeDeparture"])
                else:
                    realtime_departure = ""

                # Check if the call type is cancelled and realtime departure is not null
                if call_type == "CANCELLED_CALL" and realtime_departure != "":
                    realtime_departure = "Cancelled"

                # Check if booked departure is in locations
                if "gbttBookedDeparture" in locations:
                    # Format the time of the booked departure
                    booked_departure = format_time(locations["gbttBookedDeparture"])
                else:
                    booked_departure = ""

                # Check if platform is in locations
                if "platform" in locations:
                    platform = locations["platform"]
                else:
                    platform = "-"

                # Check if line is in locations
                if "line" in locations:
                    line = locations["line"]
                else:
                    line = "-"

                # Append the details of the calling point to the all calling points list
                all_calling_points.append([stop_name, booked_arrival, realtime_arrival, platform, line, booked_departure, realtime_departure])

            # Print the service details 
            print(f"{train_id} ({service_uid}) \n  {start_time} {origin} to {destination} \n  Pathed as {power_type}: train class {train_class} \n  Operated by {operator} \n\n  Generated at {datetime.now().strftime("%H:%M:%S on %d/%m/%y.")}")

            # Print the table for the service
            print(tabulate(
                all_calling_points, 
                tablefmt = "rounded_grid", 
                headers = ["Stop Name", 
                            "Booked Arrival", 
                            "Actual Arrival", 
                            "Platform", 
                            "Line", 
                            "Booked Departure", 
                            "Actual Departure"]
                )
            )

            return "Service data returned successfully"

        elif service_type == "bus":
            train_id = service_data["trainIdentity"] # Get the train ID
            operator = service_data["atocName"] # Get the operator

            for data in service_data["origin"]:
                origin = data["description"] # Set the origin
                start_time = format_time(data["publicTime"]) # Set the start time

            for data in service_data["destination"]:
                destination = data["description"] # Set the destination

            # Create a new calling points list
            all_calling_points: list = []

            for locations in service_data["locations"]:
                stop_name = locations["description"] # Set the stop name
                call_type = locations["displayAs"] # Set the type of call

                # Check if realtime arrival is in locations
                if "realtimeArrival" in locations:
                    # Format the time of the realtime arrival
                    realtime_arrival = format_time(locations["realtimeArrival"])
                else:
                    realtime_arrival = ""

                # Check if the call type is cancelled and realtime arrival is not null
                if call_type == "CANCELLED_CALL" and realtime_arrival != "":
                    realtime_arrival = "Cancelled"

                # Check if booked arrival is in locations
                if "gbttBookedArrival" in locations:
                    # Format the time of the booked arrival
                    booked_arrival = format_time(locations["gbttBookedArrival"])
                else:
                    booked_arrival = ""

                # Check if realtime departure is in locations
                if "realtimeDeparture" in locations:
                    # Format the time of the realtime departure
                    realtime_departure = format_time(locations["realtimeDeparture"])
                else:
                    realtime_departure = ""

                # Check if the call type is cancelled and realtime departure is not null
                if call_type == "CANCELLED_CALL" and realtime_departure != "":
                    realtime_departure = "Cancelled"

                # Check if booked departure is in locations
                if "gbttBookedDeparture" in locations:
                    # Format the time of the booked departure
                    booked_departure = format_time(locations["gbttBookedDeparture"])
                else:
                    booked_departure = ""

                # Append the details of the calling point to the all calling points list
                all_calling_points.append([stop_name, booked_arrival, realtime_arrival, "BUS", "-", booked_departure, realtime_departure])

            # Print the service details 
            print(f"{train_id} ({service_uid}) \n  {start_time} {origin} to {destination} \n  Pathed as BUS: train class BUS \n  Operated by {operator} \n\n  Generated at {datetime.now().strftime("%H:%M:%S on %d/%m/%y.")}")

            # Print the table for the service
            print(tabulate(
                all_calling_points, 
                tablefmt = "rounded_grid", 
                headers = ["Stop Name", 
                            "Booked Arrival", 
                            "Actual Arrival", 
                            "Platform", 
                            "Line", 
                            "Booked Departure", 
                            "Actual Departure"]
                )
            )

            return "Service data returned successfully"

        else:
            raise Exception("The service type of this service wasn't recognised.")
        
    # Simple Normal
    def __simple_normal(self, service_data, service_uid) -> ServiceSimple:
        train_id = service_data["trainIdentity"] # Get the train ID
        operator = service_data["atocName"] # Get the operator

        # Pop the origin
        origin = service_data["origin"].pop()["description"]
        start_time = "None"

        # Pop the destination
        destination = (service_data["destination"]).pop()["description"]

        # Create a new calling points list
        all_calling_points: list = []

        for locations in service_data["locations"]:
            stop_name = locations["description"] # Set the stop name
            call_type = locations["displayAs"] # Set the type of call

            # Check if realtime arrival is in locations
            if "realtimeArrival" in locations:
                # Format the time of the realtime arrival
                realtime_arrival = format_time(locations["realtimeArrival"])
            else:
                realtime_arrival = ""

            # Check if the call type is cancelled and realtime arrival is not null
            if call_type == "CANCELLED_CALL" and realtime_arrival != "":
                realtime_arrival = "Cancelled"

            # Check if booked arrival is in locations
            if "gbttBookedArrival" in locations:
                # Format the time of the booked arrival
                booked_arrival = format_time(locations["gbttBookedArrival"])
            else:
                booked_arrival = ""

            # Check if realtime departure is in locations
            if "realtimeDeparture" in locations:
                # Format the time of the realtime departure
                realtime_departure = format_time(locations["realtimeDeparture"])
            else:
                realtime_departure = ""

            # Check if the call type is cancelled and realtime departure is not null
            if call_type == "CANCELLED_CALL" and realtime_departure != "":
                realtime_departure = "Cancelled"

            # Check if booked departure is in locations
            if "gbttBookedDeparture" in locations:
                # Format the time of the booked departure
                booked_departure = format_time(locations["gbttBookedDeparture"])
            else:
                booked_departure = ""

            # Check if the start time is none
            if start_time == "None":
                # Set the start time to the booked departure
                start_time = booked_departure

            # Check if platform is in locations
            if "platform" in locations:
                platform = locations["platform"]
            else:
                platform = "-"

            # Append new CallingPointsAdvanced to the all calling points list
            all_calling_points.append(CallingPointsSimple(stop_name, booked_arrival, realtime_arrival, platform, booked_departure, realtime_departure))

        return ServiceSimple(train_id, service_uid, operator, origin, destination, all_calling_points, start_time)

    # Simple Prettier
    def __simple_prettier(self, service_data, service_uid) -> str:
        train_id = service_data["trainIdentity"] # Get the train ID
        operator = service_data["atocName"] # Get the operator

        # Pop the origin
        origin = service_data["origin"].pop()["description"]
        start_time = "None"

        # Pop the destination
        destination = (service_data["destination"]).pop()["description"]

        # Create a new calling points list
        all_calling_points: list = []

        for locations in service_data["locations"]:
            stop_name = locations["description"] # Set the stop name
            call_type = locations["displayAs"] # Set the type of call

            # Check if realtime arrival is in locations
            if "realtimeArrival" in locations:
                # Format the time of the realtime arrival
                realtime_arrival = format_time(locations["realtimeArrival"])
            else:
                realtime_arrival = ""

            # Check if the call type is cancelled and realtime arrival is not null
            if call_type == "CANCELLED_CALL" and realtime_arrival != "":
                realtime_arrival = "Cancelled"

            # Check if booked arrival is in locations
            if "gbttBookedArrival" in locations:
                # Format the time of the booked arrival
                booked_arrival = format_time(locations["gbttBookedArrival"])
            else:
                booked_arrival = ""

            # Check if realtime departure is in locations
            if "realtimeDeparture" in locations:
                # Format the time of the realtime departure
                realtime_departure = format_time(locations["realtimeDeparture"])
            else:
                realtime_departure = ""

            # Check if the call type is cancelled and realtime departure is not null
            if call_type == "CANCELLED_CALL" and realtime_departure != "":
                realtime_departure = "Cancelled"

            # Check if booked departure is in locations
            if "gbttBookedDeparture" in locations:
                # Format the time of the booked departure
                booked_departure = format_time(locations["gbttBookedDeparture"])
            else:
                booked_departure = ""

            # Check if the start time is none
            if start_time == "None":
                # Set the start time to the booked departure
                start_time = booked_departure

            # Check if platform is in locations
            if "platform" in locations:
                platform = locations["platform"]
            else:
                platform = "-"

            all_calling_points.append([stop_name, booked_arrival, realtime_arrival, platform, booked_departure, realtime_departure])

        # Print the service details 
        print(f"{train_id} ({service_uid}) {start_time} {origin} to {destination}. \n Operated by {operator}. \n\n Generated at {datetime.now().strftime("%H:%M:%S on %d/%m/%y.")}")
        
        # Print the table for the service
        print(tabulate(
            all_calling_points, 
            tablefmt = "rounded_grid", 
            headers = ["Stop Name", 
                        "Booked Arrival", 
                        "Actual Arrival", 
                        "Platform", 
                        "Booked Departure", 
                        "Actual Departure"]
            )
        )

        return "Service data returned successfully"