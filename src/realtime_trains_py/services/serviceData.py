from datetime import datetime, timedelta, date

import requests
import json

class Service():
    def __init__():
        pass
        ### Class service for returning services to main

class ServiceDetails():
    def __init__(self, username: str = None, password: str = None, complexity: str = "s"):
        self.__username = username
        self.__password = password
        self.__complexity = complexity
        self.__date: str = (datetime.now()).strftime("%Y/%m/%d")

        self._service_url: str = "https://api.rtt.io/api/v1/json/service/"


    def _get_service_details(self, service_uid: str, date: str = None) -> None | list:
        if date is None:
            date = self.__date

        if self.__complexity == "c" or self.__validate_time(date):
            search_query = str(self._service_url) + str(service_uid) + "/" + str(date)
            print(search_query)
            api_response =  requests.get(search_query, auth=(self.__username, self.__password))

            if api_response.status_code == 200:
                service_data = api_response.json()

                if self.__complexity == "c":
                    file_name = service_uid + "_service_data.json"

                    with open(file_name, 'x', encoding='utf-8') as file:
                        json.dump(service_data, file, ensure_ascii = False, indent = 4)

                
                elif self.__complexity == "a":
                    # data to be returned
                    pass
                
                elif self.__complexity == "s":
                    # data to be returned
                    pass


            elif api_response.status_code == 404:
                raise ValueError("Service UID not recognised. Status code:", api_response.status_code)
            
            elif api_response.status_code == 401 or api_response.status_code == 403:
                raise ValueError("Access blocked: check your credentials. Status code:", api_response.status_code)

            else:
                raise ConnectionRefusedError("Failed to connect to the RTT API server. Try again in a few minutes. Status code:", api_response.status_code)

        else: 
            raise ValueError("Invalid date. Date provided did not meet requirements or fall into the valid date range.")

    def __filter_by_calling_point(self, filter_items: list, filter: str):
        if filter == None:
            raise ValueError("No filter was provided. Provide a filter.")

        else:
            pass ## Search through calling points for filter 

    def __validate_time(self, date: str) -> bool:
        first_valid_date = self.__get_time_delta(-8)
        last_valid_date = self.__get_time_delta(81)

        date_items: list = date.split("/")
        #print(date_items)


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