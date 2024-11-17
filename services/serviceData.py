from datetime import datetime, timedelta, date

import requests

class Service():
    def __init__():
        pass
        ### Class service for returning services to main

class ServiceDetails():
    def __init__(self, username: str = None, password: str = None, complexity: str = "s"):
        self.__username = username
        self.__password = password
        self.__complexity = complexity

        self._service_url: str = "https://api.rtt.io/v1/json/service/"


    def _get_service_details(self, service_uid: str, date: str = datetime.now().strftime("%d/%m/%Y")):
        if self.__validate_time(date):
            search_query = str(self._service_url) + str(service_uid) + "/" + str(date)
            api_response =  requests.get(search_query, auth=(self.__username, self.__password))

            if api_response.status_code == 200:
                service_data = api_response.json()

                ### Data collection and returning based on complexity given


            elif api_response.status_code == 404:
                raise ValueError("Service UID not recognised. \nStatus code:", api_response.status_code)
            
            elif api_response.status_code == 400:
                raise ValueError("Access blocked: check your credentials. \nStatus code:", api_response.status_code)

            else:
                raise ConnectionRefusedError("Failed to connect to the RTT API server. Try again in a few minutes. \nStatus code:", api_response.status_code)

        else: 
            raise ValueError("Date provided did not meet requirements or fall into the valid date range.")

    def __filter_by_calling_point(self, filter_items: list, filter: str):
        if filter == None:
            raise ValueError("No filter was provided. Provide a filter.")

        else:
            pass ## Search through calling points for filter 

    def __validate_time(self, date: str) -> bool:
        first_valid_date = self.__get_time_delta(-8)
        last_valid_date = self.__get_time_delta(81)

        date_items: list = date.split("/")
        date_items = str(date_items[2]), str(date_items[1]), str(date_items[0])
        print(date_items)


        for i in range(0, 3):
            if first_valid_date[i] < date_items[i]:
                validation = True
                break
            else:
                validation = False

        if validation == True:
            for i in range(0, 3):
                if last_valid_date[i] > date_items[i]:
                    validation = True
                    break
                else:
                    validation = False
        
        return validation


    def __get_time_delta(self, delta: int) -> str:
        date_delta = str(datetime.now() + timedelta(delta)).split("-")
        date_delta[2] = (str(date_delta[2]).split(" "))[0]

        return date_delta


#sys = ServiceDetails()

#print(sys.__get_time_delta(7))
#print(sys._get_service_details("G10101"))