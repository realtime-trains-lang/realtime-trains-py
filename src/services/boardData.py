from datetime import datetime, timedelta, date

import requests
import json

class Boards:
    def __init__(self, username: str = None, password: str = None, complexity: str = "s"):
        self.__username = username
        self.__password = password
        self.__complexity = complexity
        self.__date: str = (datetime.now()).strftime("%Y/%m/%d")

        self._board_url: str = "https://api.rtt.io/api/v1/json/search/"

    def _get_board_details(self, tiploc, filter, date: str = None):
        if date is None:
            date = self.__date

        if self.__complexity == "c" or self.__complexity == "c" or self.__validate_time(date):
            search_query = str(self._board_url) + str(tiploc) + "/" + str(date)
            print(search_query)
            api_response =  requests.get(search_query, auth=(self.__username, self.__password))

            if api_response.status_code == 200:
                service_data = api_response.json()

                if self.__complexity == "c":
                    file_name = tiploc + "_board_data.json"

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
