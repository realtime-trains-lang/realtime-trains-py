# Import necessary items from other files
from realtime_trains_py.internal.boards import Boards
from realtime_trains_py.internal.live_board import LiveBoard
from realtime_trains_py.internal.services import ServiceDetails, ServiceData, ServiceDetails
from realtime_trains_py.internal.utilities import connection_authorised


class RealtimeTrainsPy:
    def __init__(self, complexity: str="s", username: str=None, password: str=None) -> None:
        """
        :param str username: (Required) A string representing your username for authentication.
        :param str password: (Required) A string representing your password for authentication.
        :param str complexity: (Optional) A string representing your chosen complexity level. 
        Choose from: `["a", "a.n", "a.p", "c", "s","s.n", "s.p"]`. If not provided, defaults to "s".
        
        ## Examples
        ```python
        rtt = RealtimeTrainsPy(complexity="s", username="<a_username>", password="<a_password>")

        rtt = RealtimeTrainsPy(complexity="a.n", username="<a_username>", password="<a_password>")
        ```
        """
        if username == None or password == None:
            raise ValueError("400: Missing authentication details. Both username and password must be provided. Not all required fields were provided.")

        if not connection_authorised(username=username, password=password):
            raise PermissionError("401: Couldn't verify your username or password. Check your details and try again.")

        if complexity.lower() not in ["a", "a.n", "a.p", "c", "s","s.n", "s.p"]:
            raise ValueError("400: Complexity not recognised. Select a valid type.")

        self.__services = ServiceDetails(username=username, password=password, complexity=complexity.lower())
        self.__boards = Boards(username=username, password=password, complexity=complexity.lower())
        self.__live_board = LiveBoard(username=username, password=password)

    def get_departures(self, tiploc: str, filter: str=None, date: str=None, rows: int=None, time: str=None) -> list | str:
        """
        ## Get Departures
        This function retrieves the departures for a given station.

        :param str tiploc: (Required) A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the station.
        :param str filter: (Optional) A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the filter station.
        :param str date: (Optional) A string representing the date in the format YYYY/MM/DD.
        :param int rows: (Optional) An integer representing the maximum number of rows to return. (Only available for simple and advanced complexity.)
        :param str time: (Optional) A string representing the time in the format HHMM.

        ## Examples
        ```python
        get_departures(tiploc="KNGX", filter="STEVNGE", date="2024/11/16", time="1800", rows=10)

        get_departures(tiploc="YORK", date="2024/11/16", time="1800")
        ```
        """
        return self.__boards._get_dep_board_details(tiploc=tiploc.upper(), search_filter=filter, date=date, rows=rows, time=time)

    def get_arrivals(self, tiploc: str, filter: str=None, date: str=None, rows: int=None, time: str=None) -> list | str:
        """
        ## Get Arrivals
        This function retrieves the arrivals for a given station.

        :param str tiploc: (Required) A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the station.
        :param str filter: (Optional) A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the filter station.
        :param str date: (Optional) A string representing the date in the format YYYY/MM/DD.
        :param int rows: (Optional) An integer representing the maximum number of rows to return. (Only available for simple and advanced complexity.)
        :param str time: (Optional) A string representing the time in the format HHMM.

        ## Examples
        ```python
        get_arrivals(tiploc="KNGX", filter="STEVNGE", date="2024/11/16", time="1800", rows=10)

        get_arrivals(tiploc="YORK", date="2024/11/16", time="1800")
        ```
        """
        return self.__boards._get_arr_board_details(tiploc=tiploc.upper(), search_filter=filter, date=date, rows=rows, time=time)

    def get_service(self, service_uid: str, date: str=None) -> ServiceData | str:
        """
        ## Get Service
        This function retrieves the service information for a given service UID on a provided date.

        :param str service_uid: (Required) A string representing the Service Unique Identity (UID) code.
        :param str date: (Optional) A string representing the date in the format YYYY/MM/DD.

        ## Examples
        ```python
        get_service(service_uid="G54071", date="2024/11/16")

        get_service(service_uid="G26171")
        ```
        """
        return self.__services._get_service_details(service_uid=service_uid.upper(), date=date)

    def get_station(self, tiploc: str, filter: str=None, date: str=None, rows: int=None, time: str=None) -> list | str:
        """
        ## Get Station
        This function retrieves the departures and arrivals for a given station and orders these into one big board.

        :param str tiploc: (Required) A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the station.
        :param str filter: (Optional) A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the filter station.
        :param str date: (Optional) A string representing the date in the format YYYY/MM/DD.
        :param int rows: (Optional) An integer representing half of the maximum number of rows to return. See below for more details.
        :param str time: (Optional) A string representing the time in the format HHMM.

        ### Rows
        Rows is the maximum number of rows to return. The API may return twice the number of rows requested, so if you want 10 rows, 
        you should set rows to 5. This is because the API returns both departures and arrivals. 
        
        If you set rows to 10, the API will return up to 10 departures and 10 arrivals. These are then sorted and combined into a single list, so you may
        not actually receive 20 rows of data.

        ---
        ## Examples
        ```python
        get_station(tiploc="STEVNGE", filter="KNGX", date="2024/11/16", time="1800", rows=10)

        get_station(tiploc="YORK", date="2024/11/16", time="1800")
        ```
        """
        return self.__boards._get_stat_board_details(tiploc=tiploc.upper(), search_filter=filter, date=date, rows=rows, time=time)

    def get_live(self, tiploc: str) -> None:
        """
        ## Get Live
        This function retrieves the live departure board for a given station. The board is updated every 60 seconds, on the minute.
        To exit the board, press Ctrl + C.

        :param str tiploc: (Required) A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the station.

        ## Examples
        ```python
        get_live(tiploc="ELYY") # Live board for Ely

        get_live(tiploc="PBRO") # Live board for Peterborough
        ```
        """
        self.__live_board._get_live(tiploc=tiploc.upper())