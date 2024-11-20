from services.boardData import Boards
from services.serviceData import Service, ServiceDetails


class RealtimeTrainsPy():
    def __init__(self, complexity = "s", username: str = None, password: str = None) -> None: 
        if username == None and password == None:
            self._username = username
            self.__password = password
        elif (username != None and password == None) or (username == None and password != None):
            raise ValueError("Missing details. Both username and password must be provided. Only one field was provided.")

        else:
            self._username = username
            self.__password = password
            if complexity not in ["s", "a", "c"]:
                raise ValueError("Complexity not recognised. Select a valid type.")
        
        self.__services = ServiceDetails(username = self._username, password = self.__password, complexity = complexity)
        self.__boards = Boards(username = self._username, password = self.__password, complexity = complexity)

    def get_departures(self, tiploc: str, filter: str = None, date: str = None, rows: int = None) -> list:
        self.__boards._get_board_details(tiploc = tiploc, filter = filter, date = date)

    def get_arrivals(self, tiploc: str, filter: str, date: str = None, rows: int = None) -> list:
        pass

    def get_service(self, service_uid: str, date: str = None) -> Service:
        self.__services._get_service_details(service_uid = service_uid, date = date)