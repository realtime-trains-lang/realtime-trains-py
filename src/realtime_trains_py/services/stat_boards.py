# Import functions from utilities
try:
    from realtime_trains_py.services.utilities import create_file, format_time, validate_date, validate_time
except:
    from services.utilities import create_file, format_time, validate_date, validate_time

# CLass for Station Board
class StationBoard():
    def __init__(self, gbtt_arrival, terminus, origin, platform, realtime_arrival, service_uid):
        self.gbtt_arrival = gbtt_arrival
        self.terminus = terminus
        self.origin = origin
        self.platform = platform
        self.realtime_arrival = realtime_arrival
        self.service_uid = service_uid

class AdvancedStationBoard():
    def __init__(self, departure_data, arrival_data):
        # Create new boards
        arrival_board = []
        departure_board = []
        self.combined_board = []

        # Iterate over each service and append it to the departure board
        for dep_service in departure_data["services"]:
            departure_board.append(self.__create_dep_adv_service(dep_service))

        # Iterate over each service and append it to the arrival board
        for arr_service in arrival_data["services"]:
            arrival_board.append(self.__create_arr_adv_service(arr_service))

        # Iterate over each att in departures
        for departures in departure_board:
            # Iterate over each att in arrivals
            for arrivals in arrival_board:
                # If the values at position 0 are equal, append it to the combined board
                if departures[0] == arrivals[0]:
                    self.combined_board.append(arrivals[1])
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

    def _create_station_board(self):
        pass

    def __create_dep_adv_service(self, service):
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
            
            # Format the gbtt departure
            gbtt_departure = format_time(gbtt_departure)

        else:
            # Set the realtime departure to cancelled
            realtime_departure = "Cancelled"
            # Format the gbtt departure
            gbtt_departure = format_time(gbtt_departure)

        
        # Pop the terminus
        terminus = (location_detail["destination"]).pop()["description"]

        # Return the service UID and Departure Board 
        return service_uid, StationBoard(gbtt_departure, terminus, "", platform, realtime_departure, service_uid)

    def __create_arr_adv_service(self, service):
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
                realtime_arrival = "Exp " + format_time(realtime_arrival)
            
            # Format the gbtt arrival
            gbtt_arrival = format_time(gbtt_arrival)

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
        return service_uid, StationBoard(gbtt_arrival, terminus, origin, platform, realtime_arrival, service_uid)


class SimpleStationBoard():
    def __create_dep_sim_service(self, service):
        pass

    def __create_arr_sim_service(self, service):
        pass