from dotenv import load_dotenv

import os


class AuthenticationDetails():
    def __init__(self) -> None:
        load_dotenv()

        self._username = os.getenv('api_username')
        self._password = os.getenv('api_password')

    ## Used for error checking only    
    def __get_details(self) -> tuple:
        return self._username, self._password