# Import libraries
from datetime import datetime
from tabulate import tabulate

# Import functions from other files
try:
    from realtime_trains_py.internal.details import StationBoardDetails
    from realtime_trains_py.internal.merge_sort import merge_sort
    from realtime_trains_py.internal.utilities import format_time
except:
    from internal.details import StationBoardDetails
    from internal.merge_sort import merge_sort
    from internal.utilities import format_time


# Class for creating station boards
class NewStationBoard:
    # Initialise the board
    def __init__(self, departure_data, arrival_data) -> None:
        requested_location = departure_data["location"]["name"]  # Requested location

        # Compare the locations and check they're equal
        if requested_location == arrival_data["location"]["name"]:
            self._requested_location = requested_location

        else:
            raise Exception(
                "500: An unexpected error occurred handling your request. Try again in a few minutes."
            )

        # Create new empty boards
        arrival_board = []
        departure_board = []
        self._combined_board = []

        # Iterate over each service and append it to the departure board
        for dep_service in departure_data["services"]:
            departure_board.append(CreateBoardDetails()._create_dep_service(dep_service))

        # Iterate over each service and append it to the arrival board
        for arr_service in arrival_data["services"]:
            arrival_board.append(CreateBoardDetails()._create_arr_service(arr_service))

        # Iterate over each att in departure board
        for departures in departure_board:
            # Iterate over each att in arrival board
            for arrivals in arrival_board:
                # If the values at position 0 are equal, append it to the combined board
                if departures[0] == arrivals[0]:
                    # Overwrite the departure times
                    arrivals[1].realtime_departure = departures[1].realtime_departure
                    arrivals[1].gbtt_departure = departures[1].gbtt_departure

                    # Append the arrivals to the combined board
                    self._combined_board.append(arrivals[1])

                    # Remove the old values from the arrival and departure boards
                    arrival_board.remove(arrivals)
                    departure_board.remove(departures)

                    break

        # Append the remaining values to the combined board
        for arrival in arrival_board:
            self._combined_board.append(arrival[1])

        for departure in departure_board:
            self._combined_board.append(departure[1])

        # Clear the old boards
        arrival_board.clear()
        departure_board.clear()

    # Get the times (the sort by) out of the combined_board
    def __extract_times(self) -> None:
        temp_board = []  # Create a temporary board

        # Iterate over each item in the board
        for item in self._combined_board:
            # If a gbtt_departure
            # print(item, item.gbtt_departure, item.gbtt_arrival)
            if item.gbtt_departure == "":
                # Append the arrival time and details to the new board
                temp_board.append([item.gbtt_arrival, item])

            else:
                # Append the departure time and details to the new board
                temp_board.append([item.gbtt_departure, item])

        # Overwrite the combined board
        self._combined_board = temp_board

    # Create the new board
    def _create_station_board(self, rows: int = None) -> list:
        self.__extract_times()  # Extract the times

        # Perform a merge sort on the combined board and return it
        combined_board = merge_sort(self._combined_board)
        self._combined_board.clear()  # Clear the combined board

        count = 0  # Set count to 0

        # Append each service to the combined board, until rows is reached
        for service in combined_board:
            self._combined_board.append(service[1])

            count += 1
            if count == rows:
                break

        # Return the combined board
        return self._combined_board

    # Output the board in a formatted way
    def _output_formatted_board(self) -> str:
        out_board = []  # Create a new empty output board

        # For each service in the board, add its content to the output board
        for service in self._combined_board:
            out_board.append(
                [
                    service.gbtt_arrival,
                    service.gbtt_departure,
                    service.terminus,
                    service.origin,
                    service.platform,
                    service.realtime_arrival,
                    service.realtime_departure,
                    service.service_uid,
                ]
            )

        # Print the station info
        print(
            f"Station board for {self._requested_location}. Generated at {datetime.now().strftime("%H:%M:%S on %d/%m/%y")}."
        )
        # Print the table
        print(
            tabulate(
                out_board,
                tablefmt="rounded_grid",
                headers=[
                    "Booked Arrival",
                    "Booked Departure",
                    "Destination",
                    "Origin",
                    "Platform",
                    "Actual Arrival",
                    "Actual Departure",
                    "Service UID",
                ],
            )
        )

        return "200: Station board printed successfully."


