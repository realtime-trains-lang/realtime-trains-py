from datetime import datetime, timedelta
from services.utilities import validate

import requests
import json

class Boards:
    def __init__(self, username: str = None, password: str = None, complexity: str = "s"):
        self.__username = username
        self.__password = password
        self.__complexity = complexity
        self.__date: str = (datetime.now()).strftime("%Y/%m/%d")

        self._board_url: str = "https://api.rtt.io/api/v1/json/search/"

    def _get_dep_board_details(self, tiploc, filter, rows, time, date: str = None):
        if date is None:
            date = self.__date

        if time is None:
            time = (datetime.now()).strftime("%H%M")

        if self.__complexity == "c" or (validate("d", date) and validate("t", time)):
            if filter != None:
                search_query = "/json/search/" + str(tiploc) + "/to/<toStation>" + str(filter)

            else:
                search_query = "https://api.rtt.io/api/v1/json/search/" + str(tiploc) + "/" + str(date)
            #print(search_query)
            api_response =  requests.get(search_query, auth=(self.__username, self.__password))

            if api_response.status_code == 200:
                service_data = api_response.json()

                if self.__complexity == "c":
                    split_date = date.split("/")
                    file_name = "JSONs/" + tiploc + "_on_" + split_date[0] + "." + split_date[1] + "." + split_date[2] + "_arr_board_data.json"

                    with open(file_name, 'x', encoding='utf-8') as file:
                        json.dump(service_data, file, ensure_ascii = False, indent = 4)

                
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
            raise ValueError("Invalid date. Date provided did not meet requirements or fall into the valid date range.")

    def _get_arr_board_details(self, tiploc, filter, rows, time, date: str = None):
        if date is None:
            date = self.__date

        if time is None:
            time = (datetime.now()).strftime("%H%M")

        if self.__complexity == "c" or (validate("d", date) and validate("t", time)):
            if filter != None:
                search_query = "/json/search/" + str(tiploc) + "/to/<toStation>" + str(filter)

            else:
                search_query = "https://api.rtt.io/api/v1/json/search/" + str(tiploc) + "/" + str(date) + "/arrivals"
            #print(search_query)
            api_response =  requests.get(search_query, auth=(self.__username, self.__password))

            if api_response.status_code == 200:
                service_data = api_response.json()

                if self.__complexity == "c":
                    split_date = date.split("/")
                    file_name = "JSONs/" + tiploc + "_on_" + split_date[0] + "." + split_date[1] + "." + split_date[2] + "_arr_board_data.json"

                    with open(file_name, 'x', encoding='utf-8') as file:
                        json.dump(service_data, file, ensure_ascii = False, indent = 4)

                
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
            raise ValueError("Invalid date. Date provided did not meet requirements or fall into the valid date range.")