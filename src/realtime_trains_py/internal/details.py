### Service Details ###

# Service data class
class ServiceData:
    def __init__(self, train_id, service_uid, operator, origin, destination, calling_points, start_time, end_time, power, train_class) -> None:
        self.train_id = train_id
        self.service_uid = service_uid
        self.operator = operator
        self.origin = origin
        self.destination = destination
        self.calling_points = calling_points
        self.start_time = start_time
        self.end_time = end_time
        self.power = power
        self.train_class = train_class

# Calling point data class
class CallingPoint:
    def __init__(self, stop_name, booked_arrival, realtime_arrival, platform, line, booked_departure, realtime_departure) -> None:
        self.stop_name = stop_name
        self.booked_arrival = booked_arrival
        self.realtime_arrival = realtime_arrival
        self.platform = platform
        self.line = line
        self.booked_departure = booked_departure
        self.realtime_departure = realtime_departure


### Board Details ###

# Station Board Details class
class StationBoardDetails:
    def __init__(self, gbtt_arrival, gbtt_departure, terminus, origin, platform, realtime_arrival, realtime_departure, service_uid) -> None:
        self.gbtt_arrival = gbtt_arrival
        self.gbtt_departure = gbtt_departure
        self.terminus = terminus
        self.origin = origin
        self.platform = platform
        self.realtime_arrival = realtime_arrival
        self.realtime_departure = realtime_departure
        self.service_uid = service_uid

# Departure Board Details class
class DepartureBoardDetails:
    def __init__(self, gbtt_departure, terminus, platform, realtime_departure, service_uid) -> None:
        self.gbtt_departure = gbtt_departure
        self.terminus = terminus
        self.platform = platform
        self.realtime_departure = realtime_departure
        self.service_uid = service_uid

# Arrivals Board Details class
class ArrivalBoardDetails:
    def __init__(self, gbtt_arrival, terminus, origin, platform, realtime_arrival, service_uid) -> None:
        self.gbtt_arrival = gbtt_arrival
        self.terminus = terminus
        self.origin = origin
        self.platform = platform
        self.realtime_arrival = realtime_arrival
        self.service_uid = service_uid