from dotenv import load_dotenv

import os


class AuthenticationDetails():
    def __init__(self) -> None:
        load_dotenv()

        self.__username = os.getenv('api_username')
        self.__password = os.getenv('api_password')

    ## Used for error checking only    
    def _get_details(self) -> tuple:
        return self.__username, self.__password