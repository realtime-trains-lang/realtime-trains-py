# Import functions from other files
try:
    from realtime_trains_py.internal.boards import Boards
    from realtime_trains_py.internal.services import (
        ServiceDetailsAdvanced,
        ServiceDetailsSimple,
        ServiceDetails,
    )
    from realtime_trains_py.internal.utilities import connection_authorised
except:
    from internal.boards import Boards
    from internal.services import (
        ServiceDetailsAdvanced,
        ServiceDetailsSimple,
        ServiceDetails,
    )
    from internal.utilities import connection_authorised


# The RealtimeTrainsPy class
class RealtimeTrainsPy:
    # Initialise the class
    def __init__(
        self, complexity: str = "s", username: str = None, password: str = None
    ) -> None:
        """
        ## Initialize realtime_trains_py.
        ### complexity (optional) [not case-sensitive]
            A string representing the complexity level of the data. The default is "s".

        ### username (required)
            A string representing the username for authentication.

        ### password (required)
            A string representing the password for authentication.

        ## Example
        ```python
        rtt = RealtimeTrainsPy(complexity="s", username="<a_username>", password="<a_password>")
        ```
        """
        # Check if the username and password have been provided
        if username == None or password == None:
            # If at least one is missing, raise an error
            raise ValueError(
                "400: Missing authentication details. Both username and password must be provided. Not all required fields were provided."
            )

        # Check if the connection is authorised
        if not connection_authorised(username=username, password=password):
            # If not authorised, raise an error
            raise PermissionError(
                "401: Couldn't verify your username or password. Check your details and try again."
            )

        # Check if selected complexity is valid
        if complexity.lower() not in ["s", "s.p", "s.n", "a", "a.p", "a.n", "c"]:
            # If complexity is not in the valid range, raise an error
            raise ValueError("400: Complexity not recognised. Select a valid type.")

        self.__services = ServiceDetails(
            username=username, password=password, complexity=complexity.lower()
        )

        self.__boards = Boards(
            username=username, password=password, complexity=complexity.lower()
        )

    # Get the departures for {tiploc}, given {filter} on {date}, at around {time}. Provide up to {rows} rows
    def get_departures(
        self,
        tiploc: str,
        filter: str = None,
        date: str = None,
        rows: int = None,
        time: str = None,
    ) -> list | str:
        """
        ### tiploc (required)

            A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the station.

        ### filter (optional)
            A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the filter station.

        ### date (optional)
            A string representing the date in the format YYYY/MM/DD.

        ### rows (optional)
            An integer representing the maximum number of rows to return. (Only available for simple and advanced complexity.)

        ### time (optional)
            A string representing the time in the format HHMM.

        ### Examples
        ```python
        get_departures(tiploc="KNGX", filter="STEVNGE", date="2024/11/16", time="1800", rows=10)

        get_departures(tiploc="YORK", date="2024/11/16", time="1800")
        ```
        """
        return self.__boards._get_dep_board_details(
            tiploc=tiploc.upper(), search_filter=filter, date=date, rows=rows, time=time
        )

    # Get the arrivals for {tiploc}, given {filter} on {date}, at around {time}. Provide up to {rows} rows
    def get_arrivals(
        self,
        tiploc: str,
        filter: str = None,
        date: str = None,
        rows: int = None,
        time: str = None,
    ) -> list | str:
        """
        ### tiploc (required)

            A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the station.

        ### filter (optional)
            A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the filter station.

        ### date (optional)
            A string representing the date in the format YYYY/MM/DD.

        ### rows (optional)
            An integer representing the maximum number of rows to return. (Only available for simple and advanced complexity.)

        ### time (optional)
            A string representing the time in the format HHMM.

        ### Examples
        ```python
        get_arrivals(tiploc="KNGX", filter="STEVNGE", date="2024/11/16", time="1800", rows=10)

        get_arrivals(tiploc="YORK", date="2024/11/16", time="1800")
        ```
        """
        return self.__boards._get_arr_board_details(
            tiploc=tiploc.upper(), search_filter=filter, date=date, rows=rows, time=time
        )

    # Get the service info for {service_uid} on {date}
    def get_service(
        self, service_uid: str, date: str = None
    ) -> ServiceDetailsAdvanced | ServiceDetailsSimple | str:
        """
        ### service_uid (required)
            A string representing the Service Unique Identity (UID) code.

        ### date (optional)
            A string representing the date in the format YYYY/MM/DD.

        ### Examples
        ```python
        get_service(service_uid="G54071", date="2024/11/16")

        get_service(service_uid="G26171")
        ```
        """
        return self.__services._get_service_details(
            service_uid=service_uid.upper(), date=date
        )

    # Get the departures and arrivals for {tiploc}, given {filter} on {date}, at around {time}. Provide up to {rows} rows
    def get_station(
        self,
        tiploc: str,
        filter: str = None,
        date: str = None,
        rows: int = None,
        time: str = None,  #
    ) -> list | str:
        """
        ### tiploc (required)
            A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the station.

        ### filter (optional)
            A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the filter station.

        ### date (optional)
            A string representing the date in the format YYYY/MM/DD.

        ### rows (optional)
            An integer representing the maximum number of rows to return. (Only available for simple and advanced complexity.)

        ### time (optional)
            A string representing the time in the format HHMM.

        ### Examples
        ```python
        get_station(tiploc="KNGX", filter="STEVNGE", date="2024/11/16", time="1800", rows=10)

        get_station(tiploc="YORK", date="2024/11/16", time="1800")
        ```
        """
        return self.__boards._get_stat_board_details(
            tiploc=tiploc.upper(), search_filter=filter, date=date, rows=rows, time=time
        )
