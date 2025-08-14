### Service Details ###

# Calling point data class
class CallingPoint:
    def __init__(self, stop_name: str, booked_arrival: str, realtime_arrival: str, platform: str, line: str, booked_departure: str, realtime_departure: str) -> None:
        self.realtime_departure: str = realtime_departure
        self.realtime_arrival: str = realtime_arrival
        self.booked_departure: str = booked_departure
        self.booked_arrival: str = booked_arrival
        self.stop_name: str = stop_name
        self.platform: str = platform
        self.line: str = line


# Service data class
class ServiceData:
    def __init__(self, train_id: str, service_uid: str, operator: str, origin: str, destination: str, calling_points: list[CallingPoint], start_time: str, end_time: str, power: str, train_class: str) -> None:
        self.calling_points: list[CallingPoint] = calling_points
        self.destination: str = destination
        self.service_uid: str = service_uid
        self.train_class: str = train_class
        self.start_time: str = start_time
        self.end_time: str = end_time
        self.operator: str = operator
        self.train_id: str = train_id
        self.origin: str = origin
        self.power: str = power
        


### Board Details ###

# Station Board Details class
class StationBoardDetails:
    def __init__(self, gbtt_arrival: str, gbtt_departure: str, terminus: str, origin: str, platform: str, realtime_arrival: str | None, realtime_departure: str | None, service_uid: str) -> None:
        self.realtime_departure: str | None = realtime_departure
        self.realtime_arrival: str | None = realtime_arrival
        self.gbtt_departure: str = gbtt_departure
        self.gbtt_arrival: str = gbtt_arrival
        self.service_uid: str = service_uid
        self.platform: str = platform
        self.terminus: str = terminus
        self.origin: str = origin


# Departure Board Details class
class DepartureBoardDetails:
    def __init__(self, gbtt_departure: str, terminus: str, platform: str, realtime_departure: str | None, service_uid: str) -> None:
        self.realtime_departure: str | None = realtime_departure
        self.gbtt_departure: str = gbtt_departure
        self.service_uid: str = service_uid
        self.platform: str = platform
        self.terminus: str = terminus


# Arrivals Board Details class
class ArrivalBoardDetails:
    def __init__(self, gbtt_arrival: str, terminus: str, origin: str, platform: str, realtime_arrival: str | None, service_uid: str) -> None:
        self.realtime_arrival: str | None = realtime_arrival
        self.service_uid: str = service_uid
        self.gbtt_arrival: str = gbtt_arrival
        self.platform: str = platform
        self.terminus: str = terminus
        self.origin: str = origin


# Default Board class
class DefaultBoard:
    def __init__(self, board: list[ArrivalBoardDetails] | list[DepartureBoardDetails], location: str) -> None:
        self.board: list[ArrivalBoardDetails] | list[DepartureBoardDetails] = board
        self.location: str = location