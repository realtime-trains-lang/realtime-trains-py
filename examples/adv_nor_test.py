from realtime_trains_py import RealtimeTrainsPy

rtt = RealtimeTrainsPy(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    complexity="a.n"
)

# Query for getting the next 5 arrivals at Norwich
arrivals_at_norwich = rtt.get_arrivals(tiploc="NRCH", rows=5)

for arrivals in arrivals_at_norwich:
    print(f"{arrivals.service_uid} | {arrivals.gbtt_arrival} | {arrivals.origin} to {arrivals.terminus}")

### OUTPUT ###
# W21663 | 21:11 | Liverpool Lime Street to Norwich
# G27466 | 21:19 | London Liverpool Street to Norwich
# G28572 | 21:32 | Lowestoft to Norwich
# G27187 | 21:36 | Cambridge to Norwich
# G27471 | 21:49 | London Liverpool Street to Norwich