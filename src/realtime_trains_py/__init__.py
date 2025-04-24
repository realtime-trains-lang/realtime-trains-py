# Import functions from other files
from realtime_trains_py.internal.boards import Boards
from realtime_trains_py.internal.services import ServiceDetailsAdvanced, ServiceDetailsSimple, ServiceDetails
from realtime_trains_py.internal.utilities import connection_authorised


# The RealtimeTrainsPy class
class RealtimeTrainsPy:
    # Initialise the class
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
        # Check if the username and password have been provided
        if username == None or password == None:
            # If at least one is missing, raise an error
            raise ValueError("400: Missing authentication details. Both username and password must be provided. Not all required fields were provided.")

        # Check if the connection is authorised
        if not connection_authorised(username=username, password=password):
            # If not authorised, raise an error
            raise PermissionError("401: Couldn't verify your username or password. Check your details and try again.")

        # Check if selected complexity is valid
        if complexity.lower() not in ["a", "a.n", "a.p", "c", "s","s.n", "s.p"]:
            # If complexity is not in the valid range, raise an error
            raise ValueError("400: Complexity not recognised. Select a valid type.")

        self.__services = ServiceDetails(username=username, password=password, complexity=complexity.lower())

        self.__boards = Boards(username=username, password=password, complexity=complexity.lower())

    # Get the departures for {tiploc}, given {filter} on {date}, at around {time}. Provide up to {rows} rows
    def get_departures(self, tiploc: str, filter: str=None, date: str=None, rows: int=None, time: str=None) -> list | str:
        """
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

    # Get the arrivals for {tiploc}, given {filter} on {date}, at around {time}. Provide up to {rows} rows
    def get_arrivals(self, tiploc: str, filter: str=None, date: str=None, rows: int=None, time: str=None) -> list | str:
        """
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

    # Get the service info for {service_uid} on {date}
    def get_service(self, service_uid: str, date: str=None) -> ServiceDetailsAdvanced | ServiceDetailsSimple | str:
        """
        :param str service_uid: (Required) A string representing the Service Unique Identity (UID) code.
        :param str date: (Optional) A string representing the date in the format YYYY/MM/DD.

        ## Examples
        ```python
        get_service(service_uid="G54071", date="2024/11/16")

        get_service(service_uid="G26171")
        ```
        """
        return self.__services._get_service_details(service_uid=service_uid.upper(), date=date)

    # Get the departures and arrivals for {tiploc}, given {filter} on {date}, at around {time}. Provide up to {rows} rows
    def get_station(self, tiploc: str, filter: str=None, date: str=None, rows: int=None, time: str=None) -> list | str:
        """
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
