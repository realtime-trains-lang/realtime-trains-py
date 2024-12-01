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

def get_time_delta(delta: int) -> str:
    date_delta = str(datetime.now() + timedelta(delta)).split("-")
    date_delta[2] = (str(date_delta[2]).split(" "))[0]

    return date_delta

def format_time(time: str) -> str:
    new_time = time[0] + time[1] + ":" + time[2] + time[3]
    return new_time

def reformat_time(time: str) -> str:
    time_data: str = ""
    time = time.split(":")
    for i in range(0, 2):
        time_data += (time[i])

    #print(time_data)

    return time_data

def merge_sort(array: list) -> list:
    if len(array) <= 1:
        return array
    
    midpoint = len(array) // 2
    left_half = array[:midpoint]
    right_half = array[midpoint:]

    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)

    return merge(left_half, right_half)

def merge(left: list, right: list) -> list:
    merged_list = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index][0] < right[right_index][0]:
            merged_list.append(left[left_index])
            left_index += 1
        else:
            merged_list.append(right[right_index])
            right_index += 1

    merged_list.extend(left[left_index:])
    merged_list.extend(right[right_index:])

    return merged_list

def remove_dupes(data: list) -> list:
    unique_rows = list(set(tuple(row) for row in data))

    return [list(row) for row in unique_rows]