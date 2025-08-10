from realtime_trains_py import RealtimeTrainsPy

# Initialise RealtimeTrainsPy
rtt = RealtimeTrainsPy(
    username="YOUR_USERNAME", # <----- CHANGE ME
    password="YOUR_PASSWORD", # <----- CHANGE ME
    complexity="a.n"
)

#### EXAMPLE 1 ####

# Query for getting the next 5 arrivals at Norwich
arrivals_at_norwich = rtt.get_arrivals(tiploc="NRCH", rows=5)

for arrivals in arrivals_at_norwich.board:
    print(f"{arrivals.service_uid} | {arrivals.gbtt_arrival} | {arrivals.origin} to {arrivals.terminus}")

### EXAMPLE OUTPUT ###
# W21663 | 21:11 | Liverpool Lime Street to Norwich
# G27466 | 21:19 | London Liverpool Street to Norwich
# G28572 | 21:32 | Lowestoft to Norwich
# G27187 | 21:36 | Cambridge to Norwich
# G27471 | 21:49 | London Liverpool Street to Norwich



#### EXAMPLE 2 ####

# Query for getting the next 10 departures from Hull around 10:00 UTC on 10th January 2025
departures_at_hull = rtt.get_departures(tiploc="HULL", date="2025/01/10", time="1000", rows=10)

for departures in departures_at_hull.board:
    print(f"{departures.service_uid} | {departures.gbtt_departure} | Hull to {departures.terminus}")

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



#### EXAMPLE 3 ####

# Query for getting the details of the service with service_uid "W47587" 
service = rtt.get_service("W47587")

print(f"Service: {service.train_id} ({service.service_uid})\n{service.origin} to {service.destination} \nOperated by {service.operator}")
for calling_point in service.calling_points:
    print(f"Arrive: {calling_point.booked_arrival} Depart: {calling_point.booked_departure} | {calling_point.stop_name} Platform {calling_point.platform}")

### EXAMPLE OUTPUT ###
# Service: 2C56 (W47587)
# Hull to Doncaster
# Operated by Northern
# Arrive:  Depart: 09:50 | Hull Platform 1
# Arrive: 09:57 Depart: 09:57 | Hessle Platform 1
# Arrive: 10:02 Depart: 10:02 | Ferriby Platform 2
# Arrive: 10:06 Depart: 10:07 | Brough Platform 2
# Arrive: 10:14 Depart: 10:14 | Gilberdyke Platform 2
# Arrive: 10:23 Depart: 10:24 | Goole Platform 2
# Arrive: 10:33 Depart: 10:33 | Thorne North Platform 1
# Arrive: 10:39 Depart: 10:40 | Hatfield & Stainforth Platform 1
# Arrive: 10:44 Depart: 10:44 | Kirk Sandall Platform 1
# Arrive: 10:53 Depart:  | Doncaster Platform 1