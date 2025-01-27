# Sort the two lists
def merge_sort(arr) -> list:
    # If the length is 1 or less, return the array
    if len(arr) <= 1: return arr
    
    # Split into two halves
    left = arr[:(len(arr)//2)]
    right = arr[(len(arr)//2):]

    # Sort each half
    sorted_l = merge_sort(left)
    sorted_r = merge_sort(right)

    # Return the sorted array
    return merge(sorted_l, sorted_r)

# Merge the two lists in order
def merge(left, right) -> list:
    # New result list
    result = []
    # Set counts to 0
    count_l = 0
    count_r = 0

    # While both counts are less than the length of the lists
    while count_l < len(left) and count_r < len(right):
        if left[count_l][0] < right[count_r][0]:
            # If left item is less than right item, append left to the result
            result.append(left[count_l])
            # Increment count
            count_l += 1

        else:
            # Append right to the result
            result.append(right[count_r])
            # Increment count
            count_r += 1

    # Extend both lists
    result.extend(left[count_l:])
    result.extend(right[count_r:])

    return result
