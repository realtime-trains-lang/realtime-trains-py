from src.authentication.getAuthDetails import AuthenticationDetails
## board needed
from src.services.serviceData import Service, ServiceDetails


class RealtimeTrainsPy():
    def __init__(self, complexity = "s", username: str = None, password: str = None) -> None: 
        if username == None and password == None:
            self.__auth_details = AuthenticationDetails()
            self._username = self.__auth_details._username
            self.__password = self.__auth_details._password
        elif (username != None and password == None) or (username == None and password != None):
            raise ValueError("Missing details. Both username and password must be provided. Only one field was provided.")

        else:
            self._username = username
            self.__password = password
            if complexity not in ["s", "a", "c"]:
                raise ValueError("Complexity not recognised. Select a valid type.")
        
        self.__services = ServiceDetails(username = self._username, password = self.__password, complexity = complexity)


    def get_departures(self, tiploc: str, filter: str, time: str = None, rows: int = None) -> list:
        pass

    def get_arrivals(self, tiploc: str, filter: str, time: str = None, rows: int = None) -> list:
        pass

    def get_service(self, service_uid: str, date: str = None) -> Service:
        self.__services._get_service_details(service_uid = service_uid, date = date)


sys = RealtimeTrainsPy(complexity = "a", username = "rttapi_anonymous4401", password = "b")