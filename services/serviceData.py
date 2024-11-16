from datetime import datetime

import requests


class ServiceDetails():
    def __init__(self, username: str = None, password: str = None):
        self.__username = username
        self.__password = password

        self._service_url: str = "https://api.rtt.io/v1/json/service/"


    def _get_service_details(self, service_uid: str, time: str = datetime.now().strftime("/%d/%m/%Y")):
        search_query = str(self._service_url) + str(service_uid) + str(time)
        api_response =  requests.get(search_query, auth=(self.__username, self.__password))

        if api_response.status_code == 200:
            service_data = api_response.json()



        else:
            raise ConnectionRefusedError("Failed to connect to the RTT API server. Status code:", api_response.status_code)

    def __filter_by_calling_point(self, filter_items: list, filter: str):
        if filter == None:
            raise ValueError("No filter was provided. Provide a filter.")

        else:
            pass ## Search through calling points for filter 


#sys = ServiceDetails()
#print(sys._get_service_details("G10101"))