from authentication.getAuthDetails import AuthenticationDetails
## board needed
from services.serviceData import ServiceDetails


class Main():
    def __init__(self):
        self.__auth_details = AuthenticationDetails()
        self.__service_details = ServiceDetails(username = self.__auth_details._username, password = self.__auth_details._password)

    def _get_departures_at(self, tiploc, rows=None) -> list:
        pass


sys = Main()