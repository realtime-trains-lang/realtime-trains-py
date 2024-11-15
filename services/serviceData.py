from authentication.getAuthDetails import AuthenticationDetails
from datetime import datetime

import requests


class ServiceData():
    def __init__(self):
        details = AuthenticationDetails()
        auth_details = details._get_details()
        self.__password = auth_details[0]
        self.__username = auth_details[1]

    def _get_service_details(self, service_uid: str, time_now = datetime.now().strftime("%d/%m/%Y")):
        pass

    def _filter_by_calling_point(self, filter):
        pass
