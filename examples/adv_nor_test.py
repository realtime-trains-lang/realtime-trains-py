from realtime_trains_py import RealtimeTrainsPy

# Initialise RealtimeTrainsPy
rtt = RealtimeTrainsPy(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    complexity="a.n"
)

#### EXAMPLE 1 ####

# Query for getting the next 5 arrivals at Norwich
arrivals_at_norwich = rtt.get_arrivals(tiploc="NRCH", rows=5)

for arrivals in arrivals_at_norwich:
    print(f"{arrivals.service_uid} | {arrivals.gbtt_arrival} | {arrivals.origin} to {arrivals.terminus}")

### EXAMPLE OUTPUT ###
# W21663 | 21:11 | Liverpool Lime Street to Norwich
# G27466 | 21:19 | London Liverpool Street to Norwich
# G28572 | 21:32 | Lowestoft to Norwich
# G27187 | 21:36 | Cambridge to Norwich
# G27471 | 21:49 | London Liverpool Street to Norwich

#### EXAMPLE 2 ####

# Query for getting the next 10 departures from Hull around 10:00 UTC on 10th January 2025
departures_at_hull = rtt.get_departures(tiploc="HULL", date="2025/01/10", time="1000", rows=15)

for departures in departures_at_hull:
    print(f"{departures.service_uid} | {departures.gbtt_departure} | {departures.origin} to {departures.terminus}")

### EXAMPLE OUTPUT ###
# G31323 | 09:47 | Hull to York
# W47587 | 09:50 | Hull to Doncaster
# W50814 | 09:59 | Hull to Bridlington
# P12814 | 10:03 | Hull to Liverpool Lime Street
# W48977 | 10:15 | Hull to Halifax
# W46501 | 10:21 | Hull to Scarborough
# W46193 | 10:23 | Hull to Sheffield
# N35979 | 10:34 | Hull to London Kings Cross
# W49960 | 10:47 | Hull to York
# W47603 | 10:50 | Hull to Doncaster