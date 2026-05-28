# Import external libraries
import requests

from datetime import datetime
from tabulate import tabulate

# Import necessary items from other files
from realtime_trains_py.internal.details import ServiceData, CallingPoint
from realtime_trains_py.internal.errors import APIResponseError, NoDataFound
from realtime_trains_py.internal.utilities import create_file, validate_date, validate_uid


# Class for getting and creating service details
class ServiceDetails:
    def __init__(self, request_token: str, complexity: str="s") -> None:
        self.__headers = {"Accept": "application/json", "Authorization": f"Bearer {request_token}"}
        self.__complexity = complexity

    # Get the service details
    def _get_service_details(self, service_uid: str, date: str | None=None) -> ServiceData:
        validate_uid(service_uid)

        if date == None:
            date = datetime.now().strftime("%Y-%m-%d")

        else:
            validate_date(date)

        # Get the api response using the auth details provided
        api_response = requests.get(f"https://data.rtt.io/rtt/service", params={"uniqueIdentity": f"gb-nr:{service_uid}:{date}",}, headers=self.__headers)

        if api_response.status_code == 200:
            service_data = api_response.json()

            if self.__complexity == "c":
                date_parts = date.split("-")

                # Set the file name
                file_name = f"{service_uid}_on_{date_parts[0]}.{date_parts[1]}.{date_parts[2]}_service_data"

                # Create a new file
                create_file(file_name, service_data)

                print(f"Service data saved to file: \n  {file_name}")
                # Return an empty ServiceData object since the data is saved to a file and not returned as an object
                return ServiceData("", "", "", "", [], "", "", 0) 

            return self._create_service_record(service_data, service_uid)

        elif api_response.status_code == 404:
           raise NoDataFound()

        else:
            raise APIResponseError(f"Failed to connect to the RTT API server: {api_response.status_code} \nResponse message: {api_response.text}")


    def _create_service_record(self,service_data, service_uid) -> ServiceData:  
        # Extract the relevant data from the API response and create a ServiceData object to return
        operator = service_data["scheduleMetadata"]["operator"].pop("name")
        origin = service_data["origin"][0]["location"].pop("description")
        start_time = service_data["origin"][0]["temporalData"].pop("scheduleAdvertised").split("T")[1][:5]
        destination = service_data["destination"][0]["location"].pop("description")
        end_time = service_data["destination"][0]["temporalData"].pop("scheduleAdvertised").split("T")[1][:5]
        coaches = 0

        calling_points: list[CallingPoint] = []
        calling_point_data: list[list[str]] = []

        # Loop through the locations in the service data and create CallingPoint objects for each location. If the complexity is simple, 
        # also create a 2D array to print as a table later.
        for locations in service_data["locations"]:
            calling_point = get_calling_point(locations)

            if calling_point.coaches != 0:
                coaches = calling_point.coaches
            
            if self.__complexity == "s":
                calling_point_data.append([
                    calling_point.stop_name,
                    calling_point.scheduled_arrival,
                    calling_point.expected_arrival,
                    calling_point.platform,
                    calling_point.line,
                    calling_point.scheduled_departure,
                    calling_point.expected_departure,
                    ])
                
            else:
                calling_points.append(calling_point)

        if self.__complexity == "s":
            if coaches != 0:
                print(f"{service_uid} \n  {start_time} {origin} to {destination} \n  A {operator} service formed of {coaches} coaches.\n\n  Generated at {datetime.now().strftime('%H:%M:%S on %d/%m/%y.')}")


            else:
                print(f"{service_uid} \n  {start_time} {origin} to {destination} \n  Operated by {operator} \n\n  Generated at {datetime.now().strftime('%H:%M:%S on %d/%m/%y.')}")

            # Print the table for the service and return an empty ServiceData object since the data is printed and not returned as an object
            print(tabulate(calling_point_data, tablefmt="rounded_grid",
                    headers=["Stop Name", "Scheduled Arrival", "Expected Arrival", "Platform", "Line", "Scheduled Departure", "Expected Departure"]
            ))
            return ServiceData("", "", "", "", [], "", "", 0)
        
        return ServiceData(service_uid, operator, origin, destination, calling_points, start_time, end_time, coaches)

    

