'''
Write a script that creates 25 random numbers and inserts into an array then finds the largest number
'''
import  numpy as np
from numpy import random

arr = np.array([])
for x in range(25):
    y = random.randint(0,100)
    arr = np.append(arr, y)
arr = np.sort(arr)

print(arr)

print(arr[len(arr)-1])