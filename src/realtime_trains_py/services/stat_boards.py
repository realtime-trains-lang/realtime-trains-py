from datetime import time

# Import functions from utilities
try:
    from realtime_trains_py.services.merge_sort import merge_sort
    from realtime_trains_py.services.utilities import format_time
except:
    from services.merge_sort import merge_sort
    from services.utilities import format_time

# CLass for Station Board
class StationBoardDetails():
    def __init__(self, gbtt_arrival, gbtt_departure, terminus, origin, platform, realtime_arrival, realtime_departure, service_uid) -> None:
        self.gbtt_arrival = gbtt_arrival
        self.gbtt_departure = gbtt_departure
        self.terminus = terminus
        self.origin = origin
        self.platform = platform
        self.realtime_arrival = realtime_arrival
        self.realtime_departure = realtime_departure
        self.service_uid = service_uid

class NewStationBoard():
    def __init__(self, departure_data, arrival_data) -> None:
        # Create new boards
        arrival_board = []
        departure_board = []
        self.combined_board = []

        # Create a new Station Board Creator
        board_creator = CreateBoardDetails()
        # Iterate over each service and append it to the departure board
        for dep_service in departure_data["services"]:
            departure_board.append(board_creator._create_dep_service(dep_service))

        # Iterate over each service and append it to the arrival board
        for arr_service in arrival_data["services"]:
            arrival_board.append(board_creator._create_arr_service(arr_service))

        # Iterate over each att in departures
        for departures in departure_board:
            # Iterate over each att in arrivals
            for arrivals in arrival_board:
                # If the values at position 0 are equal, append it to the combined board
                if departures[0] == arrivals[0]:
                    arrivals[1].realtime_departure = departures[1].realtime_departure
                    arrivals[1].gbtt_departure = departures[1].gbtt_departure
                    self.combined_board.append(arrivals[1])
                    # print(arrivals[1].gbtt_arrival,
                    #       arrivals[1].gbtt_departure,
                    #       arrivals[1].terminus,
                    #       arrivals[1].origin,
                    #       arrivals[1].platform,
                    #       arrivals[1].realtime_arrival,
                    #       arrivals[1].realtime_departure,
                    #       arrivals[1].service_uid)
                    break
        
        # Append the remaining values to the combined board
        for arrival in arrival_board:
            self.combined_board.append(arrival[1])

        # Append the remaining values to the combined board
        for departure in departure_board:
            self.combined_board.append(departure[1]) 

        # Clear the old boards
        arrival_board.clear()
        departure_board.clear()

    def __extract_times(self) -> None:
        # Create a temporary new board
        new_board = []

        # Iterate over each item in the board
        for item in self.combined_board:  
            # If a gbtt_departure       
            print(item, item.gbtt_departure, item.gbtt_arrival)    
            if item.gbtt_departure == "":
                d = item.gbtt_arrival
                new_board.append([d, item])

            else:
                a = item.gbtt_departure
                new_board.append([a, item])

        self.combined_board = new_board

    def _create_station_board(self) -> list:
        self.__extract_times()

        return merge_sort(self.combined_board)

class CreateBoardDetails():
    def _create_dep_service(self, service) -> tuple:
        location_detail = service["locationDetail"] # Details of the location
        status = location_detail["displayAs"] # Status of service

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
        terminus = (location_detail["destination"]).pop()["description"]

        # Return the service UID and Departure Board 
        return service_uid, StationBoardDetails("", gbtt_departure, terminus, "", platform, "", realtime_departure, service_uid)

    def _create_arr_service(self, service) -> tuple:
        location_detail = service["locationDetail"] # Details of the location
        status = location_detail["displayAs"] # Status of service

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
        return service_uid, StationBoardDetails(gbtt_arrival, "", terminus, origin, platform, realtime_arrival, "", service_uid)
