# py-sorting <http://github.com/gwtw/py-sorting>
# Copyright 2015 Daniel Imms <http://www.growingwiththeweb.com>
# Released under the MIT license <http://github.com/gwtw/py-sorting/blob/master/LICENSE>

import math

from common.helpers import default_compare

def sort(array, compare=default_compare):
  if len(array) <= 1:
    return array

  middle = math.floor(len(array) / 2)
  left = []
  right = []

  for i in range(0, middle):
    left.append(array[i])
  for i in range(middle, len(array)):
    right.append(array[i])

  return merge(sort(left, compare), sort(right, compare), compare)

def merge(left, right, compare):
  result = []
  leftIndex = 0
  rightIndex = 0

  while leftIndex < len(left) or rightIndex < len(right):
    if leftIndex < len(left) and rightIndex < len(right):
      if compare(left[leftIndex], right[rightIndex]) <= 0:
        result.append(left[leftIndex])
        leftIndex += 1
      else:
        result.append(right[rightIndex])
        rightIndex += 1
    elif leftIndex < len(left):
      result.append(left[leftIndex])
      leftIndex += 1
    elif rightIndex < len(right):
      result.append(right[rightIndex])
      rightIndex += 1

  return result
