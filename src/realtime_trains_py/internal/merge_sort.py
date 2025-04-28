# Sort the two lists
def merge_sort(arr) -> list:
    if len(arr) <= 1:
        return arr

    # Sort each half
    sorted_l = merge_sort(arr[:(len(arr)//2)])
    sorted_r = merge_sort(arr[(len(arr)//2) :])

    # Return the sorted array
    return merge(sorted_l, sorted_r)

# Merge the two lists in order
def merge(left, right) -> list:
    result = [] 
    count_l = count_r = 0 

    # While both counts are less than the length of the lists
    while count_l < len(left) and count_r < len(right):
        if left[count_l][0] < right[count_r][0]:
            # If left item is less than right item, append left to the result and increment the left count
            result.append(left[count_l])
            count_l += 1

        else:
            # Append right to the result and increment the right count
            result.append(right[count_r])
            count_r += 1

    # Extend both lists
    result.extend(left[count_l:])
    result.extend(right[count_r:])

    return result