from authentication.getAuthDetails import AuthenticationDetails
## board needed
from services.serviceData import ServiceDetails


class RealtimeTrainsPy():
    def __init__(self, username: str = None, password: str = None):
        if username == None and password == None:
            self.__auth_details = AuthenticationDetails()
            self._username = self.__auth_details._username
            self.__password = self.__auth_details._password
        elif (username != None and password == None) or (username == None and password != None):
            raise ValueError("Both username and password must be provided. Only one field was provided.")

        else:
            self._username = username
            self.__password = password
        
        self.__service_details = ServiceDetails(self._username, self.__password )

    def _get_departures(self, tiploc: str, filter: str, time: str = None, rows: int = None) -> list:
        pass

    def _get_arrivals(self, tiploc: str, filter: str, time: str = None, rows: int = None) -> list:
        pass

    def _get_service(self, service_uid: str, time: str = None) -> list:
        pass


sys = RealtimeTrainsPy("anonymous4401", "b")