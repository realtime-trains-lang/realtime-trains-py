from realtime_trains_py import RealtimeTrainsPy

# Initialise RealtimeTrainsPy
rtt = RealtimeTrainsPy(
    username="YOUR_USERNAME", # <----- CHANGE ME
    password="YOUR_PASSWORD", # <----- CHANGE ME
    complexity="c"
)

#### EXAMPLE 1 ####

# Query for getting the arrivals at Norwich
rtt.get_arrivals(tiploc="NRCH")

# Running this will create a new file called NRCH_on_yyyy.mm.dd_arr_board.json

# NOTE - If you provide a rows field in get_arrivals, get_station
# or get_departures when using complex mode, it will be ignored



#### EXAMPLE 2 ####

# Query for getting the next 10 departures from Hull around 10:00 UTC on 10th January 2025
rtt.get_departures(tiploc="HULL", date="2025/01/10", time="1000")

# Running this will create a new file called HULL_on_2025.01.10_dep_board.json

# NOTE - If you provide a rows field in get_arrivals, get_station 
# or get_departures when using complex mode, it will be ignored



#### EXAMPLE 3 ####

# Query for getting the details of the service with service_uid "W47587" 
rtt.get_service("W47587")

# Running this will create a new file called W47587_on_yyyy.mm.dd_service_data.json
