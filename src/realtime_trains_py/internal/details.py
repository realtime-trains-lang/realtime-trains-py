### Service Details ###

# Calling point data class
class CallingPoint:
    def __init__(self, stop_name: str, booked_arrival: str, realtime_arrival: str, platform: str, line: str, booked_departure: str, realtime_departure: str) -> None:
        self.stop_name: str = stop_name
        self.booked_arrival: str = booked_arrival
        self.realtime_arrival: str = realtime_arrival
        self.platform: str = platform
        self.line: str = line
        self.booked_departure: str = booked_departure
        self.realtime_departure: str = realtime_departure



# Service data class
class ServiceData:
    def __init__(self, train_id: str, service_uid: str, operator: str, origin: str, destination: str, calling_points: list[CallingPoint], start_time: str, end_time: str, power: str, train_class: str) -> None:
        self.train_id: str = train_id
        self.service_uid: str = service_uid
        self.operator: str = operator
        self.origin: str = origin
        self.destination: str = destination
        self.calling_points: list[CallingPoint] = calling_points
        self.start_time: str = start_time
        self.end_time: str = end_time
        self.power: str = power
        self.train_class: str = train_class
        


### Board Details ###

# Station Board Details class
class StationBoardDetails:
    def __init__(
            self, 
            scheduled_arrival: str, 
            scheduled_departure: str, 
            terminus: str, 
            origin: str, 
            platform: str, 
            actual_arrival: str | None, 
            actual_departure: str | None, 
            service_uid: str, 
            coaches: int
        ) -> None:
        self.scheduled_arrival: str = scheduled_arrival
        self.scheduled_departure: str = scheduled_departure
        self.terminus: str = terminus
        self.origin: str = origin
        self.platform: str = platform
        self.actual_arrival: str | None = actual_arrival
        self.actual_departure: str | None = actual_departure
        self.service_uid: str = service_uid
        self.coaches: int = coaches



# Default Board class
class DefaultBoard:
    def __init__(self, board: list[StationBoardDetails], location: str) -> None:
        self.board: list[StationBoardDetails] = board
        self.location: str = location