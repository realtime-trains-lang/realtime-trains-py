from datetime import datetime, timedelta 

months: list = ["31", "28", "31", "30", "31", "30", "31", "31", "30", "31", "30", "31"]

def validate_date(date: str) -> bool:
    first_valid_date = get_time_delta(-8)
    last_valid_date = get_time_delta(81)

    date_items: list = date.split("/")
    month = date_items[1]
    if month > "12":
        return False
    
    elif months[int(month)-1] < date_items[2]:
        return False
    


    #print(date_items)
    ## [29, 11, 2024]
    
    for i in range(0, 3):
        ## 
        if first_valid_date[i] < date_items[i]:

            validation = True
            break
        else:
            validation = False

    if validation == True:
        for i in range(0, 3):
            if last_valid_date[i] > date_items[i]:
                validation = True
                break
            else:
                validation = False
    
    return validation


def get_time_delta(delta: int) -> str:
    date_delta = str(datetime.now() + timedelta(delta)).split("-")
    date_delta[2] = (str(date_delta[2]).split(" "))[0]

    return date_delta


def validate_time(time: str) -> bool:
    time_data: list = []
    if len(time) != 4:
        return False
    
    else:
        for i in range(0, 4):
            time_data.append(int(time[i])) 

        if time_data[0] in range(-1, 2):
            if time_data[1] in range(-1, 10):
                if time_data[2] in range(-1, 6):
                    if time_data[3] in range(-1, 10):
                        return True
                
                    else:
                        return False
                else:
                    return False
            else:
                return False
            
        elif time_data[0] == 2:
            if time_data[1] in range(-1, 4):
                if time_data[2] in range(-1, 6):
                    if time_data[3] in range(-1, 10):
                        return True
                
                    else:
                        return False
                else:
                    return False
            else:
                return False
            
        else:
            return False
        

def format_time(time: str):
    new_time = time[0] + time[1] + ":" + time[2] + time[3]
    return new_time