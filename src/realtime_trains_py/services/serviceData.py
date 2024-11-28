from datetime import datetime
from services.utilities import validate_time, validate_date, format_time

import json
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
        self.__date: str = (datetime.now()).strftime("%Y/%m/%d")

        self._service_url: str = "https://api.rtt.io/api/v1/json/service/"


    def _get_service_details(self, service_uid: str, date: str | None, time: str | None) -> str | list:
        if date is None:
            date = self.__date

        if time is None:
            time = (datetime.now()).strftime("%H%M")


        if self.__complexity == "c" or (validate_date(time) and validate_time(time)):
            search_query = str(self._service_url) + str(service_uid) + "/" + str(date)
            #print(search_query)
            api_response =  requests.get(search_query, auth=(self.__username, self.__password))

            if api_response.status_code == 200:
                service_data = api_response.json()

                if self.__complexity == "c":
                    split_date = date.split("/")
                    file_name = "JSONs/" + service_uid + "_on_" + split_date[0] + "." + split_date[1] + "." + split_date[2] + "_service_data.json"

                    with open(file_name, 'x', encoding='utf-8') as file:
                        json.dump(service_data, file, ensure_ascii = False, indent = 4)
                        
                        return_info: str = "Service information added to new file: " + file_name

                    print(return_info) 

                
                elif self.__complexity == "a":
                    # data to be returned
                    pass
                
                elif self.__complexity == "s":
                    # data to be returned
                    pass


            elif api_response.status_code == 404:
                raise ValueError("An unexpected error occurred. Status code:", api_response.status_code)
            
            elif api_response.status_code == 401 or api_response.status_code == 403:
                raise ValueError("Access blocked: check your credentials. Status code:", api_response.status_code)

            else:
                raise ConnectionRefusedError("Failed to connect to the RTT API server. Try again in a few minutes. Status code:", api_response.status_code)
        else:
            raise ValueError("Invalid date or time. Date or time provided did not meet requirements or fall into the valid date/time range.")


#sys = ServiceDetails()

#print(sys.__get_time_delta(7))
#print(sys._get_service_details("G10101"))