# Import necessary items from other files

from realtime_trains_py.internal.boards import Boards
from realtime_trains_py.internal.details import DefaultBoard
from realtime_trains_py.internal.live_board import LiveBoard
from realtime_trains_py.internal.services import ServiceDetails, ServiceData, ServiceDetails
from realtime_trains_py.internal.utilities import check_token, validate_complexity


class RealtimeTrainsPy:
    def __init__(self, request_token: str, complexity: str="s") -> None:
        """
        :param str request_token: (Required) A string representing your request token for authentication.
        :param str complexity: (Optional) A string representing your chosen complexity level. 
        Choose from: `["a", "a.n", "c", "s","s.n"]`. If not provided, defaults to "s".
        
        ---
        ## Examples
        ```python
        rtt = RealtimeTrainsPy(request_token="<a_request_token>", complexity="s")

        rtt = RealtimeTrainsPy(request_token="<a_request_token>", complexity="a.n")
        ```

        [Check out the wiki](https://github.com/realtime-trains-lang/realtime-trains-py/wiki) for more examples and information.
        """
        complexity = complexity.lower()

        request_token = check_token(request_token=request_token)

        validate_complexity(complexity)

        self.__services = ServiceDetails(request_token=request_token, complexity=complexity)
        self.__boards = Boards(request_token=request_token, complexity=complexity)
        self.__live_board = LiveBoard(request_token=request_token)


    def get_departures(self, tiploc: str, filter_from: str | None=None, filter_to: str | None=None, date: str | None=None, rows: int | None=None, time: str | None=None) -> DefaultBoard | None:
        """
        ## Get Departures
        This function retrieves the departures for a given station.

        :param str tiploc: (Required) A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the station.
        :param str filter_from: (Optional) A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the originating station.
        :param str filter_to: (Optional) A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the destination station.
        :param str date: (Optional) A string representing the date in the format YYYY-MM-DD.
        :param int rows: (Optional) An integer representing the maximum number of rows to return. (Only available for simple and advanced complexity.)
        :param str time: (Optional) A string representing the time in the format HHMM.

        ---
        ## Examples
        ```python
        get_departures(tiploc="KNGX", filter="STEVNGE", date="2024-11-16", time="1800", rows=10)

        get_departures(tiploc="YORK", date="2024-11-16", time="1800")
        ```

        [Check out the wiki](https://github.com/realtime-trains-lang/realtime-trains-py/wiki) for more examples and information.
        """
        return self.__boards._get_dep_board_details(tiploc=tiploc.upper(), filter_from=filter_from, filter_to=filter_to, date=date, rows=rows, time=time)

    def get_service(self, service_uid: str, date: str | None=None) -> ServiceData | None:
        """
        ## Get Service
        This function retrieves the service information for a given service UID on a provided date.

        :param str service_uid: (Required) A string representing the Service Unique Identity (UID) code.
        :param str date: (Optional) A string representing the date in the format YYYY-MM-DD.

        ---
        ## Examples
        ```python
        get_service(service_uid="G54071", date="2024-11-16")

        get_service(service_uid="G26171")
        ```

        [Check out the wiki](https://github.com/realtime-trains-lang/realtime-trains-py/wiki) for more examples and information.
        """
        return self.__services._get_service_details(service_uid=service_uid.upper(), date=date)

    def get_live(self, tiploc: str, mode: str="LCD") -> None:
        """
        ## Get Live
        This function retrieves the live departure board for a given station. The board is updated every 60 seconds, on the minute.
        To exit the board, press Ctrl + C.

        :param str tiploc: (Required) A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the station.

        :param str mode: (Optional) A string representing the mode of the live board. 
        Choose from: `["DMI.Y", "DMI.W", "LCD"]`. If not provided, defaults to "LCD".

        ---
        ## Examples
        ```python
        get_live(tiploc="ELYY") # Live board for Ely

        get_live(tiploc="PBRO", mode="DMI.Y") # Live board for Peterborough, with mode set to DMI (Yellow)
        ```

        [Check out the wiki](https://github.com/realtime-trains-lang/realtime-trains-py/wiki) for more examples and information.
        """       
        self.__live_board._get_live(tiploc=tiploc.upper(), mode=mode.upper())

    def watch_service(self, service_uid: str, mode: str="LCD") -> None:
        """
        ## Watch Service
        This function retrieves the service information for a given service UID on a provided date. The service information is updated every 60 seconds, on the minute. 
        To stop watching the service, press Ctrl + C.

        :param str service_uid: (Required) A string representing the Service Unique Identity (UID) code.
        :param str mode: (Optional) A string representing the mode of the live board. 
        Choose from: `["DMI.Y", "DMI.W", "LCD"]`. If not provided, defaults to "LCD".

        ---
        ## Examples
        ```python
        watch_service(service_uid="G54071", mode="DMI.Y")

        watch_service(service_uid="G26171")
        ```

        [Check out the wiki](https://github.com/realtime-trains-lang/realtime-trains-py/wiki) for more examples and information.
        """
        raise NotImplementedError("This method is not yet implemented.")