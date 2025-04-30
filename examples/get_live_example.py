from realtime_trains_py import RealtimeTrainsPy

# Initialise RealtimeTrainsPy
rtt = RealtimeTrainsPy(
    username="YOUR_USERNAME", # <----- CHANGE ME
    password="YOUR_PASSWORD", # <----- CHANGE ME
    complexity="a.n"
)

#### EXAMPLE 1 ####

rtt.get_live("ELYY") # Get live departure board for Ely

### EXAMPLE OUTPUT ###
# Ely Live:
# 1st 22:17 Norwich Plat 1    Exp 22:49
# Calling at: Thetford, Attleborough, Wymondham & Norwich. Operated by East Midlands Railway.
# 2nd 22:18 London Kings Cross Plat 2    Exp 22:38
# 3rd 22:26 Colchester Plat 2    Exp 22:28
#          22:11:12


#### EXAMPLE 2 ####

rtt.get_live("KNGX") # Get live departure board for London Kings Cross

### EXAMPLE OUTPUT ###
# London Kings Cross Live:
# 1st 22:27 Cambridge Plat 9  On time
# Calling at: Finsbury Park, Alexandra Palace, Potters Bar, Hatfield, Welwyn Garden City, Welwyn North, Knebworth, Stevenage, Hitchin, Letchworth, Baldock, Ashwell & Morden, Royston, Meldreth, Shepreth, Foxton & Cambridge. Operated by Great Northern.
# 2nd 22:39 Kings Lynn Plat 10  On time
# 3rd 23:00 York Plat 6  On time
#          22:11:49


#### EXAMPLE 3 ####

rtt.get_live("LEEDS") # Get live departure board for Leeds

### EXAMPLE OUTPUT ###
# Leeds Live:
# 1st 21:31 York Plat 11D    Exp 22:19
# Calling at: Garforth, Church Fenton & York. Operated by Northern.
# 2nd 22:14 Darlington Plat 15    Exp 22:18
# 3rd 22:15 Manchester Piccadilly Plat 8  On time
#          22:12:19