def get_calling_point(location) -> CallingPoint:
    # Initialize variables to store the calling point data. Set default values for all variables in case some data is missing from the API response.
    stop_name = scheduled_arrival = expected_arrival = platform = line = scheduled_departure = expected_departure = ""
    coaches = 0

    temporal_data = location["temporalData"]
    location_data = location["locationMetadata"]
    stop_name = location["location"].pop("description")

    # Extract arrival data if it exists. If the service is cancelled, set the expected arrival to "Cancelled". If the service 
    # has an actual arrival time, use that as the expected arrival. If the service has a forecast arrival time, use that as the 
    # expected arrival. If the expected arrival time is the same as the scheduled arrival time, set the expected arrival to 
    # "On time" or "Arrived on time" depending on whether it has arrived or not.
    if "arrival" in temporal_data:
        is_cancelled = temporal_data["arrival"]["isCancelled"]
        scheduled_arrival = temporal_data["arrival"]["scheduleAdvertised"].split("T")[1][:5]

        if is_cancelled:
            expected_arrival = "Cancelled"
        
        elif "realtimeActual" in temporal_data["arrival"]:
            expected_arrival = temporal_data["arrival"]["realtimeActual"].split("T")[1][:5]
            if expected_arrival == scheduled_arrival:
                expected_arrival = "Arrived on time"

        elif "realtimeForecast" in temporal_data["arrival"]:
            expected_arrival = temporal_data["arrival"]["realtimeForecast"].split("T")[1][:5]
            if expected_arrival == scheduled_arrival:
                expected_arrival = "On time"

    # Extract departure data if it exists. If the service is cancelled, set the expected departure to "Cancelled". If the service 
    # has an actual departure time, use that as the expected departure. If the service has a forecast departure time, use that as the 
    # expected departure. If the expected departure time is the same as the scheduled departure time, set the expected departure to 
    # "On time" or "Departed on time" depending on whether it has departed or not.
    if "departure" in temporal_data:
        is_cancelled = temporal_data["departure"]["isCancelled"]
        scheduled_departure = temporal_data["departure"]["scheduleAdvertised"].split("T")[1][:5]
        if is_cancelled:
            expected_departure = "Cancelled"

        elif "realtimeActual" in temporal_data["departure"]:
            expected_departure = temporal_data["departure"]["realtimeActual"].split("T")[1][:5]
            if expected_departure == scheduled_departure:
                expected_departure = "Departed on time"

        elif "realtimeForecast" in temporal_data["departure"]:
            expected_departure = temporal_data["departure"]["realtimeForecast"].split("T")[1][:5] 
            if expected_departure == scheduled_departure:
                expected_departure = "On time"  

    # Extract platform data if it exists
    if "platform" in location_data:
        if "forecast" in location_data["platform"]:
            platform = location_data["platform"]["forecast"]

        else:
            platform = location_data["platform"]["actual"]

    # Extract line data if it exists
    if "line" in location_data:
        if "forecast" in location_data["line"]:
            line = location_data["line"]["forecast"]

        else:
            line = location_data["line"]["actual"]

    # If a number of coaches is given in the location data, get the number of coaches for the calling point. This is 
    # usually the same throughout the service, but if it's given for any other calling point, it can mean that the service
    # gains or loses coaches.
    if "numberOfVehicles" in location["locationMetadata"]:
        coaches = location["locationMetadata"].pop("numberOfVehicles")

    return CallingPoint(stop_name, scheduled_arrival, expected_arrival, platform, line, scheduled_departure, expected_departure, coaches)