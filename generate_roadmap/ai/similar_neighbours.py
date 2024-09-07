def bandwidth(n):
  if n >= 1.750 and n <= 1.850:
    return True
  else: return False

def similar_neighbours(arr):
  if(len(arr) < 3):
    # arr.sort()
    # return arr[len(arr)-1]
    return -1
  
  if(all(x == arr[0] for x in arr)):
    return arr[0]
  
  for i in range(2, len(arr)):
    if (bandwidth(arr[i-2]) == bandwidth(arr[i-1]) == bandwidth(arr[i]) == True):
      return max(arr[i-2], arr[i-1], arr[i])
  
  return -1