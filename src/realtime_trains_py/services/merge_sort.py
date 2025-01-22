def merge_sort(arr) -> list:
    # If the length is 1 or less, return the array
    if len(arr) <= 1: return arr
    
    # Get the centre
    centre = len(arr)//2
    # Split into two halves
    left = arr[:centre]
    right = arr[centre:]

    # Sort each half
    sorted_l = merge_sort(left)
    sorted_r = merge_sort(right)

    # Return the sorted array
    return merge(sorted_l, sorted_r)

def merge(left, right) -> list:
    # New result list
    result = []
    # Set counts to 0
    count_l = count_r = 0

    while count_l < len(left) and count_r < len(right):
        if left[count_l] < right[count_r]:
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

if __name__ == "__main__":
    unsortedArr = [
        ["00:15", "obj"],
        ["15:33", "obj"],
        ["10:44", "obj"],
        ["09:50", "obj"]
    ]

    sortedArr = merge_sort(unsortedArr)
    print("Sorted array:", sortedArr)