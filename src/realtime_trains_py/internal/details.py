### Service Details ###

# Calling point data class
class CallingPoint:
    def __init__(self, stop_name: str, scheduled_arrival: str, expected_arrival: str, platform: str, line: str, scheduled_departure: str, expected_departure: str, coaches: int) -> None:
        self.stop_name: str = stop_name
        self.scheduled_arrival: str = scheduled_arrival
        self.expected_arrival: str = expected_arrival
        self.platform: str = platform
        self.line: str = line
        self.scheduled_departure: str = scheduled_departure
        self.expected_departure: str = expected_departure
        self.coaches: int = coaches



# Service data class
class ServiceData:
    def __init__(self, service_uid: str, operator: str, origin: str, destination: str, calling_points: list[CallingPoint], start_time: str, end_time: str, coaches: int) -> None:
        self.service_uid: str = service_uid
        self.operator: str = operator
        self.origin: str = origin
        self.destination: str = destination
        self.calling_points: list[CallingPoint] = calling_points
        self.start_time: str = start_time
        self.end_time: str = end_time
        self.coaches: int = coaches
        


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
            expected_arrival: str, 
            expected_departure: str, 
            service_uid: str, 
            coaches: int
        ) -> None:
        self.scheduled_arrival: str = scheduled_arrival
        self.scheduled_departure: str = scheduled_departure
        self.terminus: str = terminus
        self.origin: str = origin
        self.platform: str = platform
        self.expected_arrival: str = expected_arrival
        self.expected_departure: str = expected_departure
        self.service_uid: str = service_uid
        self.coaches: int = coaches



# Default Board class
class DefaultBoard:
    def __init__(self, board: list[StationBoardDetails], location: str) -> None:
        self.board: list[StationBoardDetails] = board
        self.location: str = location