# Class for creating the details for the boards
class CreateBoardDetails:
    # Create the departures service info
    def _create_dep_service(self, service) -> tuple:
        location_detail = service["locationDetail"]  # Details of the location
        status = location_detail["displayAs"]  # Status of service

        # Check if booked departure is in location detail
        if "gbttBookedDeparture" in location_detail:
            gbtt_departure = location_detail["gbttBookedDeparture"]

        else:
            gbtt_departure = ""

        # Check if platform is in location detail
        if "platform" in location_detail:
            platform = location_detail["platform"]

        else:
            platform = "-"

        # Check if realtime departure is in location detail
        if "realtimeDeparture" in location_detail:
            realtime_departure = location_detail["realtimeDeparture"]

        else:
            realtime_departure = "-"

        # Check if service UID is in location detail
        if "serviceUid" in service:
            service_uid = service["serviceUid"]

        else:
            service_uid = "-"

        # Check if the status isn't cancelled
        if status != "CANCELLED_CALL":
            # If the gbtt departure and realtime departure are equal, set realtime departure to On Time
            if gbtt_departure == realtime_departure:
                realtime_departure = "On time"

            # If the realtime departure isn't null, format and add Exp
            elif realtime_departure != "-":
                realtime_departure = f"Exp {format_time(realtime_departure)}"

        else:
            # Set the realtime departure to cancelled
            realtime_departure = "Cancelled"

        # Format the gbtt departure
        gbtt_departure = format_time(gbtt_departure)

        # Pop the terminus
        terminus = location_detail["destination"].pop()["description"]

        # Pop the origin
        origin = location_detail["origin"].pop()["description"]

        # Return the service UID and Departure Board
        return service_uid, StationBoardDetails(
            "",
            gbtt_departure,
            terminus,
            origin,
            platform,
            "",
            realtime_departure,
            service_uid,
        )

    # Create the arrivals service info
    def _create_arr_service(self, service) -> tuple:
        location_detail = service["locationDetail"]  # Details of the location
        status = location_detail["displayAs"]  # Status of service

        # Check if booked arrival is in location detail
        if "gbttBookedArrival" in location_detail:
            gbtt_arrival = location_detail["gbttBookedArrival"]

        else:
            gbtt_arrival = "-"

        # Check if platform is in location detail
        if "platform" in location_detail:
            platform = location_detail["platform"]

        else:
            platform = "-"

        # Check if realtime arrival is in location detail
        if "realtimeArrival" in location_detail:
            realtime_arrival = location_detail["realtimeArrival"]

        else:
            realtime_arrival = "-"

        # Check if service UID is in location detail
        if "serviceUid" in service:
            service_uid = service["serviceUid"]

        else:
            service_uid = "-"

        # Check if the status isn't cancelled
        if status != "CANCELLED_CALL":
            # If the gbtt arrival and realtime arrival are equal, set realtime arrival to On Time
            if gbtt_arrival == realtime_arrival:
                realtime_arrival = "On time"

            # If the realtime arrival isn't null, format and add Exp
            elif realtime_arrival != "-":
                realtime_arrival = f"Exp {format_time(realtime_arrival)}"

        else:
            # Set the realtime arrival to cancelled
            realtime_arrival = "Cancelled"

        # Format the gbtt arrival
        gbtt_arrival = format_time(gbtt_arrival)

        # Pop the terminus
        terminus = (location_detail["destination"]).pop()["description"]

        # Pop the origin
        origin = (location_detail["origin"]).pop()["description"]

        # Return the service UID and Arrival Board
        return service_uid, StationBoardDetails(
            gbtt_arrival,
            "",
            terminus,
            origin,
            platform,
            realtime_arrival,
            "",
            service_uid,
        )
